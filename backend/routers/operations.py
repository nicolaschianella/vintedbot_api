###############################################################################
#
# File:      operations.py
# Author(s): Nico
# Scope:     Main routes used within the project routes
#
# Created:   16 January 2024
#
###############################################################################
import json
import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.models.models import CustomResponse, InputGetClothes, InputUpdateRequests, AddAssociations, User, \
                                  Clothe, AddClotheInStock, GetClothesInStock, SaleOfClothes, DeleteClothesFromStock, \
                                  Login, GetPickUp, SavePickUp, AutoBuy
from config.defines import VINTED_API_URL, VINTED_PRODUCTS_ENDPOINT, NB_RETRIES, \
                           MONGO_HOST_PORT, DB_NAME, REQUESTS_COLL, ASSOCIATIONS_COLL, VINTED_USER_ENDPOINT, \
                           STOCK_COLL, COOKIES_COLL, VINTED_BASE_URL, VINTED_SESSION_URL, HEADERS_LOGIN, NB_PICKUP, \
                           PICKUP_COLL, HEADERS_AUTOBUY, VINTED_BUY_URL, ALREADY_SOLD_CODE, VINTED_HEADERS_CHECKOUT_URL, \
                           VINTED_CHECKOUT_URL
from backend.utils.utils import define_session, set_cookies, reformat_clothes, serialize_datetime, check_mongo, \
                                extract_csrf_token, get_geocode, get_mondial_pickup_points, get_colissimo_pickup_points, \
                                compute_pickup_distance, store_cookies, fit_uuid, fit_pup
import logging
import time
import pytz
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/api/operations",
    tags=["operations"],
    responses={200: {"description": "Successful"},
               404: {"description": "Not Found"}}
)


@router.get("/get_clothes", status_code=200, response_model=CustomResponse)
async def get_clothes(input_filters: InputGetClothes) -> CustomResponse:
    """
    Used to get Vinted clothes based on specific filters

    Args:
        input_filters (backend.models.models.InputGetClothes): filters to apply

    Returns:
        backend.models.models.CustomResponse, with data section being all the found clothes
    """
    logging.info(f"Getting clothes with filters: {input_filters}")

    # price_from and price_to are a bit special -> excluded in request if empty (otherwise no response)
    input_filters_dict = input_filters.dict()

    if not input_filters_dict.get("price_from", None):
        input_filters_dict.pop("price_from")

    if not input_filters_dict.get("price_to", None):
        input_filters_dict.pop("price_to")

    # Format base API route to call
    url = f"{VINTED_API_URL}/{VINTED_PRODUCTS_ENDPOINT}"

    # Instantiate session
    session = define_session()
    session = set_cookies(session)

    # Try to call the API
    for attempt in range(NB_RETRIES):
        with session.get(url, params=input_filters_dict) as response:
            if response.status_code != 200 and attempt < NB_RETRIES:
                logging.warning(f"Could not get clothes with filters: {input_filters}, attempt: {attempt+1}")
                session = set_cookies(session)

            elif response.status_code == 200:
                logging.info(f"Successfully retrieved clothes with filters: {input_filters}. "
                             f"Proceeding with formatting data")

                output = json.dumps(reformat_clothes(response.json()["items"]), default=serialize_datetime)

                return JSONResponse(
                    status_code=200,
                    content={
                        "data": output,
                        "message": f"Clothes found with filters: {input_filters}",
                        "status": True
                    }
                )

    logging.error(f"Could not get clothes with filters: {input_filters}, max attempt reached. "
                  f"Full response: {response.json()}")

    return JSONResponse(
        status_code=500,
        content={
            "data": {},
            "message": f"Could not get clothes with filters: {input_filters}, max attempt reached.",
            "status": False
        }
    )


@router.get("/get_requests", status_code=200, response_model=CustomResponse)
async def get_requests() -> CustomResponse:
    """
    Used to get all the clothes requests stored in MongoDB

    Returns:
        backend.models.models.CustomResponse, with data section being all the found requests (list of dict)
    """
    logging.info("Getting all the existing requests")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    # Find active and inactive requests
    curs = list(client[DB_NAME][REQUESTS_COLL].find({"$or": [{"state": "active"}, {"state": "inactive"}]}))

    # Case no requests available
    if not curs:
        logging.warning(f"No available requests in ({DB_NAME}, {REQUESTS_COLL})")
        return JSONResponse(
            status_code=404,
            content={
                "data": {},
                "message": f"No available requests in ({DB_NAME}, {REQUESTS_COLL})",
                "status": False
            },
        )

    # Case where we have requests
    logging.info(f"Found requests: {curs}")
    return JSONResponse(
        status_code=200,
        content={
            "data": {"requests": json.dumps(curs, default=serialize_datetime)},
            "message": "Successfully found requests",
            "status": True
        },
    )


@router.post("/update_requests", status_code=200, response_model=CustomResponse)
async def update_requests(input_filters: InputUpdateRequests) -> CustomResponse:
    """
    Used to update all the clothes requests stored in MongoDB

    Args:
        input_filters (backend.models.models.InputUpdateRequests): filters to apply

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not, and concerned ids
        in data section
    """
    input_filters = input_filters.dict()
    logging.info(f"Updating all the existing requests, received: {input_filters}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    try:
        # Keep track of ids
        ids = {}
        # Find previous requests to log them
        curs = list(client[DB_NAME][REQUESTS_COLL].find())
        logging.info(f"Existing requests: {curs}")

        deleted, added, updated = input_filters["deleted"], input_filters["added"], input_filters["updated"]

        # Deleted requests
        if deleted:
            deleted_requests = []
            for _id in deleted:
                deleted_requests.extend(list(client[DB_NAME][REQUESTS_COLL].find({"_id": ObjectId(_id)})))
                client[DB_NAME][REQUESTS_COLL].update_one({"_id": ObjectId(_id)},
                                                          {"$set": {"state": "deleted",
                                                                    "updated": datetime.now()}})
            ids["deleted"] = deleted
            logging.info(f"Deleted requests: {deleted_requests}")

        # Added requests
        if added:
            added_ids = []
            for item in added:
                # Change creation_date and updated keys
                item["creation_date"] = item["updated"] = datetime.now()
                item.pop("id")
                _id = client[DB_NAME][REQUESTS_COLL].insert_one(item)
                added_ids.append(str(_id.inserted_id))
            ids["added"] = added_ids
            logging.info(f"Added requests: {added}")

        # Updated requests
        if updated:
            updated_ids = []
            for item in updated:
                # Change updated key
                item["updated"] = datetime.now()
                _id = item["id"]
                item.pop("id")
                client[DB_NAME][REQUESTS_COLL].update_one({"_id": ObjectId(_id)}, {"$set": item})
                updated_ids.append(_id)
            ids["updated"] = updated_ids
            logging.info(f"Updated requests: {updated}")

        # Find current requests to log them
        curs = list(client[DB_NAME][REQUESTS_COLL].find())

        logging.info(f"Successfully updated requests. Current requests: {curs}")

        return JSONResponse(
            status_code=200,
            content={
                "data": json.dumps(ids),
                "message": "Success",
                "status": True
            },
        )

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": "Internal Server Error",
                "status": False
            },
        )


@router.post("/add_association", status_code=200, response_model=CustomResponse)
async def add_association(association: AddAssociations) -> CustomResponse:
    """
    Used to add an association between clothe request_id and discord channel_id

    Args:
        association (backend.models.models.AddAssociations): association to add in the MongoDB

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    association_dict = association.dict()
    logging.info(f"Starting association insertion: {association_dict}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    try:
        # Add creation_date
        association_dict["creation_date"] = datetime.now()

        # Insertion
        client[DB_NAME][ASSOCIATIONS_COLL].insert_one(association_dict)

        # Case where we have requests
        logging.info(f"Inserted association: {association_dict}")
        return JSONResponse(
            status_code=200,
            content={
                "data": {},
                "message": "Success",
                "status": True
            },
        )

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": "Internal Server Error",
                "status": False
            },
        )


@router.get("/get_active_requests_and_channels", status_code=200, response_model=CustomResponse)
async def get_active_requests_and_channels() -> CustomResponse:
    """
    Used to get all active clothes requests and their corresponding channel id

    Returns:
        backend.models.models.CustomResponse, with data section being all the found requests and
        channels ids (list[dict, list])
    """
    logging.info("Acquiring all the requests and channel ids")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    try:
        # First get all associations
        associations = list(client[DB_NAME][ASSOCIATIONS_COLL].find())

        # Now get corresponding requests and channel ids
        requests = []
        channel_ids = []
        for association in associations:
            requests.append(list(client[DB_NAME][REQUESTS_COLL].find({"_id": ObjectId(association["request_id"])}))[0])
            channel_ids.append(association["channel_id"])

        response = {
            "requests": requests,
            "channel_ids": channel_ids
        }

        logging.info(f"Requests and channel ids found: {response['requests']}")

        return JSONResponse(
            status_code=200,
            content={
                "data": json.dumps(response, default=serialize_datetime),
                "message": "Success",
                "status": True
            },
        )

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Internal Server Error {e}",
                "status": False
            },
        )


@router.get("/get_user_infos", status_code=200, response_model=CustomResponse)
async def get_user_infos(user: User) -> CustomResponse:
    """
    Returns number of stars and number of reviews of a user

    Args:
        user (backend.models.models.User): the user to get the infos from

    Returns:
        backend.models.models.CustomResponse, with data section being the number of stars and number of reviews
    """
    logging.info(f"Getting infos from user: {user}")

    # Format base API route to call
    url = f"{VINTED_API_URL}/{VINTED_USER_ENDPOINT}"

    # Instantiate session
    session = define_session()
    session = set_cookies(session)

    # Try to call the API
    for attempt in range(NB_RETRIES):
        with session.get(f"{url}/{user.dict()['user_id']}") as response:
            if response.status_code != 200 and attempt < NB_RETRIES:
                logging.warning(f"Could not get infos from user: {user}, attempt: {attempt+1}")
                session = set_cookies(session)

            elif response.status_code == 200:
                logging.info(f"Successfully retrieved user infos for user: {user}")

                number_reviews = response.json()["user"]["feedback_count"]
                number_stars = float(response.json()["user"]["feedback_reputation"])

                # number_stars is a number between 0 and 1 -> convert to 1, 2, 3, 4 or 5 stars
                number_stars = round(5 * number_stars)

                logging.info(f"User: {user}, found number of reviews: {number_reviews}, "
                             f"number of stars: {number_stars}")

                output = json.dumps({"number_reviews": number_reviews,
                                     "number_stars": number_stars})

                return JSONResponse(
                    status_code=200,
                    content={
                        "data": output,
                        "message": f"Infos for user {user}",
                        "status": True
                    }
                )

            else:
                logging.error(f"Could not get infos for user: {user}, max attempt reached. "
                              f"Full response: {response.json()}")

                return JSONResponse(
                    status_code=500,
                    content={
                        "data": {},
                        "message": f"Could not get infos for user: {user}, max attempt reached. ",
                        "status": False
                    }
                )


@router.get("/get_images_url", status_code=200, response_model=CustomResponse)
async def get_images_url(clothe: Clothe) -> CustomResponse:
    """
    Returns all images URLs found for a given clothe URL

    Args:
        clothe (backend.models.models.Clothe): clothe object containing the URL to scrape images from

    Returns:
        backend.models.models.CustomResponse, with data section containing all found images URLs

    Note: using this method, we can only scrape the displayed carousel images. In case the item contains more
    than 5 images, they cannot be retrieved using this technique, since remaining images appear in the HTML code
    only after clicking on whatever displayed image.
    """
    logging.info(f"Getting images from URL: {clothe}")

    # Stopwatch
    start = time.time()

    # Instantiate session
    session = define_session()

    # Request page
    data = session.get(clothe.dict()["clothe_url"])

    # Retrieve page HTML
    html = data.text

    # Find images
    soup = BeautifulSoup(html, 'html.parser')

    # This is hard-coded since if page changes, it might be at a very different location anyway...
    carousel = soup.find("div", {"class": "item-photos"})

    try:
        images = carousel.find_all("img")
        images_url = []

        for img in images:
            src = img.get("src")
            images_url.append(src)

        end = time.time()

        logging.info(f"Found {len(images_url)} images in {end - start} seconds. URLs: {images_url}")

        return JSONResponse(
            status_code=200,
            content={
                "data": {"images_url": images_url},
                "message": f"Images for clothe {clothe}",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"There was an error acquiring images for {clothe}: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Could not get images for {clothe}",
                "status": False
            }
        )


@router.post("/add_clothe_in_stock", status_code=200, response_model=CustomResponse)
async def add_clothe_in_stock(clothe: AddClotheInStock) -> CustomResponse:
    """
    Registers a new clothe in stock

    Args:
        clothe (backend.models.models.AddClotheInStock): clothe to insert

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    logging.info(f"Registering clothe in stock: {clothe}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    clothe = clothe.dict()

    # Add "added_in_stock_date", "updated", "state", "selling_price" keys
    clothe["added_in_stock_date"] = clothe["updated"] = datetime.now()
    clothe["sale_date"] = clothe["selling_price"] = "NA"
    clothe["state"] = "in_stock"

    try:
        # Are there already clothes with this id in the DB?
        curs = list(client[DB_NAME][STOCK_COLL].find({"clothe_id": clothe["clothe_id"]}))

        if curs:
            logging.error(f"Clothe with clothe_id {clothe['clothe_id']} already exists in stock")

            return JSONResponse(
                status_code=501,
                content={
                    "data": {},
                    "message": f"Clothe with clothe_id {clothe['clothe_id']} already exists in stock",
                    "status": False
                }
            )

        # Insertion in stock
        client[DB_NAME][STOCK_COLL].insert_one(clothe)

        logging.info(f"Clothe {clothe} registered in stock")

        return JSONResponse(
            status_code=200,
            content={
                "data": {},
                "message": f"Clothe {clothe} registered in stock",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"Error while putting clothe in stock: {clothe}, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Could not insert clothe in stock: {clothe}",
                "status": False
            }
        )


@router.get("/get_clothes_from_stock", status_code=200, response_model=CustomResponse)
async def get_clothes_from_stock(mode: GetClothesInStock) -> CustomResponse:
    """
    Get clothes in stock

    Args:
        mode (backend.models.models.AddClotheInStock): one of "all", "in_stock", "sold"

    Returns:
        backend.models.models.CustomResponse, with data section being found clothes
    """
    logging.info(f"Getting clothes from stock, mode: {mode}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    mode = mode.dict()

    try:
        # Find clothes matching this filter
        if mode["which"] in ["in_stock", "sold"]:
            curs = list(client[DB_NAME][STOCK_COLL].find({"state": mode["which"]}))

        elif mode["which"] == "all":
            curs = list(client[DB_NAME][STOCK_COLL].find({}))

        else:
            logging.error(f"Wrong mode specified {mode} - should be one of 'in_stock', 'sold', 'all'")

            return JSONResponse(
                status_code=501,
                content={
                    "data": {},
                    "message": f"Wrong mode specified {mode} - should be one of 'in_stock', 'sold', 'all'",
                    "status": False
                }
            )

        logging.info(f"Found {len(curs)} clothe(s) in stock with mode {mode}")

        return JSONResponse(
            status_code=200,
            content={
                "data": json.dumps({"found_clothes": curs}, default=serialize_datetime),
                "message": f"Clothes from stock with mode {mode}",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"Error while getting clothes from stock with mode: {mode}, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Could not get clothes from stock with mode: {mode}",
                "status": False
            }
        )


@router.post("/sell_clothes", status_code=200, response_model=CustomResponse)
async def sell_clothes(clothe: SaleOfClothes) -> CustomResponse:
    """
    Updates clothes from in_stock to sold

    Args:
        clothe (backend.models.models.SaleOfClothes): clothe to sell

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    logging.info(f"Selling clothe in stock: {clothe}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    clothe = clothe.dict()

    original_sale_date = clothe["sale_date"]

    # Try to parse date into datetime object
    try:
        clothe["sale_date"] = pytz.timezone("Europe/Brussels").localize(datetime.strptime(clothe["sale_date"],
                                                                           "%d-%m-%Y %H:%M")).astimezone(pytz.utc)

    except Exception as e:
        logging.error(f"Could not parse date {original_sale_date} in format '%d-%m-%Y %H:%M': {e}")

        return JSONResponse(
            status_code=501,
            content={
                "data": {},
                "message": f"Could not parse date {original_sale_date} in format '%d-%m-%Y %H:%M'",
                "status": False
            }
        )

    try:
        # If ok, we can update the item in stock
        client[DB_NAME][STOCK_COLL].update_one({"clothe_id": clothe["clothe_id"]},
                                                  {"$set": {"state": "sold",
                                                            "selling_price": clothe["selling_price"],
                                                            "sale_date": clothe["sale_date"],
                                                            "updated": datetime.now()}})

        logging.info(f"Clothe {clothe} registered as sold")

        return JSONResponse(
            status_code=200,
            content={
                "data": {},
                "message": f"Clothe {clothe} registered as sold",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"Error while putting clothe as sold: {clothe}, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Could not insert clothe as sold: {clothe}",
                "status": False
            }
        )


@router.post("/delete_clothes", status_code=200, response_model=CustomResponse)
async def delete_clothes(clothe: DeleteClothesFromStock) -> CustomResponse:
    """
    Deletes clothes in stock

    Args:
        clothe (backend.models.models.DeleteClothesFromStock): clothe_id to delete

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    logging.info(f"Deleting clothe in stock: {clothe}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    clothe = clothe.dict()

    try:
        # If ok, we can update the item in stock
        client[DB_NAME][STOCK_COLL].delete_one({"clothe_id": clothe["clothe_id"]})

        logging.info(f"Clothe {clothe} deleted from stock")

        return JSONResponse(
            status_code=200,
            content={
                "data": {},
                "message": f"Clothe {clothe} deleted from stock",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"Error while deleting clothe from stock: {clothe}, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Could not delete clothe from stock: {clothe}",
                "status": False
            }
        )


@router.post("/login", status_code=200, response_model=CustomResponse)
async def login(log_in: Login) -> CustomResponse:
    """
    Log in, write CSRF-Token and cookies in Mongo

    Args:
        log_in (backend.models.models.Login): bearer token to log in

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    logging.info(f"Attempting login")

    log_in = log_in.dict()

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    try:
        bearer = log_in["bearer"]

        # Define session using base headers
        session = define_session()
        session = set_cookies(session)

        # First request to retrieve CSRF-Token
        req = session.get(VINTED_BASE_URL)
        csrf_token = extract_csrf_token(req.text)

        # First case - no CSRF-Token
        if not csrf_token:
            logging.error(f"Could not retrieve CSRF-Token, full response: {req.text}")

            return JSONResponse(
                status_code=501,
                content={
                    "data": {},
                    "message": "Could not retrieve CSRF-Token",
                    "status": False
                }
            )

        logging.info(f"CSRF-Token OK: {csrf_token}")

        # If OK attempt format headers
        headers_login = HEADERS_LOGIN.copy()
        headers_login["authorization"] = f"Bearer {bearer}"
        session = define_session(headers_login, False, session)

        # Attempt log in
        req = session.get(VINTED_SESSION_URL)

        # Success - post results in DB (update)
        if "v_uid" in req.cookies.get_dict().keys():
            logging.info("Login OK - pushing bearer, csrf-token and cookies in Mongo")

            client[DB_NAME][COOKIES_COLL].update_one({"name": "bearer"},
                                                     {"$set": {"value": bearer}},
                                                     upsert=True)

            client[DB_NAME][COOKIES_COLL].update_one({"name": "csrf_token"},
                                                     {"$set": {"value": csrf_token}},
                                                     upsert=True)

            client[DB_NAME][COOKIES_COLL].update_one({"name": "cookies"},
                                                     {"$set": {"value": session.cookies.get_dict()}},
                                                     upsert=True)

            logging.info("Insertion in DB OK")

            return JSONResponse(
                status_code=200,
                content={
                    "data": {},
                    "message": "Vinted login success",
                    "status": True
                }
            )

        # Error during login
        else:
            logging.error(f"Vinted login failed, status_code: {req.status_code}, full response: {req.text}")

            return JSONResponse(
                status_code=502,
                content={
                    "data": {},
                    "message": f"Vinted login failed, status_code: {req.status_code}",
                    "status": False
                }
            )

    except Exception as e:
        logging.error(f"Could not log in, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": "Internal server error",
                "status": False
            }
        )


@router.get("/get_close_pickup_points", status_code=200, response_model=CustomResponse)
async def get_close_pickup_points(address: GetPickUp) -> CustomResponse:
    """
    Get n close pick-up points for different services

    Args:
        address (backend.models.models.GetPickUp): address to look nearby

    Returns:
        backend.models.models.CustomResponse, with data section being found pick-up points
    """
    logging.info(f"Getting {NB_PICKUP} closest pickup points")

    try:
        address = address.dict()
        order = ["number", "street", "zipcode", "city", "country"]
        address_str = ""

        zipcode, city, country = address["zipcode"], address["city"], address["country"]

        # Get infos
        for o in order:
            address_str += address[o] + ","

        # Delete last coma
        address_str = address_str[:-1]

        lat, lon = get_geocode(address_str)

        # Get pick up points
        colissimo_pup = get_colissimo_pickup_points(lat, lon, zipcode, city, country)
        mondial_pup = get_mondial_pickup_points(zipcode, city)

        # mondial_up needs to be sorted by distance
        distances = []
        for pickup in mondial_pup:
            distances.append(compute_pickup_distance((float(lat), float(lon)),
                                                     (pickup["Adresse"]["Latitude"], pickup["Adresse"]["Longitude"])))

        mondial_pup = [pickup for _, pickup in sorted(zip(distances, mondial_pup))]

        # Filter NB_PICKUP closest
        colissimo_pup = colissimo_pup[:NB_PICKUP]
        mondial_pup = mondial_pup[:NB_PICKUP]

        if (len(colissimo_pup) == 0) or (len(mondial_pup) == 0):
            logging.error(f"One pick up points list is empty: colissimo len {len(colissimo_pup)}, mondial len "
                          f"{mondial_pup}")

            return JSONResponse(
                status_code=501,
                content={
                    "data": {},
                    "message": "One pick up points list is empty",
                    "status": False
                }
            )

        logging.info(f"Found {len(colissimo_pup)} colissimo pick up points and {len(mondial_pup)} mondial pick up "
                     f"points")

        # Format outputs
        output_misc = {"user_lat": lat,
                       "user_lon": lon}

        output_col = []

        for pickup in colissimo_pup:
            # Convert to float to remove zeros
            output_col_dict = {
                "lat": float(pickup["latitude"]),
                "lon": float(pickup["longitude"]),
                "user_display": pickup["name"] + " " +
                                pickup["address"] + " " +
                                pickup["zipcode"] + " " +
                                pickup["city"]
            }
            output_col.append(output_col_dict)

        output_mon = []

        for pickup in mondial_pup:
            output_mon_dict = {
                "lat": float(pickup["Adresse"]["Latitude"]),
                "lon": float(pickup["Adresse"]["Longitude"]),
                "user_display": pickup["Adresse"]["Libelle"] + " " +
                                pickup["Adresse"]["AdresseLigne1"] + " " +
                                pickup["Adresse"]["CodePostal"] + " " +
                                pickup["Adresse"]["Ville"]
            }
            output_mon.append(output_mon_dict)

        output = {
            "user_misc": output_misc,
            "col": output_col,
            "mon": output_mon
        }

        logging.info(f"Final output: {output}")

        return JSONResponse(
            status_code=200,
            content={
                "data": json.dumps(output),
                "message": f"Found {len(colissimo_pup)} colissimo pick up points and {len(mondial_pup)} mondial "
                           f"pick up points",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"Could get pick up points, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": "Internal server error",
                "status": False
            }
        )


@router.post("/save_pickup_points", status_code=200, response_model=CustomResponse)
async def save_pickup_points(positions: SavePickUp) -> CustomResponse:
    """
    Save pickup points and user position in DB

    Args:
        positions (backend.models.models.SavePickUp): user, colissimo and mondial positions

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    logging.info("Saving pickup points and user positions")

    positions = positions.dict()

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    try:
        # If ok, we can update pickup points
        col, mon, user = positions["col"], positions["mon"], positions["user_position"]

        client[DB_NAME][PICKUP_COLL].update_one({"type": "user"},
                                                {"$set": {"value": user}},
                                                upsert=True)

        client[DB_NAME][PICKUP_COLL].update_one({"type": "col"},
                                                {"$set": {"value": col}},
                                                upsert=True)

        client[DB_NAME][PICKUP_COLL].update_one({"type": "mon"},
                                                {"$set": {"value": mon}},
                                                upsert=True)

        logging.info("Successfully saved pickup points and user positions")

        return JSONResponse(
            status_code=200,
            content={
                "data": {},
                "message": "Successfully saved pickup points and user positions",
                "status": True
            }
        )

    except Exception as e:
        logging.error(f"Could save pick up points and user positions, exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": "Internal server error",
                "status": False
            }
        )


@router.post("/autobuy", status_code=200, response_model=CustomResponse)
async def autobuy(buy: AutoBuy) -> CustomResponse:
    """
    Autobuy an item on Vinted

    Args:
        buy (backend.models.models.AutoBuy): information needed for the transaction to be done

    Returns:
        backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    buy = buy.dict()

    item_id, seller_id, item_url = buy["item_id"], buy["seller_id"], buy["item_url"]

    logging.info(f"Autobuy, item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    try:
        # First we need to retrieve bearer stored in Mongo
        bearer = list(client[DB_NAME][COOKIES_COLL].find({"name": "bearer"}))[0]["value"]
        # Now log in
        await login(Login.parse_obj({"bearer": bearer}))

        # Now retrieve CSRF-Tokenn anon_id and generated cookies
        csrf_token = list(client[DB_NAME][COOKIES_COLL].find({"name": "csrf_token"}))[0]["value"]
        cookies = list(client[DB_NAME][COOKIES_COLL].find({"name": "cookies"}))[0]["value"]
        anon_id = cookies["anon_id"]

        # Define headers
        buy_headers = HEADERS_AUTOBUY.copy()
        buy_headers["content-type"] = "application/json"
        buy_headers["referer"] = item_url
        buy_headers["x-anon-id"] = anon_id
        buy_headers["x-csrf-token"] = csrf_token

        # Define a new session object, apply cookies and headers
        session = define_session(headers=buy_headers, cookies=cookies)

        # Format params
        params_buy = {"initiator": "buy",
                      "item_id": item_id,
                      "opposite_user_id": seller_id}

        ########################################### BUY REQUEST ###########################################

        # Buy request
        buy = session.post(VINTED_BUY_URL, data=json.dumps(params_buy))

        # First case - item already sold
        if (buy.status_code == 400) and (int(json.loads(buy.text)["code"]) == ALREADY_SOLD_CODE):
            logging.warning(f"Item already sold: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url}), "
                            f"full response: {buy.text}")

            # Save session cookies
            store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

            return JSONResponse(
                status_code=501,
                content={
                    "data": {},
                    "message": "Already sold",
                    "status": False
                }
            )

        # Second case - not 200
        elif buy.status_code != 200:
            logging.error(f"Issue with buy request: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url}), "
                          f"full response: {buy.text}")

            # Save session cookies
            store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

            return JSONResponse(
                status_code=502,
                content={
                    "data": {},
                    "message": f"Issue with buy request: {buy.text}",
                    "status": False
                }
            )

        # Third case - OK
        logging.info(f"Buy request OK: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url})")

        ########################################### CHECKOUT REQUEST ###########################################

        # Proceed to store cookies
        store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

        # Find transaction_id
        transaction_id = re.search(r'"transaction":{"id":([^"]+),"', buy.text).group(1)

        # Define new headers
        checkout_headers = HEADERS_AUTOBUY.copy()
        checkout_headers["content-type"] = "application/x-www-form-urlencoded"
        checkout_headers["referer"] = f"{VINTED_HEADERS_CHECKOUT_URL}{transaction_id}"
        checkout_headers["x-anon-id"] = anon_id
        checkout_headers["x-csrf-token"] = csrf_token
        checkout_headers["x-money-object"] = "true"

        # Update session object (to keep cookies) and headers
        session = define_session(headers=checkout_headers, new=False, session=session)

        # Checkout request
        checkout = session.put(f"{VINTED_CHECKOUT_URL}/{transaction_id}/checkout")

        # First case - not 200
        if checkout.status_code != 200:
            logging.error(f"Issue with checkout request: (item_id: {item_id}, seller_id: {seller_id}, "
                          f"item_url: {item_url}), full response: {checkout.text}")

            # Save session cookies
            store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

            return JSONResponse(
                status_code=503,
                content={
                    "data": {},
                    "message": f"Issue with checkout request: {checkout.text}",
                    "status": False
                }
            )

        # Second case - OK
        logging.info(f"Checkout request OK: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url})")

        ########################################### SHIPPING REQUEST ###########################################

        # Proceed to store cookies
        store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

        # GET THE DEFAULT PICK UP POINT UUID's
        rate_uuid, root_rate_uuid = fit_uuid(checkout.text)

        # Define new headers
        shipping_headers = HEADERS_AUTOBUY.copy()
        del shipping_headers["origin"]
        shipping_headers["referer"] = f"{VINTED_HEADERS_CHECKOUT_URL}{transaction_id}"
        shipping_headers["x-anon-id"] = anon_id
        shipping_headers["x-csrf-token"] = csrf_token
        shipping_headers["x-money-object"] = "true"

        # Update session object (to keep cookies) and headers
        session = define_session(headers=shipping_headers, new=False, session=session)

        # Get user lat and lon
        user_info = list(client[DB_NAME][PICKUP_COLL].find({"type": "user"}))[0]["value"]
        user_lat, user_lon = user_info["user_lat"], user_info["user_lon"]

        # Format params
        params_shipping = {
                        'country_code': 'FR',
                        'latitude': float(user_lat),
                        'longitude': float(user_lon),
                        'should_label_nearest_points': 'false'
                    }

        logging.info(f"params_shipping: {params_shipping}")

        # Make request
        shipping = session.get(f"{VINTED_CHECKOUT_URL}/{transaction_id}/nearby_shipping_options",
                               data=params_shipping)

        # First case - not 200
        if shipping.status_code != 200:
            logging.error(f"Issue with shipping request: (item_id: {item_id}, seller_id: {seller_id}, "
                          f"item_url: {item_url}), full response: {shipping.text}")

            # Save session cookies
            store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

            return JSONResponse(
                status_code=504,
                content={
                    "data": {},
                    "message": f"Issue with shipping request: {shipping.text}",
                    "status": False
                }
            )

        # Second case - OK
        logging.info(f"Shipping request OK: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url})")

        ########################################### PICKUP REQUEST ###########################################

        # Proceed to store cookies
        store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

        # Get pickup points infos
        col_info = list(client[DB_NAME][PICKUP_COLL].find({"type": "col"}))[0]["value"]
        mon_info = list(client[DB_NAME][PICKUP_COLL].find({"type": "mon"}))[0]["value"]
        col_lat, col_lon = float(col_info["lat"]), float(col_info["lon"])
        mon_lat, mon_lon = float(mon_info["lat"]), float(mon_info["lon"])

        # Get data for the chosen pickup point
        new_uuid, pup_code, trans_code = fit_pup(json.loads(shipping.text)['nearby_shipping_points'],
                                                 [col_lat, col_lon],
                                                 [mon_lat, mon_lon],
                                                 json.loads(checkout.text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_options"])

        # Define new headers
        pickup_headers = HEADERS_AUTOBUY.copy()
        pickup_headers["content-type"] = "application/json"
        pickup_headers["referer"] = f"{VINTED_HEADERS_CHECKOUT_URL}{transaction_id}"
        pickup_headers["x-anon-id"] = anon_id
        pickup_headers["x-csrf-token"] = csrf_token
        pickup_headers["x-money-object"] = "true"

        # Update session object (to keep cookies) and headers
        session = define_session(headers=pickup_headers, new=False, session=session)

        # Format params
        params_pickup = {
                    "transaction":{
                        "shipment":{
                            "package_type_id": trans_code,
                            "pickup_point_code": pup_code,
                            "rate_uuid": rate_uuid,
                            "point_uuid": new_uuid,
                            "root_rate_uuid": root_rate_uuid
                        },
                        "buyer_debit": {},
                        "offline_verification": {}
                    }
                }

        logging.info(f"params_pickup: {params_pickup}")

        # Make request
        pickup = session.put(f"{VINTED_CHECKOUT_URL}/{transaction_id}/checkout",
                             data=json.dumps(params_pickup))

        # First case - not 200
        if pickup.status_code != 200:
            logging.error(f"Issue with pickup request: (item_id: {item_id}, seller_id: {seller_id}, "
                          f"item_url: {item_url}), full response: {pickup.text}")

            # Save session cookies
            store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

            return JSONResponse(
                status_code=505,
                content={
                    "data": {},
                    "message": f"Issue with pickup request: {pickup.text}",
                    "status": False
                }
            )

        # Second case - OK
        logging.info(f"Pickup request OK: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url})")

        ########################################### PAY REQUEST ###########################################

        # Proceed to store cookies
        store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

        # Get payment ID
        checksum = re.search(r'"checksum":"([^"]+)"', pickup.text).group(1)

        # Define new headers
        pay_headers = HEADERS_AUTOBUY.copy()
        pay_headers["content-type"] = "application/json"
        pay_headers["referer"] = f"{VINTED_HEADERS_CHECKOUT_URL}{transaction_id}"
        pay_headers["x-anon-id"] = anon_id
        pay_headers["x-csrf-token"] = csrf_token

        # Update session object (to keep cookies) and headers
        session = define_session(headers=pay_headers, new=False, session=session)

        # Format params
        params_pay = {"checksum": f"{checksum}",
                      "browser_attributes": {
                          "language": "en-US",
                          "color_depth": 24,
                          "java_enabled": "false",
                          "screen_height": 1080,
                          "screen_width": 1920,
                          "timezone_offset": -60}
                      }

        # Make request
        pay = session.post(f"{VINTED_CHECKOUT_URL}/{transaction_id}/checkout/payment",
                          data=json.dumps(params_pay))

        # First case - not 200
        if pay.status_code != 200:
            logging.error(f"Issue with pay request: (item_id: {item_id}, seller_id: {seller_id}, "
                          f"item_url: {item_url}), full response: {pay.text}")

            # Save session cookies
            store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

            return JSONResponse(
                status_code=506,
                content={
                    "data": {},
                    "message": f"Issue with pay request: {pay.text}",
                    "status": False
                }
            )

        # Second case - OK
        logging.info(f"Pay request OK: (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url})")

        # Save session cookies
        store_cookies(client, DB_NAME, COOKIES_COLL, session.cookies.get_dict())

        return JSONResponse(
            status_code=200,
            content={
                "data": {},
                "message": "Success",
                "status": False
            }
        )

    except Exception as e:
        logging.error(f"Could not autobuy (item_id: {item_id}, seller_id: {seller_id}, item_url: {item_url}), "
                      f"exception: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"Internal server error: {e}",
                "status": False
            }
        )

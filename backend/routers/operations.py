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
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.models.models import CustomResponse, InputGetClothes, InputUpdateRequests, AddAssociations, User, \
                                  Clothe, AddClotheInStock, GetClothesInStock
from config.defines import VINTED_API_URL, VINTED_PRODUCTS_ENDPOINT, NB_RETRIES, \
                           MONGO_HOST_PORT, DB_NAME, REQUESTS_COLL, ASSOCIATIONS_COLL, VINTED_USER_ENDPOINT, \
                           STOCK_COLL
from backend.utils.utils import define_session, set_cookies, reformat_clothes, serialize_datetime, check_mongo
import logging
import time
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
        input_filters: backend.models.models.InputGetClothes, filters to apply

    Returns: backend.models.models.CustomResponse, with data section being all the found clothes

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

            else:
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
    :return: backend.models.models.CustomResponse, with data section being all the found requests (list of dict)
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
    :return: backend.models.models.CustomResponse, with custom status_code if successful or not, and concerned ids
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
    :return: backend.models.models.CustomResponse, with custom status_code if successful or not
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
    :return: backend.models.models.CustomResponse, with data section being all the found requests and
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
        user: backend.models.models.User, the user to get the infos from

    Returns: backend.models.models.CustomResponse, with data section being the number of stars and number of reviews

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
        clothe: backend.models.models.Clothe, clothe object containing the URL to scrape images from

    Returns: backend.models.models.CustomResponse, with data section containing all found images URLs

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
        clothe: backend.models.models.AddClotheInStock, clothe to insert

    Returns: backend.models.models.CustomResponse, with custom status_code if successful or not

    """
    logging.info(f"Registering clothe in stock: {clothe}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

    clothe = clothe.dict()

    # Add "added_in_stock", "updated", "state", "selling_price" keys
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
        mode: backend.models.models.AddClotheInStock, one of "all", "in_stock", "sold"

    Returns: backend.models.models.CustomResponse, with data section being found clothes

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

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
from backend.models.models import CustomResponse, InputGetClothes, InputUpdateRequests, PostAssociations
from config.defines import VINTED_API_URL, VINTED_PRODUCTS_ENDPOINT, NB_RETRIES, \
                           MONGO_HOST_PORT, DB_NAME, REQUESTS_COLL, ASSOCIATIONS_COLL
from backend.utils.utils import define_session, set_cookies, reformat_clothes, serialize_datetime, check_mongo
import logging
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
async def add_association(association: PostAssociations):
    """
    Used to add an association between clothe request_id and discord channel_id
    :return: backend.models.models.CustomResponse, with custom status_code if successful or not
    """
    association_dict = association.dict()
    logging.info(f"Starting association insertion: {association_dict}")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)
    check_mongo(client)

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

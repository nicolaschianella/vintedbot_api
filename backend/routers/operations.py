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
from backend.models.models import CustomResponse, InputGetClothes
from config.defines import VINTED_API_URL, VINTED_PRODUCTS_ENDPOINT, NB_RETRIES, \
                           MONGO_HOST_PORT, DB_NAME, REQUESTS_COLL
from backend.utils.utils import define_session, set_cookies, reformat_clothes, serialize_datetime
import logging
from pymongo import MongoClient

router = APIRouter(
    prefix="/api/operations",
    tags=["operations"],
    responses={200: {"description": "Successful"},
               404: {"description": "Not Found"}}
)


@router.get("/get_clothes", status_code=200, response_model=CustomResponse)
async def get_clothes(input_filters: InputGetClothes):
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
async def get_requests():
    """
    Used to get all the clothes requests stored in MongoDB
    :return: backend.models.models.CustomResponse, with data section being all the found requests (list of dict)
    """
    logging.info(f"Getting all the existing requests")

    # Instantiate MongoClient
    client = MongoClient(MONGO_HOST_PORT, serverSelectionTimeoutMS=10000)

    # Check MongoDB health state
    try:
        client.server_info()

    except Exception as e:
        logging.error(f"MongoDB is not alive, error {e}")
        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "message": f"MongoDB is not alive, error: {str(e)}",
                "status": False
            },
        )

    # Find all the requests
    curs = list(client[DB_NAME][REQUESTS_COLL].find())

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
            "data": {"requests": curs},
            "message": "Successfully found requests",
            "status": True
        },
    )

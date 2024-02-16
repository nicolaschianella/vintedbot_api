###############################################################################
#
# File:      utils.py
# Author(s): Nico
# Scope:     Utils
#
# Created:   16 January 2024
#
###############################################################################
from config.defines import VINTED_AUTH_URL, HEADERS_BASE_URL
from pymongo import MongoClient
import requests
import logging
import bson
import re
from datetime import datetime, timezone


def define_session(headers=HEADERS_BASE_URL, new=True, session=None) -> requests.Session:
    """
    Generic function to define a user session and set headers

    Args:
        headers: dict, headers to set
        new: bool, whether we want a full new session or update existing
        session: request.Session, if we want to update this session (new should be False in this case)

    Returns:

    """
    if new:
        session = requests.Session()

    session.headers.update(headers)

    return session

def set_cookies(session: requests.Session) -> requests.Session:
    """
    Sets AUTH cookie to session, to allow users to get Vinted clothes
    Args:
        session: requests.Session, session instance with headers already set

    Returns:
        session: requests.Session, session instance with AUTH cookies set

    """
    session.cookies.clear_session_cookies()

    try:
        session.post(VINTED_AUTH_URL)

    except Exception as e:
        logging.error(f"There was an error fetching cookies for vinted\n Error: {e}")

    return session

def reformat_clothes(clothes: list[dict]) -> list[dict]:
    """
    Reformat clothes gotten from get_clothes route to keep only desirable information
    Args:
        clothes: list of dictionaries with every dictionary being the result of get_clothes route

    Returns:
        output: list of dictionaries with every dictionary filtered on desirable keys

    """
    output = []

    # Define every wanted field
    for clothe in clothes:
        try:
            reformat_clothe = dict()

            reformat_clothe["id"] = clothe["id"]
            reformat_clothe['seller_id'] = clothe["user"]["id"]
            reformat_clothe["title"] = clothe["title"]
            reformat_clothe["brand_title"] = clothe["brand_title"]
            reformat_clothe["size_title"] = clothe["size_title"]
            reformat_clothe["status"] = clothe["status"]
            reformat_clothe["price_no_fee"] = clothe["price"]
            reformat_clothe["service_fee"] = clothe["service_fee"]
            reformat_clothe["total_item_price"] = clothe["total_item_price"]
            reformat_clothe["currency"] = clothe["currency"]
            reformat_clothe["url"] = clothe["url"]

            # Sometimes no picture, not a big deal we don't make the program crash in this case
            reformat_clothe["photo_url"] = clothe["photo"]["url"] if clothe.get("photo", None) else "NA"
            reformat_clothe["is_photo_suspicious"] = clothe["photo"]["is_suspicious"] if clothe.get("photo", None)\
                else "NA"
            reformat_clothe["created_at_ts"] = datetime.fromtimestamp(
                clothe["photo"]["high_resolution"]["timestamp"], tz=timezone.utc
            ) if clothe.get("photo", None) else "NA"
            reformat_clothe["raw_timestamp"] = clothe["photo"]["high_resolution"]["timestamp"] \
                if clothe.get("photo", None) else "NA"

            reformat_clothe["favourite_count"] = clothe["favourite_count"]
            reformat_clothe["view_count"] = clothe["view_count"]

            output.append(reformat_clothe)

        except Exception as e:
            logging.warning(f"Could not reformat clothe {clothe} \nError: {e}")

    logging.info(f"Successfully reformatted {len(output)} clothe(s)")

    return output

def serialize_datetime(obj):
    """
    Small util function to JSON-serialize datetime objects
    Args:
        obj: datetime object

    Returns:
        A JSON serializable datetime object

    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bson.objectid.ObjectId):
        return str(obj)

def check_mongo(client: MongoClient):
    """
    Checks Mongo helath state and returns an error in case
    :param client: MongoClient to check
    :return: None if OK, JSONResponse status_code 500 if error
    """
    # Check MongoDB health state
    try:
        client.server_info()

    except Exception as e:
        logging.error(f"MongoDB is not alive, error {e}")
        raise Exception(f"MongoDB is not alive, error {e}")

def extract_csrf_token(request_text):
    """
    Extracts CSRF-Token from request text
    Args:
        request_text: str, request text

    Returns: str

    """
    match = re.search(r'\\"CSRF_TOKEN\\":\\"([^"]+)\\"', request_text)

    if match:
        token = match.group(1)
        logging.info(f"Extracted CSRF-Token: {token}")
        return token

    else:
        logging.error(f"Error getting CSRF-Token")

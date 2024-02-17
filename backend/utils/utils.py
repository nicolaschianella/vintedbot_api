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
import json
from datetime import datetime, timezone
from geopy.geocoders import Nominatim
import geopy.distance


def define_session(headers=HEADERS_BASE_URL, new=True, session=None, cookies=None) -> requests.Session:
    """
    Generic function to define a user session and set headers and cookies

    Args:
        headers: dict, headers to set
        new: bool, whether we want a full new session or update existing
        session: request.Session, if we want to update this session (new should be False in this case)
        cookies: dict, cookies to set

    Returns:

    """
    if new:
        session = requests.Session()

    session.headers.update(headers)

    if cookies:
        session.cookies.update(cookies)

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

def get_geocode(address):
    """
    Get the latitude and longitude of the given address
    Args:
        address: str, user address

    Returns: tuple[float, float], latitude and longitude

    """
    logging.info("Getting address lat, lon")

    geolocator = Nominatim(user_agent='user')
    location = geolocator.geocode(address)

    lat, lon = float(location.raw['lat']), float(location.raw['lon'])

    logging.info(f"Found address lat: {lat}, lon: {lon}")

    return lat, lon

def get_mondial_pickup_points(zipcode, city):
    """
    Get mondial pickup
    Args:
        zipcode: str
        city: str

    Returns: list, list of pickup points (from closest to furthest)

    """

    headers = {
        'authority': 'www.mondialrelay.fr',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr-FR',
        'referer': f'https://www.mondialrelay.fr/trouver-le-point-relais-le-plus-proche-de-chez-moi/?codePays=FR&codePostal={zipcode}',
        'requestverificationtoken': 'VRMZ-6oSgJoMPCKSPfvptpkzQ6TyFek_lYpi69-XaHGPzODs12jS2AbFbvHKKxVGbodS1Haon-vBlV1VsxcNJzIGtuk1:uQ0aA4Q6Y_hdgwfbWiV6iHi88CNCaMA-_gbxx0B4VMlTnLWJ8d-1DGbAedgy4Yw0_xil6wfyrAvbzDJijqi76jRypME1',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://www.mondialrelay.fr/api/parcelshop?country=FR&postcode={zipcode}&city={city}&services=&excludeSat=false&naturesAllowed=1,A,E,F,D,J,T,S,C&agencesAllowed=',
        headers=headers,
    )

    return json.loads(response.text)

def get_colissimo_pickup_points(latitude, longitude, zipcode, city, country):
    """
    Get colissimo pickup
    Args:
        latitude: str
        longitude: str
        zipcode: str
        city: str
        country: str

    Returns: list, list of pickup points (from closest to furthest)

    """

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'https://www.chronopost.fr/expeditionAvanceeSec/ounoustrouver.html?copyButton=1&key=7n8nI15pWlZ3wC6o16gigg==&zipCode={zipcode}&city={city}&backUrl=http://infosco.chronopost.fr&category=2&vue=relaissansservice',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'lat': latitude,
        'lon': longitude,
        'r': '40',
        'z': zipcode,
        'c': city,
        'a': '',
        'p': country,
        'lang': 'null',
        '_': '170862393908',
    }

    response = requests.get(
        'https://www.chronopost.fr/expeditionAvanceeSec/stubpointsearchinterparservice.json',
        params=params,
        headers=headers,
    )

    return json.loads(response.text)['olgiPointList']

def compute_pickup_distance(point_1: tuple, point_2: tuple) -> float:
    """
    Compute distance between two points using coordinates in km
    Args:
        point_1: tuple, (lat1, lon1)
        point_2: tuple, (lat2, lon2)

    Returns: float, distance in km

    """
    return geopy.distance.geodesic(point_1, point_2).km

def store_cookies(client: MongoClient, db: str, coll: str, cookies: dict) -> None:
    """
    Stores cookies in Mongo to keep track of session cookies
    Args:
        client: MongoClient
        db: str, db where we store cookies
        coll: str, collection where we store cookies
        cookies: dict, cookies to store

    Returns: None

    """
    logging.info("Storing cookies in Mongo")

    # No upsert needed since process crashes in any way if record doesn't exist
    client[db][coll].update_one({"name": "cookies"},
                                {"$set": {"value": cookies}})
    logging.info("Storing cookies OK")

def fit_uuid(text) :
    """
    Get the default uuid's from Vinted.
    These are then used in the param file for the pickup point update.
    Args:
        text: str, request response text

    Returns: tuple[str, str]

    """
    rate_uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_option"]["rate_uuid"]
    root_rate_uuid = json.loads(text)["checkout"]["services"]["shipping"]["delivery_types"]["pickup"]["shipping_option"]["root_rate_uuid"]

    logging.info("rate_uuid, root_rate_uuid OK")

    return rate_uuid, root_rate_uuid

def code_pup(p):
    """
    Returns the transporter code as defined by Vinted
    Args:
        p: dict, pickup point

    Returns: int, transporter code

    """
    if p['point']['carrier_id'] == 4:
        m = 1017

    elif p['point']['carrier_id'] == 27:
        m = 118

    else:
        m = 0

    logging.info(f"Found transporter code: {m}")

    return m

def fit_pup(pick_up_available, col_pup, mon_pup) :
    """
    Scans the nearby pickup points and tries to find one of the user's defined point.
    If no match, returns the first point of the list.
    Args:
        pick_up_available: list, nearby pickup points
        col_pup: tuple[float, float], latitude and longitude for colissimo saved pickup point
        mon_pup: tuple[float, float], latitude and longitude for mondial saved pickup point

    Returns: tuple[int, str, str], point_uuid, point_code, transporter_code

    """

    i = 0

    try :
        while float(pick_up_available[i].get('point').get('latitude')) != col_pup[0] and float(pick_up_available[i].get('point').get('latitude')) != mon_pup[0]:
            i+=1

        if float(pick_up_available[i].get('point').get('longitude')) == col_pup[1] or float(pick_up_available[i].get('point').get('longitude')) == mon_pup[1]:
            marker = i

        else:
            marker = 0

    except IndexError:
        marker = 0

    point_uuid, point_code, transporter_code = (pick_up_available[marker].get('point').get('uuid'),
                                                pick_up_available[marker].get('point').get('code'),
                                                code_pup(pick_up_available[marker]))

    logging.info(f"Found point_uuid: {point_uuid}, point_code: {point_code}, transporter_code: {transporter_code}")

    return point_uuid, point_code, transporter_code

###############################################################################
#
# File:      defines.py
# Author(s): Nico
# Scope:     General variables to be used within the project
#
# Created:   13 January 2024
#
###############################################################################


########## Routes, header ##########
# Vinted BASE URL
VINTED_BASE_URL = "https://www.vinted.fr"
# Base API URL
VINTED_API_URL = f"{VINTED_BASE_URL}/api/v2"
# End point used to get clothes
VINTED_PRODUCTS_ENDPOINT = "catalog/items"
# End point to get user infos
VINTED_USER_ENDPOINT = "users/"
# Number of retries to get clothes
NB_RETRIES = 5
# Number of pickup points to retrieve
NB_PICKUP = 5
# If item is already bought using autobuy
ALREADY_SOLD_CODE = 99
# Vinted SESSION URL to login
VINTED_SESSION_URL = f"{VINTED_BASE_URL}/member/general/session_from_token"
# Vinted AUTH URL to get clothes
VINTED_AUTH_URL = f"{VINTED_BASE_URL}/auth/token_refresh"
# Vinted BUY URL - buy request
VINTED_BUY_URL = f"{VINTED_API_URL}/conversations"
# Vinted CHECKOUT URL - checkout request
VINTED_CHECKOUT_URL = f"{VINTED_API_URL}/transactions"
# Headers for base url
HEADERS_BASE_URL = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr',
        "host": VINTED_BASE_URL.split("//")[-1]
    }
# Headers to log in
HEADERS_LOGIN = {
    'authority': VINTED_BASE_URL.split("//")[-1],
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    "referer": f"{VINTED_BASE_URL}",
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
# Generic headers to autobuy
HEADERS_AUTOBUY = {
    'authority': VINTED_BASE_URL.split("//")[-1],
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    'origin': f'{VINTED_BASE_URL}',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
# Vinted CHECKOUT URL - checkout request (formatted in headers)
VINTED_HEADERS_CHECKOUT_URL = f"{VINTED_BASE_URL}/checkout?transaction_id="

########## MongoDB related ##########
# MongoDB Host/Port
MONGO_HOST_PORT = "mongodb://localhost:27017"
# Main DB name to use
DB_NAME = "guysvinted"
# Collection containing requests
# Keys: all filters (backend.models.models.InputGetClothes) + 'creation_date' (UTC) = when the request was created
# + 'name' = unique name characterizing the request
REQUESTS_COLL = "requests"
# Collection containing associations {clothe_request_id: discord_channel_id}
ASSOCIATIONS_COLL = "associations"
# Collection for stock
STOCK_COLL = "stock"
# Collection for CSRF-Token and session cookies
COOKIES_COLL = "cookies"
# Collection for pickup points and user positions
PICKUP_COLL = "pickup"

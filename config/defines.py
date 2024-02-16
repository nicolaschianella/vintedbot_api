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
# Base API URL
VINTED_API_URL = f"https://www.vinted.fr/api/v2"
# End point used to get clothes
VINTED_PRODUCTS_ENDPOINT = "catalog/items"
# End point to get user infos
VINTED_USER_ENDPOINT = "users/"
# Number of retries to get clothes
NB_RETRIES = 5
# Vinted AUTH URL to get clothes
VINTED_AUTH_URL = "https://www.vinted.fr/auth/token_refresh"
# Vinted BASE URL
VINTED_BASE_URL = "https://www.vinted.fr"
# Headers for base url
HEADERS_BASE_URL = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr',
        "host": "www.vinted.fr"
    }
# Vinted SESSION URL to login
VINTED_SESSION_URL = "https://www.vinted.fr/member/general/session_from_token"
# Headers to log in
HEADERS_LOGIN = {
    'authority': 'www.vinted.fr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'fr',
    "referer":"https://www.vinted.fr/",
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

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

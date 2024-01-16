###############################################################################
#
# File:      defines.py
# Author(s): Nico
# Scope:     General variables to be used within the project
#
# Created:   13 January 2024
#
###############################################################################


# Base API URL
VINTED_API_URL = f"https://www.vinted.fr/api/v2"
# End point used to get clothes
VINTED_PRODUCTS_ENDPOINT = "catalog/items"
# Number of retries to get clothes
NB_RETRIES = 5
# Headers to pass for get_clothes route
HEADERS_GET_CLOTHES = {
    "User-Agent": "PostmanRuntime/7.28.4",
    "Host": "www.vinted.fr"
}
# Vinted AUTH URL to get clothes
VINTED_AUTH_URL = "https://www.vinted.fr/auth/token_refresh"

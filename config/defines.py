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
# Headers to pass for get_clothes route
HEADERS_GET_CLOTHES = {
    "User-Agent": "PostmanRuntime/7.28.4",
    "Host": "www.vinted.fr"
}
# Vinted AUTH URL to get clothes
VINTED_AUTH_URL = "https://www.vinted.fr/auth/token_refresh"

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

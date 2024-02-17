###############################################################################
#
# File:      models.py
# Author(s): Nico
# Scope:     Define base structures to be used in routes
#
# Created:   13 January 2024
#
###############################################################################
from pydantic import BaseModel
from typing import List


class CustomResponse(BaseModel):
    data: dict
    message: str
    status: bool


class InputGetClothes(BaseModel):
    # Page number to get items from per search
    page: str = "1"
    # Number of items for this page to get per search
    per_page: str = "96"
    # "Rechercher" field
    search_text: str = ""
    # "Catégorie" filter
    catalog_ids: str = ""
    # "Couleur" field (if multiple, separate them with a coma)
    color_ids: str = ""
    # "Marque" field (if multiple, separate them with a coma)
    brand_ids: str = ""
    # "Taille" filter (if multiple, separate them with a coma)
    size_ids: str = ""
    # "Matière" field (if multiple, separate them with a coma)
    material_ids: str = ""
    # Price from -> parameter only appears in API if value != ""
    price_from: str = ""
    # Price to -> parameter only appears in API if value != ""
    price_to: str = ""
    # "Etat" field (if multiple, separate them with a coma)
    status_ids: str = ""
    # "Trier par" field
    order: str = "newest_first"
    # Not a filter itself but necessary for the API to work
    currency: str = "EUR"


class AddedUpdatedRequests(BaseModel):
    """
    Model wrapped in InputUpdateRequests to update requests
    """
    # MongoDB _id
    id: str = ""
    # Request name
    name: str = "DEFAULT"
    # Creation date
    creation_date: str = ""
    # State: active or inactive
    state: str = "active"
    # Update date
    updated: str = ""
    # Page number to get items from per search
    page: str = "1"
    # Number of items for this page to get per search
    per_page: str = "96"
    # "Rechercher" field
    search_text: str = ""
    # "Catégorie" filter
    catalog_ids: str = ""
    # "Couleur" field (if multiple, separate them with a coma)
    color_ids: str = ""
    # "Marque" field (if multiple, separate them with a coma)
    brand_ids: str = ""
    # "Taille" filter (if multiple, separate them with a coma)
    size_ids: str = ""
    # "Matière" field (if multiple, separate them with a coma)
    material_ids: str = ""
    # Price from -> parameter only appears in API if value != ""
    price_from: str = ""
    # Price to -> parameter only appears in API if value != ""
    price_to: str = ""
    # "Etat" field (if multiple, separate them with a coma)
    status_ids: str = ""
    # "Trier par" field
    order: str = "newest_first"
    # Not a filter itself but necessary for the API to work
    currency: str = "EUR"


class InputUpdateRequests(BaseModel):
    # ids to delete
    deleted: List[str] = []
    # Rows to add
    added: List[AddedUpdatedRequests] = []
    # Rows to update
    updated: List[AddedUpdatedRequests] = []


class AddAssociations(BaseModel):
    # request_id
    request_id: str
    # request name
    request_name: str
    # channel_id
    channel_id: str
    # channel name
    channel_name: str


class User(BaseModel):
    # user_id
    user_id: str


class Clothe(BaseModel):
    # clothe_url
    clothe_url: str


class AddClotheInStock(BaseModel):
    """
    Represents clothes we add in stock
    """
    # request_id in our DB used to get this clothe
    request_id: str
    # Vinted clothe id
    clothe_id: str
    # seller_id
    seller_id: str
    # clothe name
    title: str
    # brand name
    brand_title: str
    # size
    size_title: str
    # clothe state
    status: str
    # prices
    price_no_fee: str
    service_fee: str
    total_item_price: str
    # Always EUR
    currency: str
    # clothe url, photo url
    url: str
    photo_url: str
    # can this be sometimes yes?
    is_photo_suspicious: str
    # when the clothe was put in Vinted's DB
    created_at_ts: str
    raw_timestamp: str
    # number of favourites/views when we bought the clothe
    favourite_count: str
    view_count: str
    # fuzz partial ratio (clothe name/request search text)
    ratio: str


class GetClothesInStock(BaseModel):
    # "all", "in_stock" or "sold"
    which: str = "all"


class SaleOfClothes(BaseModel):
    # clothe_id
    clothe_id: str
    # sale_date
    sale_date: str
    # selling_price
    selling_price: str


class DeleteClothesFromStock(BaseModel):
    # clothe_id
    clothe_id: str


class Login(BaseModel):
    # Bearer token
    bearer: str


class GetPickUp(BaseModel):
    # Number
    number: str
    # Street
    street: str
    # Zipcode
    zipcode: str
    # City
    city: str
    # Country
    country: str


class UserPosition(BaseModel):
    # latitude
    user_lat: str
    # longitude
    user_lon: str


class PickUpPosition(BaseModel):
    # latitude
    lat: str
    # longitude
    lon: str
    # name, address
    user_display: str

class SavePickUp(BaseModel):
    # colissimo position
    col: PickUpPosition
    # mondial position
    mon: PickUpPosition
    # user position
    user_position: UserPosition


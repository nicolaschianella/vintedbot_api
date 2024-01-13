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


class CustomResponse(BaseModel):
    data: dict
    message: str
    status: bool


class InputGetClothes(BaseModel):
    nb_items: int = 50
    search_text: str = ""
    catalog_ids: str = ""
    color_ids: str = ""
    brand_ids: str = ""
    size_ids: str = ""
    material_ids: str = ""
    status_ids: str = ""
    country_ids: str = ""
    city_ids: str = ""
    is_for_swap: str = ""
    currency: str = "EUR"
    price_to: int = 1000
    price_from: int = 0
    order: str = "newest_first"
    time: None

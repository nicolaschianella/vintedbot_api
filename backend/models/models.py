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
    # Page number to get items from per search
    page: str = "1"
    # Number of items for this page to get per search
    per_page: str = "96"
    # "Rechercher" field
    search_text: str = ""
    # "Catégorie" filter
    catalog_ids: str = ""
    # "Couleur" field
    color_ids: str = ""
    # "Marque" field
    brand_ids: str = ""
    # "Taille" filter
    size_ids: str = ""
    # "Matière" field
    material_ids: str = ""
    # Price from -> parameter only appears in API if value != ""
    price_from: str = ""
    # Price to -> parameter only appears in API if value != ""
    price_to: str = ""
    # "Etat" field
    status_ids: str = ""
    # "Trier par" field
    order: str = "newest_first"
    # Not a filter itself but necessary for the API to work
    currency: str = "EUR"

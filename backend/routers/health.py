###############################################################################
#
# File:      health.py
# Author(s): Nico
# Scope:     Health-related routes
#
# Created:   15 January 2024
#
###############################################################################
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.models.models import CustomResponse
import logging

router = APIRouter(
    prefix="/api/health",
    tags=["health"],
    responses={200: {"description": "Successful"},
               404: {"description": "Not Found"}}
)


@router.get("/backend", status_code=200, response_model=CustomResponse)
async def health_check():
    """
    Simple route to check if the API is alive
    :return:
    """
    logging.info("I am alive, please check the docs for my usage")
    return JSONResponse(
        status_code=200,
        content={
            "data": {},
            "message": "I am alive, please check the docs for my usage",
            "status": True
        }
    )

###############################################################################
#
# File:      main.py
# Author(s): Nico
# Scope:     Entry point
#
# Created:   13 January 2024
#
###############################################################################
import argparse
import logging
import os
import time
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.models.models import CustomResponse
from backend.routers import operations

app = FastAPI(
    title="VintedBot",
    description="Auto-manage purchases and sales from Vinted",
    version="1.0",
    license="Guys Copyright"
)




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
from backend.routers import health, operations


if __name__ == "__main__":

    # Get arguments
    parser = argparse.ArgumentParser(description="VintedBot")
    parser.add_argument(
        "-p",
        "--port",
        action="store",
        default=8000,
        help="Specify port to use",
        required=False
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store",
        default="vinted_bot.log",
        help="Specify output log file",
        required=False
    )

    args = parser.parse_args()

    # Set timezone to UTC
    os.environ["TZ"] = "UTC"
    time.tzset()

    # Define logs config
    logging.basicConfig(
        filename=args.log,
        level=logging.DEBUG,
        format="%(asctime)s -- %(funcName)s -- %(levelname)s -- %(message)s"
    )

    # Define app, include routes
    app = FastAPI(
        title="VintedBot",
        description="Auto-manage purchases and sales from Vinted",
        version="1.0",
        license="Guys Copyright"
    )

    app.include_router(health.router)
    app.include_router(operations.router)

    # Run app - override log_config parameter
    uvicorn.run(app, host="127.0.0.1", port=int(args.port), log_config=None)

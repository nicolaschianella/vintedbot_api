###############################################################################
#
# File:      utils.py
# Author(s): Nico
# Scope:     Utils
#
# Created:   16 January 2024
#
###############################################################################
from config.defines import HEADERS_GET_CLOTHES, VINTED_AUTH_URL
import requests
import logging

def define_session():
    """
    Generic function to define a new user session and set headers

    Returns: requests.Session, session instance with headers set

    """
    session = requests.Session()
    session.headers.update(HEADERS_GET_CLOTHES)

    return session

def set_cookies(session):
    """
    Sets AUTH cookie to session, to allow users to get Vinted clothes
    Args:
        session: requests.Session, session instance with headers already set

    Returns:
        session: requests.Session, session instance with AUTH cookies set

    """
    session.cookies.clear_session_cookies()

    try:
        session.post(VINTED_AUTH_URL)

    except Exception as e:
        logging.error(f"There was an error fetching cookies for vinted\n Error: {e}")

    return session

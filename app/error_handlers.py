# Error handler functions intended to globally handle errors throughout the Flask application will be placed here

from app.base_api_error import BaseApiError


def handle_base_api_error(e: BaseApiError):
    print("BaseApiError triggered")
    return e.build_error()


def handle_generic_exception(e: Exception):
    print("Generic exception triggered")
    return {"error": str(e)}, 500

# Error handler functions intended to globally handle errors throughout the Flask application will be placed here
import traceback
from app.base_api_error import BaseApiError


def handle_base_api_error(e: BaseApiError):
    return e.build_error()


def handle_generic_exception(e: Exception):
    print(traceback.format_exc())
    return {"success": False, "message": str(e)}, 500

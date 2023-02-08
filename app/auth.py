from firebase_admin import auth
from firebase_admin._user_mgt import UserRecord
from werkzeug.exceptions import Unauthorized
from typing import Dict, Any
from functools import wraps

from app.user_api.User import User
from app.user_api.user_service import find_user
from app.user_api.errors import UserNotFoundError


def with_auth_user(func):
    """
    Decorator to transform attach the firebase user record to the function
    using the token_info decoded from the Authorization header.

    Usage
    ```
    @with_auth_user
    def my_function(user: UserRecord, **kwargs):
        ...
    ```
    Note: It's important to have **kwargs to pass `token_info` arg to the decorator.

    :param func: Function to decorate
    :return: Decorated function
    """

    @wraps(func)
    def wrapper(*args, token_info: Dict[str, Any], **kwargs):
        try:
            firebase_user_record: UserRecord = auth.get_user(token_info["uid"])
            user: User = find_user(firebase_user_record.email)
            kwargs["user"] = user
        except ValueError as e:
            return {"error": "Invalid user ID", "message": str(e)}, 400
        except auth.UserNotFoundError as e:
            return {"error": "User not found in firebase auth", "message": str(e)}, 404
        except UserNotFoundError as e:
            return {"error": "User not found in database", "message": str(e)}, 404
        except Exception as e:
            return {"error": "Unknown error", "message": str(e)}, 500

        return func(*args, **kwargs)

    return wrapper


def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate and decode a JWT token using Firebase

    :param token: JWT token passed as a Bearer token in the Authorization header
    :return: Dictionary of value pairs from the decoded JWT

    :raises Unauthorized: If the token is invalid, expired, revoked, or the certificate cannot be fetched
    :raises ValueError: If the token is not a string or empty
    """
    try:
        return auth.verify_id_token(token)
    except (
        auth.InvalidIdTokenError,
        auth.ExpiredIdTokenError,
        auth.RevokedIdTokenError,
        auth.CertificateFetchError,
    ) as e:
        raise Unauthorized(f"Invalid token. {str(e)}") from e

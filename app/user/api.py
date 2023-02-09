from .service import create_user, delete_user
from app.events.service import (
    generate_account_signup_event,
    generate_account_delete_event,
)
from .errors import UserNotFoundError, UserAlreadyExistsError
from .user import User
from flask import jsonify
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from typing import Dict, Any
from app.auth import with_auth_user

# Note: this endpoint will NOT use our middleware wrapper, since at this point we have no User record yet. We will default to the parameters connexion gives us
def new_user_signup(token_info: Dict[str, Any]):
    try:
        firebase_user_record: auth.UserRecord = auth.get_user(token_info["uid"])
        new_user = create_user(firebase_user_record.email)
        generate_account_signup_event(new_user)
    except ValueError as e:
        return {"error": "Invalid user ID", "message": str(e)}, 400
    except auth.UserNotFoundError as e:
        return {"error": "User not found in firebase auth", "message": str(e)}, 404
    except UserAlreadyExistsError as e:
        return e.buildError()
    # except Exception as e:
    #   return {"error": "Unknown error", "message": str(e)}, 500
    return "", 204


@with_auth_user
def delete_user_profile(user, **kwargs):
    try:
        delete_user(user)
        generate_account_delete_event(user)
    except UserNotFoundError:
        return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    return {"message": "Success"}, 200

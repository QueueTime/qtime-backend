from .service import create_user, delete_user
from .errors import UserNotFoundError, UserAlreadyExistsError
from firebase_admin import auth
from typing import Dict, Any
from app.auth import with_auth_user
from app.user.user import User

# Note: this endpoint will NOT use our middleware wrapper, since at this point we have no User record yet. We will default to the parameters connexion gives us
def new_user_signup(token_info: Dict[str, Any]):
    try:
        firebase_user_record: auth.UserRecord = auth.get_user(token_info["uid"])
        create_user(firebase_user_record.email)
    except ValueError as e:
        return {"error": "Invalid user ID", "message": str(e)}, 400
    except auth.UserNotFoundError as e:
        return {"error": "User not found in firebase auth", "message": str(e)}, 404
    return None, 204


@with_auth_user
def delete_user_profile(user: User, **kwargs):
    delete_user(user)
    return None, 204

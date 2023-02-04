from .user_service import User_Service
from .errors import UserNotFoundError, UserAuthenticationError
from .User import User
from flask import jsonify
from firebase_admin import auth
import jwt

user_service = User_Service()


def get_user_profile(email):
    try:
        user = user_service.findUser(email)
    except UserNotFoundError:
        return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    return jsonify(user.to_dict()), 200


def delete_user_profile(email):
    try:
        target_user = user_service.findUser(email)
        user = user_service.deleteUser(target_user)
    except UserNotFoundError:
        return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    return {"message": "Success"}, 200


def test_authenticate(token_info):
    try:
        user = auth.get_user(token_info["uid"])
        return f"Success, you are {user.email}", 200
    except ValueError as e:
        return {"error": "Invalid user ID", "details": str(e)}, 400
    except auth.UserNotFoundError as e:
        return {"error": "User not found", "details": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 500

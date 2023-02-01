from .user_service import User_Service
from .errors import UserNotFoundError
from .User import User
from flask import jsonify

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

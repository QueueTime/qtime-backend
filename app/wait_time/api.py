from flask import jsonify
from app.auth import with_auth_user
from app.user.user import User
from typing import Dict, Any
from .location import UserLocation
from .service import uid_to_aid, update_location, add_wait_time_suggestion
from app.common import BaseApiError


@with_auth_user
def update_user_location(
    user: User, location_data: Dict[str, float], token_info: Dict[str, Any]
):
    try:
        user_location = UserLocation.from_dict(
            uid_to_aid(token_info["uid"]), location_data
        )
        update_location(user_location)
    except BaseApiError as e:
        return e.build_error()
    except Exception as e:
        return {"error": str(e)}, 500
    return None, 204


@with_auth_user
def submit_user_estimate(
    user: User, estimate_data: Dict[str, int], poi_id: str, **kwargs
):
    # TODO: implement user estimate submission
    # If we need more POI data, change this to fetch the actual POI object instead of just using poi_id
    try:
        if estimate_data["wait_time_estimate"] < 0:
            return {"error": "Invalid wait time submission"}, 400
        add_wait_time_suggestion(user, poi_id, estimate_data["wait_time_estimate"])
    except BaseApiError as e:
        return e.build_error()
    except Exception as e:
        return {"error", str(e)}, 500
    return None, 204

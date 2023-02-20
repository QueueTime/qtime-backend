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
    """
    Takes in a JSON body with location data in the following format:
    {
        "latitude": float,
        "longitude": float
    }

    Latitide is expected to be a float between -90 and 90. Longitude is expected to be
    a float between -180 and 180
    """
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
    """
    Receives poi_id from the request path and estimate data from the request body.
    Estimate data is expected to be in the following JSON format:
    {
        "wait_time_estimate": int
    }

    Wait time estimate is expected to be an int greater than or equal to 0.
    poi_id is expected to be a valid POI ID.
    """
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

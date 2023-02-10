from flask import jsonify
from app.auth import with_auth_user
from app.user.user import User
from typing import Dict, Any


@with_auth_user
def update_user_location(user: User, location_data: Dict[str, float], **kwargs):
    # TODO: implement uploading user location
    return jsonify(location_data), 200


@with_auth_user
def submit_user_estimate(
    user: User, estimate_data: Dict[str, int], poi_id: str, **kwargs
):
    # TODO: implement user estimate submission
    return jsonify(estimate_data), 200

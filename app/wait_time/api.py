from flask import jsonify
from app.auth import with_auth_user


@with_auth_user
def update_user_location(user, location_data, **kwargs):
    # TODO: implement uploading user location
    return jsonify(location_data), 200


@with_auth_user
def submit_user_estimate(user, estimate_data, poi_id, **kwargs):
    # TODO: implement user estimate submission
    return jsonify(estimate_data), 200

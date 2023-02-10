from flask import jsonify
from app.auth import with_auth_user


@with_auth_user
def update_user_location(user, location_data, **kwargs):
    # TODO: implement uploading user location
    return jsonify(location_data), 200

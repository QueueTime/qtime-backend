from flask import jsonify


def get_server_health():
    return jsonify({"status": "up"})

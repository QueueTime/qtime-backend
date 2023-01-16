from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("app/key/serviceAccountKey.json")
default_app = initialize_app(cred)
firestore_db = firestore.client()


def create_app():
    app = Flask(__name__)

    @app.route("/success")
    def health():
        return jsonify("success")

    return app

from datetime import datetime
from app import firestore_db
from flask import jsonify


def list_places():
    poi_ref = firestore_db.collection("POI")
    all_poi = [doc.to_dict() for doc in poi_ref.stream()]
    return jsonify(all_poi), 200

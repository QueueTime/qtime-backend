from datetime import datetime
from app import common
from app.firebase import firestore_db
from flask import jsonify


class POI(common.FirebaseDataEntity):
    def __init__(
        self,
        db_ref,
        name,
        clasification,
        hours_of_operation,
        address,
        type,
        longitude,
        latitude,
        image_url,
    ):
        super().__init__(db_ref)
        if db_ref is None:
            self.db_ref = firestore_db
        self.name = name
        self.classification = clasification
        self.hours_of_operation = hours_of_operation
        self.address = address
        self.type = type
        self.longitude = longitude
        self.latitude = latitude
        self.image_url = image_url

    def get_all_POI():
        poi_ref = firestore_db.collection("POI")
        all_poi = [doc.to_dict() for doc in poi_ref.stream()]
        return jsonify(all_poi), 200

    def get_POI(poi_id):
        try:
            poi_ref = firestore_db.collection("POI")
            poi = poi_ref.document(poi_id).get()
            return jsonify(poi.to_dict()), 200
        except Exception as e:
            return f"An Error Occured: {e}"

    def save_POI_suggestion():
        pass

    def create_POI_suggestion():
        pass

    def fetch_latest_estimated_value():
        pass

    def generate_histogram_for_POI():
        pass

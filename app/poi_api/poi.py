from datetime import datetime
from app import firestore_db, common
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

    # replace with db ref from super class
    def list_POI():
        poi_ref = firestore_db.collection("POI")
        all_poi = [doc.to_dict() for doc in poi_ref.stream()]
        return jsonify(all_poi), 200

    # def get(db_ref, id):
    #     poi_ref = firestore_db.collection("POI")
    #     all_poi = [doc.to_dict() for doc in poi_ref.stream()]
    #     return jsonify(all_poi), 200

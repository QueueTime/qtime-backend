from datetime import datetime
from app import common
from app.firebase import firestore_db
from app.poi_api.poi_errors import POINotFoundError
from flask import jsonify


class POI(common.FirebaseDataEntity):
    def __init__(
        self,
        db_ref,
        _id,
        name,
        clasification,
        hours_of_operation,
        address,
        poi_type,
        location,
        image_url,
    ):
        super().__init__(db_ref)
        self._id = _id
        self.name = name
        self.classification = clasification
        self.hours_of_operation = hours_of_operation
        self.address = address
        self.poi_type = poi_type
        self.location = location
        self.image_url = image_url

    def get(db_ref, id):
        target_data = db_ref.document(id).get()
        if not target_data.exists:
            raise POINotFoundError(id)
        return POI.from_dict(db_ref, target_data.to_dict())

    def from_dict(db_ref, dict):
        try:
            return POI(
                db_ref,
                dict["_id"],
                dict["address"],
                dict["class"],
                dict["hours_of_operation"],
                dict["image_url"],
                dict["location"],
                dict["name"],
                dict["type"],
            )
        except KeyError as e:
            raise common.BadDataError("Missing data from poi data: " + str(e))

    def to_dict(self):
        poi_dict = {
            "_id": self._id,
            "address": self.address,
            "class": self.classification,
            "hours_of_operation": self.hours_of_operation,
            "image_url": self.image_url,
            "location": self.location,
            "name": self.name,
            "type": self.poi_type,
        }
        return poi_dict

    def push(self, merge=True):
        target_ref = self.db_reference.document(self._id)
        target_ref.set(self.to_dict(), merge=merge)

    def __eq__(self, other):
        return self._id == other._id

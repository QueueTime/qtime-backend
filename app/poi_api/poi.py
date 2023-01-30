from datetime import datetime
from app import firestore_db, common
from flask import jsonify


class POI:
    def __init__(
        self,
        _id,
        name,
        clasification,
        hours_of_operation,
        address,
        poi_type,
        location,
        image_url,
    ):
        self._id = _id
        self.name = name
        self.classification = clasification
        self.hours_of_operation = hours_of_operation
        self.address = address
        self.poi_type = poi_type
        self.location = location
        self.image_url = image_url

    def to_dict(self):
        poi_suggestion_dict = {
            "_id": self._id,
            "address": self.address,
            "class": self.classification,
            "hours_of_operation": self.hours_of_operation,
            "image_url": self.image_url,
            "location": self.location,
            "name": self.name,
            "type": self.poi_type,
        }
        return poi_suggestion_dict

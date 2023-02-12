from enum import Enum
from typing import Dict
from app.common import BadDataError
from app.poi_api.errors import POINotFoundError
import json


class POI:
    def __init__(
        self,
        _id: str,
        name: str,
        classification: str,
        hours_of_operation: Dict[str, str],
        address: str,
        poi_type: str,
        location: Dict[str, str],
        image_url: str,
    ):
        self._id = _id
        self.name = name
        self.classification = classification
        self.hours_of_operation = hours_of_operation
        self.address = address
        self.poi_type = poi_type
        self.location = location
        self.image_url = image_url

    @staticmethod
    def from_dict(dict: Dict[str, str]) -> "POI":
        """
        Creates a new POI object from a Python Dictionary

        Args:
            dict: Dictionary of key-value pairs corresponding to the poi.

        Returns:
            POI: from specified data

        Raises:
            BadDataError: If required data is missing from the dictionary
        """
        try:
            return POI(
                _id=dict["_id"],
                name=dict["name"],
                classification=dict["class"],
                hours_of_operation=dict["hours_of_operation"],
                address=dict["address"],
                poi_type=dict["type"],
                location=dict["location"],
                image_url=dict["image_url"],
            )
        except KeyError as e:
            raise BadDataError("Missing data from poi data: " + str(e))

    def to_dict(self) -> Dict[str, str]:
        """
        Returns a dictionary containing all properties from the POI

        Returns:
            dict: containing key-value pairs with all POI data
        """
        return {
            "_id": self._id,
            "address": self.address,
            "class": self.classification,
            "hours_of_operation": self.hours_of_operation,
            "image_url": self.image_url,
            "location": self.location,
            "name": self.name,
            "type": self.poi_type,
        }

    def to_json(self) -> str:
        """Return all properties in a JSON string"""
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        return self._id == other._id

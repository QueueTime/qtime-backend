from enum import Enum
from typing import Dict, Any
from app.common import BadDataError
from app.locations.errors import POINotFoundError
import json


class POIClassification(Enum):
    """
    Classification of the POI.
    Queue if there can exist a line at the POI.
    Occupancy if we are interested in the occupancy of the POI.
    POIs cannot be of both types.
    """

    QUEUE = "queue"
    OCCUPANCY = "occupancy"


class POI:
    def __init__(
        self,
        id: str,
        name: str,
        classification: POIClassification,
        hours_of_operation: Dict[str, Any],
        address: str,
        poi_type: str,
        location: Dict[str, Any],
        image_url: str,
    ):
        self.id = id
        self.name = name
        self.classification = POIClassification(classification)
        self.hours_of_operation = hours_of_operation
        self.address = address
        self.poi_type = poi_type
        self.location = location
        self.image_url = image_url

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "POI":
        """
        Creates a POI object from a dictionary.

        :param dict: Dictionary of the parameters corresponding to a POI
        """
        try:
            return POI(
                id=dict["_id"],
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Creates a dictionary from a POI object
        """
        return {
            "_id": self.id,
            "address": self.address,
            "class": self.classification.value,
            "hours_of_operation": self.hours_of_operation,
            "image_url": self.image_url,
            "location": self.location,
            "name": self.name,
            "type": self.poi_type,
        }

    def to_json(self) -> str:
        """
        Return all properties in a JSON string
        """
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        """
        Checks if two POI objects are equal based on id
        """
        return isinstance(other, POI) and self.to_dict() == other.to_dict()

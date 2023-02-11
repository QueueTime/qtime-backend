from datetime import datetime
from typing import Dict, Any
from app.common import BadDataError
import json


class Location:
    def __init__(
        self,
        aid: str,
        latitude: float,
        longitude: float,
        timestamp: datetime = datetime.now(),
    ):
        self.aid = aid
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    @staticmethod
    def from_dict(aid: str, dict: Dict[str, Any]) -> "Location":
        """
        Creates a new Location object from a Python Dictionary

        :param dict: Dictionary of key-value pairs corresponding to location.
        :returns: Location from specified data
        :raises BadDataError: If required data is missing from the dictionary
        """
        try:
            return Location(aid, dict["latitude"], dict["longitude"], dict["timestamp"])
        except KeyError as e:
            raise BadDataError("Missing data from Location data: " + str(e))

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all properties from the User

        :returns: dictionary containing key-value pairs with all User data
        """
        return {
            "aid": self.aid,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        """Return all properties in a JSON string"""
        json_dict = self.to_dict()
        json_dict["timestamp"] = json_dict["timestamp"].isoformat()
        return json.dumps(json_dict)

    def __eq__(self, other):
        return self.aid == other.aid

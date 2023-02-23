from datetime import datetime, timezone
from typing import Dict, Any
from app.common import BadDataError
import json


class UserLocation:
    def __init__(
        self,
        aid: str,
        latitude: float,
        longitude: float,
        timestamp: datetime = datetime.now(timezone.utc),
    ):
        self.aid = aid
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    @staticmethod
    def from_dict(aid: str, dict: Dict[str, Any]) -> "UserLocation":
        """
        Creates a new UserLocation object from a Python Dictionary

        :param dict: Dictionary of key-value pairs corresponding to location.
        :returns: UserLocation from specified data
        :raises BadDataError: If required data is missing from the dictionary
        """
        try:
            location = UserLocation(
                aid,
                dict["latitude"],
                dict["longitude"],
                dict.get("timestamp", datetime.now(timezone.utc)),
            )
        except KeyError as e:
            raise BadDataError("Missing data from Location data: " + str(e))

        if not _is_valid_gps_coordinates(location.latitude, location.longitude):
            raise BadDataError(
                f"Invalid GPS coordinates: latitude={location.latitude}, longitude={location.longitude}"
            )

        return location

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all properties from the UserLocation

        :returns: dictionary containing key-value pairs with all UserLocation data
        """
        dict = self.__dict__
        # Delete primary key before returning dict
        del dict["aid"]
        return dict

    def to_json(self) -> str:
        """Return all properties in a JSON string"""
        json_dict = self.to_dict()
        json_dict["timestamp"] = json_dict["timestamp"].isoformat()
        return json.dumps(json_dict)

    def __eq__(self, other):
        return isinstance(other, UserLocation) and self.to_dict() == other.to_dict()


def _is_valid_gps_coordinates(latitude, longitude):
    return latitude >= -90 and latitude <= 90 and longitude >= -180 and longitude <= 180

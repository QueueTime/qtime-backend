from datetime import datetime
from app.poi_api.errors import POINotFoundError, InvalidPOISuggestionError
from app.common import BadDataError
from typing import Dict
import json


class POI_suggestion:
    def __init__(
        self,
        pid,
        suggestion_name,
        notes,
        submitted_by,
        submission_time=datetime.now(),
    ) -> None:
        self._pid = pid
        self.suggestion_name = suggestion_name
        self.notes = notes
        self.submitted_by = submitted_by
        self.submission_time = submission_time

    def get_pid(self) -> str:
        """Return pid of the POI_suggestion"""
        return self._pid

    @staticmethod
    def from_dict(dict: Dict[str, str]) -> "POI_suggestion":
        """
        Creates a new POI_suggestion object from a Python Dictionary

        Args:
            dict: Dictionary of key-value pairs corresponding to user.

        Returns:
            User: from specified data

        Raises:
            BadDataError: If required data is missing from the dictionary
        """
        try:
            return POI_suggestion(
                dict["_pid"],
                dict["suggestion_name"],
                dict["notes"],
                dict["submission_time"],
                dict["submitted_by"],
            )
        except KeyError as e:
            raise BadDataError("Missing data from poi suggestion data: " + str(e))

    def to_dict(self) -> Dict[str, str]:
        """
        Returns a dictionary containing all properties from the POI_suggestion

        Returns:
            dict: containing key-value pairs with all POI_suggestion data
        """
        return self.__dict__

    def to_json(self) -> str:
        """Return all properties in a JSON string"""
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        return self._pid == other._pid

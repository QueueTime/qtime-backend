from datetime import datetime
from app.locations.errors import POINotFoundError, InvalidPOISuggestionError
from app.common import BadDataError
from typing import Dict
import json


class POI_suggestion:
    def __init__(
        self,
        pid,
        suggestion_name,
        notes,
        submission_time=datetime.now(datetime.timezone.utc),
    ) -> None:
        self._pid = pid
        self.suggestion_name = suggestion_name
        self.notes = notes
        self.submission_time = submission_time

    def get_pid(self) -> str:
        """
        Returns the pid of the POI suggestion
        """
        return self._pid

    @staticmethod
    def from_dict(dict: Dict[str, str]) -> "POI_suggestion":
        """
        Creates a POI_suggestion object from a dictionary.

        :param dict: Dictionary of the parameters corresponding to a POI_suggestion
        """
        try:
            return POI_suggestion(
                pid=dict["_pid"],
                suggestion_name=dict["suggestion_name"],
                notes=dict["notes"],
                submission_timedict=datetime.now(datetime.timezone.utc),
            )
        except KeyError as e:
            raise BadDataError("Missing data from poi suggestion data: " + str(e))

    def to_dict(self) -> Dict[str, str]:
        """
        Creates a dictionary from a POI_suggestion object
        """
        return self.__dict__

    def to_json(self) -> str:
        """
        Return all properties in a JSON string
        """
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        """
        Checks if two POI_suggestion objects are equal based on pid
        """
        return self._pid == other._pid

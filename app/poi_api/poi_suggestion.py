from datetime import datetime
from app.poi_api.poi_errors import POINotFoundError, InvalidPOISuggestionError
from app import common


class POI_suggestions(common.FirebaseDataEntity):
    def __init__(
        self,
        db_ref,
        pid,
        suggestion_name,
        notes,
        submitted_by,
        submission_time=datetime.now(),
    ) -> None:
        super().__init__(db_ref)
        self._pid = pid
        self.suggestion_name = suggestion_name
        self.notes = notes
        self.submitted_by = submitted_by
        self.submission_time = submission_time

    def get_pid(self):
        return self._pid

    def get(db_ref, id):
        target_data = db_ref.document(id).get()
        if not target_data.exists:
            raise POINotFoundError(id)
        return POI_suggestions.from_dict(db_ref, target_data.to_dict())

    def to_dict(self):
        poi_suggestion_dict = {
            "_pid": self._pid,
            "suggestion_name": self.suggestion_name,
            "notes": self.notes,
            "submission_time": self.submission_time,
            "submitted_by": self.submitted_by,
        }
        return poi_suggestion_dict

    def from_dict(db_ref, dict):
        try:
            return POI_suggestions(
                db_ref,
                dict["_pid"],
                dict["suggestion_name"],
                dict["notes"],
                dict["submission_time"],
                dict["submitted_by"],
            )
        except KeyError as e:
            raise common.BadDataError(
                "Missing data from poi suggestion data: " + str(e)
            )

    def push(self, merge=True):
        target_ref = self.db_reference.document(self._pid)
        target_ref.set(self.to_dict(), merge=merge)

    def __eq__(self, other):
        return self._pid == other._pid

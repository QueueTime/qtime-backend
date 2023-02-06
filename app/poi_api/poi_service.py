from app.firebase import firestore_db
from flask import jsonify
from .poi_suggestion import POI_suggestions
from .poi import POI
from .poi_errors import POINotFoundError, InvalidPOISuggestionError
from app import common
from datetime import datetime

# TODO: Fix error handling
class POI_Service:
    def __init__(self):
        self.poi_ref = firestore_db.collection("POI")
        self.poi_suggestion_ref = firestore_db.collection("POI_proposal")

    def get_all_POI(self):
        return [
            POI.from_dict(self.poi_ref, doc.to_dict()) for doc in self.poi_ref.stream()
        ]

    def get_POI(self, poi_id):
        return POI.get(self.poi_ref, poi_id)

    def suggest_new_POI(self, poi_suggestion):
        poi_suggestion_ref = self.poi_suggestion_ref.document()
        # Generate id for poi suggestion document
        pid = poi_suggestion_ref.id
        poi_suggestion_instance = self._create_POI_suggestion(pid, poi_suggestion)
        poi_suggestion_instance.push()
        return 204

    def _create_POI_suggestion(self, pid, poi_suggestion):
        try:
            suggestion_name = poi_suggestion.get("suggestion_name")
            notes = poi_suggestion.get("notes")
            submission_time = datetime.now()
            submitted_by = poi_suggestion.get("submitted_by")
            if suggestion_name is None or submitted_by is None:
                raise InvalidPOISuggestionError("Invalid POI submission")
            return POI_suggestions(
                self.poi_suggestion_ref,
                pid,
                suggestion_name,
                notes,
                submitted_by,
                submission_time,
            )
        except KeyError as e:
            raise common.BadDataError(
                "Missing data from poi suggestion data: " + str(e)
            )

    def _fetch_latest_estimated_value(self):
        pass

    def _generate_histogram_for_POI(self):
        pass

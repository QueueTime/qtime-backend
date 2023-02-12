from flask import jsonify
from typing import List, Dict
from .poi_suggestion import POI_suggestion
from .poi import POI
from .errors import POINotFoundError, InvalidPOISuggestionError
from app import common
from datetime import datetime
from app.firebase import firestore_db, POI_COLLECTION, POI_PROPOSAL_COLLECTION

poi_collection = firestore_db.collection(POI_COLLECTION)
poi_proposal_collection = firestore_db.collection(POI_PROPOSAL_COLLECTION)


def list_POI() -> List[POI]:
    return [POI.from_dict(doc.to_dict()) for doc in poi_collection.stream()]


def get_details_for_POI(poi_id: str) -> POI:
    poi_data = poi_collection.document(poi_id).get()
    if not poi_data.exists:
        raise POINotFoundError(poi_id)
    return POI.from_dict(poi_data.to_dict())


def new_POI_suggestion(poi_suggestion: Dict[str, str]) -> int:
    poi_suggestion_ref = poi_proposal_collection.document()
    # Generate id for poi suggestion document
    pid = poi_suggestion_ref.id
    poi_suggestion_instance = _create_POI_suggestion(pid, poi_suggestion)
    _save_POI_suggestion(poi_suggestion_instance, pid)
    return 204


def _save_POI_suggestion(
    poi_suggestion_instance: POI_suggestion, pid: str, merge: bool = True
) -> None:
    target_ref = poi_proposal_collection.document(pid)
    target_ref.set(poi_suggestion_instance.to_dict(), merge=merge)


def _create_POI_suggestion(pid: str, poi_suggestion: Dict[str, str]) -> POI_suggestion:
    try:
        suggestion_name = poi_suggestion.get("suggestion_name")
        notes = poi_suggestion.get("notes")
        submission_time = datetime.now()
        submitted_by = poi_suggestion.get("submitted_by")
        if suggestion_name is None or submitted_by is None:
            raise InvalidPOISuggestionError("Invalid POI submission")
        return POI_suggestion(
            pid=pid,
            suggestion_name=suggestion_name,
            notes=notes,
            submitted_by=submitted_by,
            submission_time=submission_time,
        )
    except KeyError as e:
        raise common.BadDataError("Missing data from poi suggestion data: " + str(e))


def _fetch_latest_estimated_value(self):
    pass


def _generate_histogram_for_POI(self):
    pass

import haversine
from typing import Dict, Tuple, Iterable, Optional

from .poi_suggestion import POI_suggestion
from .poi import POI, POIClassification
from .errors import POINotFoundError, InvalidPOISuggestionError
from app import common
from datetime import datetime, timezone
from app.firebase import firestore_db, POI_COLLECTION, POI_PROPOSAL_COLLECTION


def poi_collection():
    return firestore_db().collection(POI_COLLECTION)


def poi_proposal_collection():
    return firestore_db().collection(POI_PROPOSAL_COLLECTION)


def list_POI(
    clazz: Optional[POIClassification] = None,
    user_location: Optional[Tuple[float, float]] = None,
) -> Iterable[POI]:
    """
    Returns an iterable of POI objects from the POI collection in Firestore.

    :param clazz: The class of POI to filter by
    :param user_location: The user's location to use to sort POIs by proximity.
    """
    query = poi_collection()
    if clazz:
        query = query.where("class", "==", clazz.value)
    query_results = query.stream()

    if user_location:

        def key_comparator(d):
            poi = d.to_dict()
            return _compute_geo_distance(
                user_location,
                (poi["location"]["latitude"], poi["location"]["longitude"]),
            )

        query_results = sorted(
            query_results,
            key=key_comparator,
        )

    return map(lambda d: POI.from_dict(d.to_dict()), query_results)


def get_details_for_POI(poi_id: str) -> POI:
    """
    Returns a POI object based on a given POI ID from the POI collction in Firestore.

    :param poi_id: ID of the POI
    """
    poi_data = poi_collection().document(poi_id).get()
    if not poi_data.exists:
        raise POINotFoundError(poi_id)
    return POI.from_dict(poi_data.to_dict())


def new_POI_suggestion(poi_suggestion: Dict[str, str]) -> POI_suggestion:
    """
    Saves a POI suggestion in the POI_proposal collection in firebase and returns
    the corresponding POI_suggection object

    :param poi_suggestion: A dictionary of the proposal to be made
    """
    poi_suggestion_ref = poi_proposal_collection().document()
    # Generate id for poi suggestion document
    pid = poi_suggestion_ref.id
    poi_suggestion["_pid"] = pid
    poi_suggestion_instance = POI_suggestion.from_dict(poi_suggestion)
    _save_POI_suggestion(poi_suggestion_instance, pid)
    return poi_suggestion_instance


def _save_POI_suggestion(
    poi_suggestion_instance: POI_suggestion, pid: str, merge: bool = True
) -> None:
    """
    Saves a POI suggestion in the POI_proposal collection in firebase.
    """
    target_ref = poi_proposal_collection().document(pid)
    target_ref.set(poi_suggestion_instance.to_dict(), merge=merge)


def _create_POI_suggestion(pid: str, poi_suggestion: Dict[str, str]) -> POI_suggestion:
    """
    Creates a POI_suggestion object.

    :param pid: The generated pid of the POI suggestion to be added
    :param poi_suggestion: Dictionary of the proposal made
    """
    try:
        suggestion_name = poi_suggestion.get("suggestion_name")
        notes = poi_suggestion.get("notes")
        submission_time = datetime.now(timezone.utc)
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


def _compute_geo_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Computes the distance in meters between two points on the earth's surface using the
    Haversine formula.

    :param p1: A tuple of the latitude and longitude of the first point
    :param p2: A tuple of the latitude and longitude of the second point
    """
    return haversine.haversine(p1, p2, unit=haversine.Unit.METERS)

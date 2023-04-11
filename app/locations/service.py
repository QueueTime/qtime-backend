import haversine
from typing import Dict, Tuple, Iterable, Optional, List, Any
import math
import pytz
from random import random

from .poi_suggestion import POI_suggestion
from .poi import POI, POIClassification, Histogram
from .errors import POINotFoundError, InvalidPOISuggestionError
from app import common
from datetime import datetime, timezone
from app.firebase import (
    firestore_db,
    POI_COLLECTION,
    POI_PROPOSAL_COLLECTION,
    HISTOGRAM_COLLECTION,
)


def poi_collection():
    return firestore_db().collection(POI_COLLECTION)


def poi_proposal_collection():
    return firestore_db().collection(POI_PROPOSAL_COLLECTION)


def histogram_collection():
    return firestore_db().collection(HISTOGRAM_COLLECTION)


def list_POI(
    user_location: Tuple[float, float],
    classification: Optional[POIClassification] = None,
    sort_by: Optional[str] = None,
) -> List[Tuple[POI, float, float, float]]:
    """
    Compute an iterable of (POI, estimate, distance, last_updated) computed from the POI collection in Firestore.

    :param clazz: The class of POI to filter by
    :param user_location: The user's location to use to sort POIs by proximity.
    :param sort_by: The field to sort the iterable by. Allowed values are "distance" and "estimate"
    :return: An iterable of (POI, estimate, distance, last_updated) tuples
    """
    query = poi_collection()
    if classification:
        query = query.where("class", "==", classification.value)

    def compute_query_results(d):
        poi = d.to_dict()
        # TODO: Compute the estimate (time or capacity) for each POI
        SAMPLE_ESTIMATE = fetch_latest_estimated_value(poi["_id"], poi["class"])
        # TODO: Compute the last_updated value for each POI
        SAMPLE_LAST_UPDATED = 3
        user_distance = _compute_geo_distance(
            user_location,
            (poi["location"]["latitude"], poi["location"]["longitude"]),
        )
        return (POI.from_dict(poi), SAMPLE_ESTIMATE, user_distance, SAMPLE_LAST_UPDATED)

    query_results = list(map(compute_query_results, query.stream()))

    if sort_by == "distance":
        query_results = sorted(
            query_results,
            key=lambda x: x[2],  # sort by distance
        )
    elif sort_by == "estimate":
        query_results = sorted(
            query_results, key=lambda x: x[1]
        )  # sort by estimate (time or capacity)

    return query_results


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


def get_distance_to_POI(poi: POI, user_location: Tuple[float, float]) -> float:
    """
    Computes the distance in meters between the given POI and the user's location.

    :param poi: The POI to compute the distance to
    :param user_location: The user's location to compute the distance from
    """
    return _compute_geo_distance(
        user_location, (poi.location["latitude"], poi.location["longitude"])
    )


def _compute_geo_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Computes the distance in meters between two points on the earth's surface using the
    Haversine formula.

    :param p1: A tuple of the latitude and longitude of the first point
    :param p2: A tuple of the latitude and longitude of the second point
    """
    return haversine.haversine(p1, p2, unit=haversine.Unit.METERS)


def generate_histogram_for_POI(poi_name: str, day: str = "") -> List[Any]:
    """
    Returns the histogram of the wait time/occupancy for opening hours for a specified POI

    :param poi_name: Name of the point of interest (also known as the POI id)
    :param day: Specific day to get the wait time/occupancy histogram from (Optional)
    """
    histogram_instance = histogram_for_POI(poi_name)
    histogram = histogram_instance.to_dict()
    histogram_data = histogram["histogram_data"]

    est = pytz.timezone("US/Eastern")
    if day == "":
        day = datetime.now().astimezone(est).strftime("%A")

    if day not in histogram_data:
        return [{"time": 0, "estimate": 0}]

    return list(
        sorted(
            (
                {"time": int(t), "estimate": histogram_data[day]["hours"][t]}
                for t in histogram_data[day]["hours"]
            ),
            key=lambda x: x["time"],
        )
    )


def fetch_latest_estimated_value(
    poi_name: str,
    classification: str,
    day: str = "",
    current_hour: int = 0,
    current_minute: int = 0,
) -> int:
    """
    Returns the estimated wait time/occupancy of a specified POI

    :param poi_name: Name of the point of interest (also known as the POI id)
    :param day: Specific day to get the wait time/occupancy histogram from (Optional)
    :param current_hour: The hours of the day in 24hr format (Optional)
    :param current_minute: The minute of the day (Optional)
    """
    wait_time_estimate = 0
    # histogram_instance = histogram_for_POI(poi_name)
    # histogram_dict = histogram_instance.to_dict()
    # histogram_data = histogram_dict["histogram_data"]

    est = pytz.timezone("US/Eastern")
    now = datetime.now().astimezone(est)

    if day == "":
        day = now.strftime("%A")

    if current_hour == 0:
        current_hour = int(now.strftime("%H"))
    if current_minute == 0:
        current_minute = int(now.strftime("%M"))

    try:
        histogram_hourly_data = (
            histogram_collection()
            .document(poi_name)
            .collection("histogram_data")
            .document(day)
            .get()
            .to_dict()["hours"]
        )
    except Exception as e:
        return wait_time_estimate

    # if day not in histogram_data:
    #     return wait_time_estimate

    # histogram_hourly_data = histogram_data[day]["hours"]

    if str(current_hour) in histogram_hourly_data:
        wait_time_estimate = histogram_hourly_data[str(current_hour)]
    else:
        return wait_time_estimate

    # poi_class = histogram_dict["class"]
    # For wait time queue
    if classification == "queue":
        # Add 5 minutes to queue time during peak times
        if current_minute >= 20 and current_minute <= 30:
            wait_time_estimate += 5
    if classification == "occupancy":
        # Add 10% to occupancy during peak times
        if current_minute >= 20 and current_minute <= 30:
            wait_time_estimate += 10

    return wait_time_estimate


# Create histogram object
def histogram_for_POI(poi_id: str) -> Histogram:
    """
    Returns the Histogram object of the wait time/occupancy for opening hours for a specified POI

    :param poi_name: Name of the point of interest (also known as the POI id)
    """
    # Getting information from histogram base collection
    histogram_base_ref = histogram_collection().document(poi_id)
    histogram_base_doc = histogram_base_ref.get()
    if not histogram_base_doc.exists:
        raise POINotFoundError(poi_id)
    histogram_base_doc_dict = histogram_base_doc.to_dict()
    poi_name = histogram_base_doc_dict["poi_name"]
    class_type = histogram_base_doc_dict["class"]

    # Getting histogram data for each day for a poi
    histogram_docs = (
        histogram_collection().document(poi_id).collection("histogram_data").stream()
    )
    histogram_data_dict = {
        doc.to_dict()["day"]: doc.to_dict() for doc in histogram_docs
    }

    histogram_dict = {
        "poi_name": poi_name,
        "class": class_type,
        "histogram_data": histogram_data_dict,
    }

    return Histogram.from_dict(histogram_dict)

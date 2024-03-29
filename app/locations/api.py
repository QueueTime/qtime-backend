from flask import jsonify
from typing import Dict, Any, Optional, List
import math
from random import random, randint

from app.auth import with_auth_user
from app.user.user import User
from app.base_api_error import MissingQueryParameterError
from .poi import POIClassification, POI
from .service import (
    list_POI,
    get_details_for_POI,
    new_POI_suggestion,
    get_distance_to_POI,
    generate_histogram_for_POI,
    fetch_latest_estimated_value,
)


def _build_POI_api_model(
    poi: POI, estimate: float, distance: float, last_updated: float
) -> Dict[str, Any]:
    """
    Build a model to be returned by the POI api. Extends the POI dictionary with additional fields.
    """
    return {
        "_id": poi.id,
        "name": poi.name,
        "type": poi.poi_type,
        "class": poi.classification.value,
        "location": poi.location,
        "estimate": estimate,
        "distance": distance,
        "lastUpdated": last_updated,
    }


def _build_POI_details_api_response(
    poi: POI,
    estimate: float,
    distance: float,
    last_updated: float,
    histogram: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Build the dictionary to return as JSON for the POI details API endpoint.
    Extends the POI to_dict() with the distance, estimate, lastUpdated and histogram fields.
    """
    d = {
        "histogram": histogram,
        "distance": distance,
        "estimate": estimate,
        "lastUpdated": last_updated,
        "hoursOfOperation": poi.hours_of_operation,
        "imageUrl": poi.image_url,
        **poi.to_dict(),
    }
    del d["hours_of_operation"]  # remove hours_of_operation (incorrect naming)
    del d["image_url"]  # remove image_url (incorrect naming)
    return d


@with_auth_user
def get_all_POI(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    sort: Optional[str] = None,
    **kwargs
):
    """
    Return a list of all the tracked points of interests. Requires the geo coordinates of the user's location.
    Allows filtering by POI class and sorting by distance or estimate.
    """
    if latitude is None:
        raise MissingQueryParameterError("latitude")
    elif longitude is None:
        raise MissingQueryParameterError("longitude")

    user_location = (latitude, longitude)

    class_filter = kwargs.get("class", None)
    if class_filter:
        class_filter = POIClassification(class_filter)
    list_all_poi = list_POI(user_location, classification=class_filter, sort_by=sort)
    return (
        jsonify(
            [
                _build_POI_api_model(poi, estimate, distance, last_updated)
                for poi, estimate, distance, last_updated in list_all_poi
            ]
        ),
        200,
    )


@with_auth_user
def get_POI_details(
    poi_id: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    **kwargs
):
    """
    Returns the details of a single point of interest.

    :param poi_id: The id of the point of interest
    :param latitude: The latitude of the user's location
    :param longitude: The longitude of the user's location
    """
    if latitude is None:
        raise MissingQueryParameterError("latitude")
    elif longitude is None:
        raise MissingQueryParameterError("longitude")
    user_location = (latitude, longitude)

    poi = get_details_for_POI(poi_id)
    distance = get_distance_to_POI(poi, user_location)
    # TODO: Compute the estimate (time or capacity)
    SAMPLE_ESTIMATE = fetch_latest_estimated_value(poi_id, poi.classification.value)
    # TODO: Compute the last_updated value
    SAMPLE_LAST_UPDATED = 3
    # TODO: Compute the histogram values that match this format
    SAMPLE_HISTOGRAM = generate_histogram_for_POI(poi_id)

    return (
        jsonify(
            _build_POI_details_api_response(
                poi,
                SAMPLE_ESTIMATE,
                distance,
                SAMPLE_LAST_UPDATED,
                SAMPLE_HISTOGRAM,
            )
        ),
        200,
    )


@with_auth_user
def suggest_new_POI(poi_suggestion: Dict[str, str], user: User, **kwargs):
    """
    Save a POI suggestion to the poi_proposal collection in Firestore.

    :param poi_suggestion: Suggestion to be saved
    :param user: User object of the user who submitted the suggestion
    """
    poi_suggestion["submitted_by"] = user.email
    new_POI_suggestion(poi_suggestion)
    return None, 204

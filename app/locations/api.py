from .service import list_POI, get_details_for_POI, new_POI_suggestion
from flask import jsonify
from typing import Dict
from app.auth import with_auth_user
from app.user.user import User
from app.base_api_error import MissingQueryParameterError
from .poi import POIClassification, POI


def _build_POI_api_model(
    poi: POI, estimate: float, distance: float, last_updated: float
) -> Dict[str, str]:
    """
    Build a model to be returned by the POI api. Extends the POI dictionary with additional fields.
    """
    return {
        "estimate": estimate,
        "distance": distance,
        "lastUpdated": last_updated,
        **poi.to_dict(),
    }


@with_auth_user
def get_all_POI(**kwargs):
    """
    Return a list of all the tracked points of interests. Requires the geo coordinates of the user's location.
    Allows filtering by POI class and sorting by distance or estimate.
    """
    lat, long = kwargs.get("latitude"), kwargs.get("longitude")

    if lat is None:
        raise MissingQueryParameterError("latitude")
    elif long is None:
        raise MissingQueryParameterError("longitude")

    user_location = (lat, long)

    class_filter = POIClassification(kwargs.get("class"), None)
    sort_by = kwargs.get("sort", None)
    list_all_poi = list_POI(user_location, clazz=class_filter, sort_by=sort_by)
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
def get_POI(poi_id: str, **kwargs):
    """
    Returns the details of a single point of interest.

    :param poi_id: The id of the point of interest
    """
    get_poi = get_details_for_POI(poi_id)
    return jsonify(get_poi.to_dict()), 200


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

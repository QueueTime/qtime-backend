from .service import list_POI, get_details_for_POI, new_POI_suggestion
from flask import jsonify
from .errors import POINotFoundError, InvalidPOISuggestionError
from typing import Dict
from app.auth import with_auth_user
from app.user.user import User


@with_auth_user
def get_all_POI(**kwargs):
    """
    Return a list of all the tracked points of interests.
    """
    try:
        list_all_poi = list_POI()
        return jsonify([poi.to_dict() for poi in list_all_poi]), 200
    except Exception as e:
        return {"error": str(e)}, 500


@with_auth_user
def get_POI(poi_id: str, **kwargs):
    """
    Returns the details of a single point of interest.

    :param poi_id: The id of the point of interest
    """
    try:
        get_poi = get_details_for_POI(poi_id)
        return jsonify(get_poi.to_dict()), 200
    except POINotFoundError as e:
        return e.build_error()
    except Exception as e:
        return {"error": str(e)}, 500


@with_auth_user
def suggest_new_POI(poi_suggestion: Dict[str, str], user: User, **kwargs):
    """
    Save a POI suggestion to the poi_proposal collection in Firestore.

    :param poi_suggestion: Suggestion to be saved
    :param user: User object of the user who submitted the suggestion
    """
    try:
        poi_suggestion["submitted_by"] = user.email
        suggestion = new_POI_suggestion(poi_suggestion)
        return None, 204
    except InvalidPOISuggestionError as e:
        return e.build_error()
    except Exception as e:
        return {"error": str(e)}, 500

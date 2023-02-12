from .service import list_POI, get_details_for_POI, new_POI_suggestion
from flask import jsonify
from .errors import POINotFoundError, InvalidPOISuggestionError
from typing import Dict

# TODO Exception handling
# TODO type hints
def get_all_POI():
    try:
        list_all_poi = list_POI()
        return jsonify([poi.to_dict() for poi in list_all_poi]), 200
    except Exception as e:
        return {"error": str(e)}, 500


def get_POI(poi_id: str):
    try:
        get_poi = get_details_for_POI(poi_id)
        return jsonify(get_poi.to_dict()), 200
    except POINotFoundError as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 500


def suggest_new_POI(poi_suggestion: Dict[str, str]):
    try:
        suggestion = new_POI_suggestion(poi_suggestion)
        return None, 204
    except InvalidPOISuggestionError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500

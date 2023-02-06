from .poi_service import POI_Service
from flask import jsonify
from .poi_errors import POINotFoundError, InvalidPOISuggestionError

poi_service_class = POI_Service()

# TODO Exception handling
# TODO type hints
def get_all_POI():
    try:
        list_all_poi = poi_service_class.get_all_POI()
        return jsonify([poi.to_dict() for poi in list_all_poi]), 200
    except Exception as e:
        return {"error": str(e)}, 500


def get_POI(poi_id):
    try:
        get_poi = poi_service_class.get_POI(poi_id)
        return jsonify(get_poi.to_dict()), 200
    except POINotFoundError as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 500


def suggest_new_POI(poi_suggestion):
    try:
        return poi_service_class.suggest_new_POI(poi_suggestion)
    except InvalidPOISuggestionError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500

from .poi_service import POI_Service
from flask import jsonify
from .poi_errors import POINotFoundError, InvalidPOISuggestionError

poi_service_class = POI_Service()

# TODO Exception handling
# TODO type hints
def get_all_POI():
    try:
        list_all_poi = poi_service_class.get_all_POI()
        return [poi.to_dict() for poi in list_all_poi], 200
    except Exception as e:
        return {"success": False, "message": str(e), "error_code": 400}, 400


def get_POI(poi_id):
    try:
        get_poi = poi_service_class.get_POI(poi_id)
        return get_poi.to_dict(), 200
    except POINotFoundError as e:
        return {"success": False, "message": str(e), "error_code": 404}, 404
    except Exception as e:
        return {"success": False, "message": str(e), "error_code": 404}, 404


def suggest_new_POI(poi_suggestion):
    try:
        return poi_service_class.suggest_new_POI(poi_suggestion), 200
    except InvalidPOISuggestionError as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400}), 400
    except Exception as e:
        return {"success": False, "message": str(e), "error_code": 400}, 400

from .poi_service import POI_Service
from flask import jsonify
from .poi_errors import POINotFoundError, InvalidPOISuggestionError

poi_service_class = POI_Service()

# TODO Exception handling
# TODO type hints
def get_all_POI():
    try:
        get_all_POI_reponse = poi_service_class.get_all_POI()
        list_all_poi = get_all_POI_reponse[0]
        get_all_poi_status = get_all_POI_reponse[1]
        if get_all_poi_status == 200:
            return [poi._to_dict() for poi in list_all_poi]
        else:
            return jsonify(
                {
                    "success": False,
                    "message": "POI list could not be retrieved.",
                    "error_code": get_all_poi_status,
                }
            )
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400})


def get_POI(poi_id):
    try:
        get_poi = poi_service_class.get_POI(poi_id)
        poi = get_poi[0]
        get_poi_status = get_poi[1]
        if get_poi_status == 200:
            return poi._to_dict()
        else:
            return jsonify({"success": False, "error_code": get_poi_status})
    except POINotFoundError as e:
        return jsonify({"success": False, "message": str(e), "error_code": 404})


def suggest_new_POI(poi_suggestion):
    try:
        return poi_service_class.suggest_new_POI(poi_suggestion)
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400})

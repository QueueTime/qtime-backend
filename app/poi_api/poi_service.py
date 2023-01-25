from app import firestore_db
from flask import jsonify
from .poi_api import POIApi


class POI_Service(POIApi):
    def get_all_POI(self):
        try:
            poi_ref = firestore_db.collection("POI")
            all_poi = [doc.to_dict() for doc in poi_ref.stream()]
            return jsonify(all_poi), 200
        except Exception as e:
            return f"An Error Occured: {e}", 404

    def get_POI(self, poi_id):
        try:
            poi_ref = firestore_db.collection("POI")
            poi = poi_ref.document(poi_id).get()
            poi_dict = poi.to_dict()
            if poi_dict is not None:
                return jsonify(poi.to_dict()), 200
            else:
                return f"POI with id: {poi_id}, does not exist", 404

        except Exception as e:
            return f"An Error Occured: {e}"

    def suggest_new_POI(self):
        pass

    def _save_POI_suggestion(self):
        pass

    def _fetch_latest_estimated_value(self):
        pass

    def _generate_histogram_for_POI(self):
        pass

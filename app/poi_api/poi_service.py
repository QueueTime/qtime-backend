from app import firestore_db
from flask import jsonify
from .poi_api import POIApi
from .poi_suggestion import POI_suggestions
from .poi import POI
from .poi_errors import POINotFoundError, InvalidPOISuggestionError
from datetime import datetime


class POI_Service(POIApi):
    def get_all_POI(self):
        try:
            poi_ref = firestore_db.collection("POI")
            all_poi = [doc.to_dict() for doc in poi_ref.stream()]
            list_all_poi = list()
            for poi in all_poi:
                poi_object = self._create_poi_object(poi)
                list_all_poi.append(poi_object)
            return list_all_poi, 200
        except Exception as e:
            raise Exception(f"An error occured: {e}")

    def get_POI(self, poi_id):
        try:
            poi_ref = firestore_db.collection("POI")
            poi = poi_ref.document(poi_id).get()
            poi_dict = poi.to_dict()
            if poi_dict is not None:
                return self._create_poi_object(poi_dict), 200
            else:
                raise Exception(f"The POI with the id: {poi_id} could not be found")
        except Exception as e:
            raise POINotFoundError(f"{e}", 404)

    def suggest_new_POI(self, poi_suggestion):
        try:
            poi_suggestion_ref = firestore_db.collection("POI_proposal").document()
            pid = poi_suggestion_ref.id
            poi_suggestion_instance = self._create_POI_suggestion(pid, poi_suggestion)
            return self._save_POI_suggestion(
                poi_suggestion_instance, poi_suggestion_ref
            )
        except Exception as e:
            error_code = 400
            raise InvalidPOISuggestionError(f"Invalid POI submission: {e}", error_code)

    # TODO: Add User parameter
    # TODO: Create user object for submitted_by
    def _create_POI_suggestion(self, pid, poi_suggestion):
        try:
            suggestion_name = poi_suggestion.get("suggestion_name")
            notes = poi_suggestion.get("notes")
            submission_time = datetime.now()
            submitted_by = poi_suggestion.get("submitted_by")
            return POI_suggestions(
                pid, suggestion_name, notes, submission_time, submitted_by
            )
        except Exception as e:
            raise Exception(f"An error occured: {e}")

    def _save_POI_suggestion(self, poi_suggestion_instance, poi_suggestion_ref) -> str:
        try:
            poi_suggestion_dict = poi_suggestion_instance.to_dict()
            # Retrieves key from push
            poi_suggestion_post_ref = poi_suggestion_ref.set(
                poi_suggestion_dict, merge=True
            )
            return poi_suggestion_post_ref
        except Exception as e:
            raise Exception(f"An error occured: {e}")

    def _create_poi_object(self, poi):
        try:
            _id = poi["_id"]
            name = poi["name"]
            clasification = poi["class"]
            hours_of_operation = poi["hours_of_operation"]
            address = poi["address"]
            poi_type = poi["type"]
            location = poi["location"]
            image_url = poi["image_url"]
            return POI(
                _id,
                name,
                clasification,
                hours_of_operation,
                address,
                poi_type,
                location,
                image_url,
            )
        except Exception as e:
            raise Exception(f"An error occured: {e}")

    def _fetch_latest_estimated_value(self):
        pass

    def _generate_histogram_for_POI(self):
        pass

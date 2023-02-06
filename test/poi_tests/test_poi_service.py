import unittest
from app.poi_api.poi_service import POI_Service
from app.poi_api.poi_suggestion import POI_suggestions
from app.poi_api.poi_errors import POINotFoundError, InvalidPOISuggestionError
from firebase_admin import credentials, initialize_app, firestore


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cred = credentials.Certificate("app/key/serviceAccountKey.json")
        self.firestore_db = firestore.client()
        self.poi_ref = self.firestore_db.collection("POI")
        self.poi_sug_ref = self.firestore_db.collection("POI_proposal")
        self.poi_service = POI_Service()
        self.poi_suggestion = {
            "suggestion_name": "TEST",
            "notes": "Test case",
            "submitted_by": "P-body and Atlas",
        }
        self.poi_suggestion_id = "0"

    def test_get_all_poi(self):
        poi_obj_list = self.poi_service.get_all_POI()
        all_poi_db = [doc.to_dict() for doc in self.poi_ref.stream()]
        self.assertEqual([poi.to_dict() for poi in poi_obj_list], all_poi_db)

    def test_get_all_poi_exception(self):
        with self.assertRaises(Exception):
            poi_obj_list = self.poi_service.get_all_POI()
            all_poi_db = [doc.to_dict() for doc in self.poi_sug_ref.stream()]
            self.assertEqual([poi.to_dict() for poi in poi_obj_list], all_poi_db)

    def test_get_POI(self):
        poi_id = "tim_hortons_musc"
        poi = self.poi_service.get_POI(poi_id).to_dict()
        poi_db = self.poi_ref.document(poi_id).get().to_dict()
        self.assertEqual(poi, poi_db)

    def test_get_POI_POINotFoundError(self):
        with self.assertRaises(POINotFoundError):
            poi_id = "tim_hortons_bsb"
            poi = self.poi_service.get_POI(poi_id).to_dict()
            poi_db = self.poi_ref.document(poi_id).get().to_dict()
            self.assertEqual(poi, poi_db)

    # TODO: Update test as ID is no longer returned
    # Testing that poi suggestion has been added to the data base by checking matching id
    # def test_suggest_new_POI(self):
    #     poi_suggestion_id = self.poi_service.suggest_new_POI(self.poi_suggestion)[
    #         "poi_suggestion_id"
    #     ]
    #     self.poi_suggestion_id = poi_suggestion_id
    #     get_poi_suggestion = (
    #         self.poi_sug_ref.document(poi_suggestion_id).get().to_dict()
    #     )
    #     self.assertEqual(self.poi_suggestion_id, get_poi_suggestion["_pid"])

    # def test_suggest_new_POI_InvalidPOISuggestionError(self):
    #     with self.assertRaises(InvalidPOISuggestionError):
    #         poi_suggestion_error = {
    #             "submitted_by": "P-body and Atlas",
    #         }
    #         self.poi_service.suggest_new_POI(poi_suggestion_error)

    def tearDown(self):
        self.poi_sug_ref.document(self.poi_suggestion_id).delete()

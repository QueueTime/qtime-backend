import unittest
from app.poi_api.poi_service import POI_Service
from firebase_admin import credentials, initialize_app, firestore


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cred = credentials.Certificate("app/key/serviceAccountKey.json")
        self.firestore_db = firestore.client()
        self.poi_ref = self.firestore_db.collection("POI")
        self.poi_service = POI_Service()

    def test_get_all_poi(self):
        poi_obj_list = self.poi_service.get_all_POI()
        all_poi_db = [doc.to_dict() for doc in self.poi_ref.stream()]
        self.assertEquals([poi._to_dict() for poi in poi_obj_list])

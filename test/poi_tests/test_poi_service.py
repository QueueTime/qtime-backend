import unittest
from firebase_admin import credentials, firestore
from app.poi_api.poi_service import get_all_POI
from flask import jsonify, Flask
import json


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cred = credentials.Certificate("app/key/serviceAccountKey.json")
        # default_app = initialize_app(cred)     (not needed when running unittest)
        self.firestore_db = firestore.client()
        self.poi_ref = self.firestore_db.collection("POI")
        self.poi_suggestion_ref = self.firestore_db.collection("POI_proposal")
        app = Flask(__name__)
        app.app_context()

    def test_get_all_poi(self):
        app = Flask(__name__)
        with app.app_context():
            valid_poi_ids = ["tim_hortons_musc"]
            poi_list = get_all_POI()
            print(poi_list)


if __name__ == "__main__":
    unittest.main()

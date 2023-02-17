import unittest
from app.user.user import User
from app.firebase import firestore_db, LOCATION_COLLECTION, POI_COLLECTION
import json
from app.locations.poi import POI

from test.mixins.flask_client_mixin import FlaskTestClientMixin
from test.mixins.firebase_mixin import FirebaseTestMixin


class TestWaitTimeApi(unittest.TestCase, FlaskTestClientMixin, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        self.with_test_flask_client(self)
        self.with_rest_defaults(self)

    def setUp(self):
        self.test_user = User("test@sample.com")
        self.with_user_accounts(self.test_user)
        self.location_request_body = {
            "latitude": 43.263532187492686,
            "longitude": -79.91758503073444,
        }
        # Sample POI
        self.sample_poi = POI(
            id="tim_hortons_musc",
            name="Tim Hortons MUSC",
            classification="queue",
            hours_of_operation={
                "Sunday": "Closed",
                "Monday": "7:30 AM - 9:00 PM",
                "Tuesday": "7:30 AM - 9:00 PM",
                "Wednesday": "7:30AM - 9:00 PM",
                "Thursday": "7:30 AM - 9:00 PM",
                "Friday": "7:30 AM - 8:00 PM",
                "Saturday": "Closed",
            },
            address="McMaster University Student Centre",
            poi_type="EATERY",
            location={
                "latitude": 43.263532187492686,
                "longitude": -79.91758503073444,
            },
            image_url="https://discover.mcmaster.ca/app/uploads/2019/06/Booster-Juice.jpg",
        )
        firestore_db().collection(POI_COLLECTION).document(self.sample_poi.id).set(
            self.sample_poi.to_dict()
        )

    def tearDown(self):
        self.delete_user_accounts()
        self.clear_all_firestore_data()

    def test_update_user_location(self):
        response = self.client.post(
            f"{self.base_url}/user/location",
            json=self.location_request_body,
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 204)
        # Check if location collection is not empty
        self.assertTrue(firestore_db().collection(LOCATION_COLLECTION).limit(1).get())

    def test_update_user_location_bad_body(self):
        response = self.client.post(
            f"{self.base_url}/user/location",
            json={"latitude": 34234},
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_user_estimate(self):
        response = self.client.post(
            f"{self.base_url}/places/tim_hortons_musc/estimate",
            json={"wait_time_estimate": 5323},
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 204)

    def test_submit_user_estimate_bad_body(self):
        response = self.client.post(
            f"{self.base_url}/places/tim_hortons_musc/estimate",
            json={"invalid_param": 5323},
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_user_estimate_bad_estimate(self):
        response = self.client.post(
            f"{self.base_url}/places/tim_hortons_musc/estimate",
            json={"wait_time_estimate": -2},
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_user_estimate_invalid_poi_id(self):
        response = self.client.post(
            f"{self.base_url}/places/invalid_name/estimate",
            json={"wait_time_estimate": 5323},
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 404)

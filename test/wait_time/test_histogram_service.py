import unittest
from unittest.mock import patch, Mock
from test.mixins.firebase_mixin import FirebaseTestMixin

from datetime import datetime, timezone, timedelta
from app.firebase import firestore_db
from app.user.user import User
from app.wait_time.location import UserLocation
from app.locations.poi import POI, POIClassification
from app.locations.service import (
    poi_collection,
    histogram_for_POI,
    generate_histogram_for_POI,
    fetch_latest_estimated_value,
)


class TestWaitTimeComputation(unittest.TestCase, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)

    def setUp(self):
        self.poi_id = "tim_hortons_musc"
        self.poi_id_occ = "centro"
        self.sample_histogram = {
            "poi_name": "tim_hortons_musc",
            "class": "queue",
            "histogram_data": {
                "Sunday": {
                    "day": "Sunday",
                    "poi_name": "tim_hortons_musc",
                    "hours": {"1": 1, "2": 2},
                },
                "Monday": {
                    "day": "Monday",
                    "poi_name": "tim_hortons_musc",
                    "hours": {"2": 2},
                },
            },
        }
        self.sample_histogram_occupancy = {
            "poi_name": "centro",
            "class": "occupancy",
            "histogram_data": {
                "Sunday": {
                    "day": "Sunday",
                    "poi_name": "centro",
                    "hours": {"1": 10, "4": 90},
                }
            },
        }
        self.sample_generate_histogram_for_POI = [
            {"time": 1, "estimate": 1},
            {"time": 2, "estimate": 2},
        ]
        self.sample_generate_histogram_for_POI_occupancy = [
            {"time": 4, "estimate": 90},
            {"time": 1, "estimate": 10},
        ]
        self.sample_wait_time_estimate = 1
        self.sample_wait_time_estimate_peak = 6
        self.sample_wait_time_estimate_occ = 10
        self.sample_wait_time_estimate_peak_occ = 20

    def tearDown(self):
        pass

    def test_histogram_for_POI_queue(self):
        self.maxDiff = None
        histogram_instace = histogram_for_POI(self.poi_id)
        self.assertDictEqual(histogram_instace.to_dict(), self.sample_histogram)

    def test_histogram_for_POI_occupancy(self):
        self.maxDiff = None
        histogram_instace = histogram_for_POI(self.poi_id_occ)
        self.assertDictEqual(
            histogram_instace.to_dict(), self.sample_histogram_occupancy
        )

    def test_generate_histogram_for_POI_queue(self):
        self.maxDiff = None
        self.assertListEqual(
            generate_histogram_for_POI(self.poi_id, "Sunday"),
            self.sample_generate_histogram_for_POI,
        )

    def test_generate_histogram_for_POI_occupancy(self):
        self.maxDiff = None
        self.assertEqual(
            generate_histogram_for_POI(self.poi_id_occ, "Sunday"),
            self.sample_generate_histogram_for_POI_occupancy,
        )

    def test_fetch_latest_estimated_value_queue(self):
        self.assertEqual(
            fetch_latest_estimated_value(self.poi_id, "Sunday", 1, 10),
            self.sample_wait_time_estimate,
        )

    def test_fetch_latest_estimated_value_peak_queur(self):
        self.assertEqual(
            fetch_latest_estimated_value(self.poi_id, "Sunday", 1, 25),
            self.sample_wait_time_estimate_peak,
        )

    def test_fetch_latest_estimated_value_occupancy(self):
        self.assertEqual(
            fetch_latest_estimated_value(self.poi_id_occ, "Sunday", 1, 10),
            self.sample_wait_time_estimate_occ,
        )

    def test_fetch_latest_estimated_value_peak_occupancy(self):
        self.assertEqual(
            fetch_latest_estimated_value(self.poi_id_occ, "Sunday", 1, 25),
            self.sample_wait_time_estimate_peak_occ,
        )

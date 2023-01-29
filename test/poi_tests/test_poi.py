# run with: python -m unittest test/poi_tests/test_poi.py
import unittest
from app.poi_api.poi import POI


class TestPOI(unittest.TestCase):
    def test_to_dict(self):
        poi = POI(
            _id="0",
            name="test",
            clasification="TEST",
            hours_of_operation={"Monday": "11:00"},
            address="123 McMaster",
            poi_type="test",
            location={"longitude": "0", "latitude": "0"},
            image_url="picture",
        )
        poi_dict = {
            "_id": "0",
            "name": "test",
            "class": "TEST",
            "hours_of_operation": {"Monday": "11:00"},
            "address": "123 McMaster",
            "type": "test",
            "location": {"longitude": "0", "latitude": "0"},
            "image_url": "picture",
        }
        self.assertEqual(poi._to_dict(), poi_dict)

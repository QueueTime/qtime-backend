import unittest
from app.locations.poi import POI


class TestPOI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.poi = POI(
            _id="0",
            name="test",
            clasification="TEST",
            hours_of_operation={"Monday": "11:00"},
            address="123 McMaster",
            poi_type="test",
            location={"longitude": "0", "latitude": "0"},
            image_url="picture",
        )

    def test_to_dict(self):
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
        self.assertEqual(self.poi.to_dict(), poi_dict)

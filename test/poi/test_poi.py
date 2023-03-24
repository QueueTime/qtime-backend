import unittest
from app.locations.poi import POI


class TestPOI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.poi = POI(
            id="0",
            name="test",
            classification="queue",
            hours_of_operation={"Monday": "11:00"},
            address="123 McMaster",
            poi_type="test",
            location={"longitude": "0", "latitude": "0"},
            image_url="picture",
        )
        self.poi_dict = {
            "_id": "0",
            "name": "test",
            "class": "queue",
            "hoursOfOperation": {"Monday": "11:00"},
            "address": "123 McMaster",
            "type": "test",
            "location": {"longitude": "0", "latitude": "0"},
            "image_url": "picture",
        }

    def test_to_dict(self):
        self.assertEqual(self.poi.to_dict(), self.poi_dict)

    def test_from_dict(self):
        self.assertEqual(self.poi, POI.from_dict(self.poi_dict))

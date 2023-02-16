import unittest
from app.wait_time.location import Location
from datetime import datetime, timezone


class TestLocation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        current_datetime = datetime.now(timezone.utc)
        self.sample_location = Location(
            "abcd1234", 43.263532187492686, -79.91758503073444, current_datetime
        )
        self.sample_dict = {
            "aid": "abcd1234",
            "latitude": 43.263532187492686,
            "longitude": -79.91758503073444,
            "timestamp": current_datetime,
        }

    def test_to_from_dict(self):
        self.assertEqual(
            self.sample_location,
            Location.from_dict("abcd1234", self.sample_dict),
        )

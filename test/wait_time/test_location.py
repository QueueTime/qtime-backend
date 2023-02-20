import unittest
from app.wait_time.location import UserLocation
from datetime import datetime, timezone
from app.common import BadDataError


class TestLocation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        current_datetime = datetime.now(timezone.utc)
        self.sample_location = UserLocation(
            "abcd1234", 43.263532187492686, -79.91758503073444, current_datetime
        )
        self.sample_dict = {
            "aid": "abcd1234",
            "latitude": 43.263532187492686,
            "longitude": -79.91758503073444,
            "timestamp": current_datetime,
        }

        self.bad_latitude_dict = {"latitude": 91.22323, "longitude": -79.91758503073444}

        self.bad_longitude_dict = {
            "latitude": 43.263532187492686,
            "longitude": -181.0323423423,
        }

    def test_to_from_dict(self):
        self.assertEqual(
            self.sample_location,
            UserLocation.from_dict("abcd1234", self.sample_dict),
        )

    def test_from_dict_bad_location(self):
        self.assertRaises(
            BadDataError, UserLocation.from_dict, "abcd1234", self.bad_latitude_dict
        )
        self.assertRaises(
            BadDataError, UserLocation.from_dict, "abcd1234", self.bad_longitude_dict
        )

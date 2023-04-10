import unittest
from unittest.mock import patch, Mock
from app.user.user import User

from app.wait_time import service as wait_time_service
from app.wait_time.location import UserLocation
from app.locations.poi import POI

SAMPLE_UID = "2Nc3UKvI98YvhTlud9ZEomZHr9p2"


@patch("app.wait_time.service.location_collection")
class TestWaitTimeService(unittest.TestCase):
    """Test the Wait Time service"""

    @classmethod
    def setUpClass(self):
        self.test_user = User("test@sample.com")
        self.test_location = UserLocation(
            aid=SAMPLE_UID, latitude=43.263532187492686, longitude=-79.91758503073444
        )
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

    def test_uid_to_aid(self, mock_location_collection):
        self.assertTrue(len(wait_time_service.uid_to_aid(SAMPLE_UID)) > 0)

    def test_update_location(self, mock_location_collection):
        wait_time_service.update_location(self.test_location)
        mock_location_collection().document().set.assert_called_once()

    @patch("app.wait_time.service.generate_waittime_submit_event")
    @patch("app.wait_time.service.get_details_for_POI")
    def test_add_wait_time_suggestion(
        self, mock_get_poi_func, mock_waittime_submit_func, mock_location_collection
    ):
        mock_get_poi_func.return_value = self.sample_poi
        wait_time_service.add_wait_time_suggestion(
            self.test_user, "tim_hortons_musc", 5
        )
        mock_waittime_submit_func.assert_called_once()

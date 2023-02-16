import unittest
from unittest.mock import patch, Mock
from app.user.user import User

from app.wait_time import service as wait_time_service
from app.wait_time.location import UserLocation

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

    def test_uid_to_aid(self, mock_location_collection):
        self.assertTrue(len(wait_time_service.uid_to_aid(SAMPLE_UID)) > 0)

    def test_update_location(self, mock_location_collection):
        wait_time_service.update_location(self.test_location)
        mock_location_collection().document().set.assert_called_once()

    @patch("app.events.service.generate_waittime_submit_event")
    def test_add_wait_time_suggestion(
        self, mock_waittime_submit_func, mock_location_collection
    ):
        wait_time_service.add_wait_time_suggestion(
            self.test_user, "tim_hortons_musc", 5
        )
        mock_waittime_submit_func.assert_called_once()

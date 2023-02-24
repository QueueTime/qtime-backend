import unittest
from unittest.mock import patch, Mock
from test.mixins.firebase_mixin import FirebaseTestMixin

from datetime import datetime, timezone, timedelta
from app.firebase import firestore_db, POI_COLLECTION
from app.user.user import User
from app.wait_time import service as wait_time_service
from app.wait_time.location import UserLocation
from app.locations.poi import POI
from app.wait_time.sourcing_data import POIPool
from app.wait_time.errors import UserNotInPoolError, UserAlreadyInPoolError

SAMPLE_UID = "2Nc3UKvI98YvhTlud9ZEomZHr9p2"

sample_poi = POI(
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

other_poi = POI(
    id="booster_juice_musc",
    name="Booster Juice MUSC",
    address="McMaster University Student Centre",
    poi_type="EATERY",
    location={"latitude": 43.263532187492686, "longitude": -79.91758503073444},
    image_url="https://discover.mcmaster.ca/app/uploads/2019/06/Booster-Juice.jpg",
    classification="queue",
    hours_of_operation={
        "Sunday": "Closed",
        "Monday": "10:00 AM - 6:30 PM",
        "Tuesday": "10:00 AM - 6:30 PM",
        "Wednesday": "10:00 AM - 6:30 PM",
        "Thursday": "10:00 AM - 6:30 PM",
        "Friday": "10:00 AM - 6:30 PM",
        "Saturday": "Closed",
    },
)


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

    @patch("app.wait_time.service.generate_waittime_submit_event")
    @patch("app.wait_time.service.get_details_for_POI")
    def test_add_wait_time_suggestion(
        self, mock_get_poi_func, mock_waittime_submit_func, mock_location_collection
    ):
        mock_get_poi_func.return_value = sample_poi
        wait_time_service.add_wait_time_suggestion(
            self.test_user, "tim_hortons_musc", 5
        )
        mock_waittime_submit_func.assert_called_once()


# Separate class for computation tests to utilize Firebase Emulator instead of mocking
class TestWaitTimeComputation(unittest.TestCase, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        sample_iso_timestamp1 = (
            datetime.now(timezone.utc) - timedelta(seconds=400)
        ).isoformat()
        sample_iso_timestamp2 = (
            datetime.now(timezone.utc) - timedelta(seconds=1900)
        ).isoformat()
        self.sample_pool_dict = {
            "current_average_wait_time": 8,
            "pool": {
                "test@sample.com": {
                    "start_time": datetime.now(timezone.utc) - timedelta(seconds=300),
                    "last_seen": datetime.now(timezone.utc) - timedelta(seconds=100),
                }
            },
            "recent_wait_times": {sample_iso_timestamp1: 6, sample_iso_timestamp2: 9},
        }

    def setUp(self):
        self.test_user = User("test@sample.com")
        self.with_user_accounts(self.test_user)
        self.sample_pool = POIPool(
            "tim_hortons_musc",
            pool=self.sample_pool_dict["pool"],
            recent_wait_times=self.sample_pool_dict["recent_wait_times"],
            current_average_wait_time=self.sample_pool_dict[
                "current_average_wait_time"
            ],
        )
        # Sample POI
        sample_poi = POI(
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
        firestore_db().collection(POI_COLLECTION).document(sample_poi.id).set(
            sample_poi.to_dict()
        )

        wait_time_service.save_poi_pool(self.sample_pool)
        wait_time_service.save_poi_pool(POIPool(other_poi.id))

    def tearDown(self):
        self.delete_user_accounts()
        self.clear_all_firestore_data()

    def test_get_pool_for_poi(self):
        self.assertEqual(
            wait_time_service.get_pool_for_poi(sample_poi), self.sample_pool
        )

    def test_save_poi_pool(self):
        firestore_db().collection(POI_COLLECTION).document(sample_poi.id).delete()
        wait_time_service.save_poi_pool(self.sample_pool)
        self.assertEqual(
            wait_time_service.get_pool_for_poi(sample_poi), self.sample_pool
        )

    def test_add_user_to_pool(self):
        self.assertRaises(
            UserAlreadyInPoolError,
            wait_time_service.add_user_to_poi_pool,
            self.test_user,
            other_poi,
        )
        wait_time_service.remove_user_from_poi_pool(self.test_user, sample_poi)
        wait_time_service.add_user_to_poi_pool(self.test_user, sample_poi)
        self.assertTrue(wait_time_service.get_user_current_poi_pool(self.test_user))
        # Make sure we can update the user's last seen timestamp as well
        wait_time_service.add_user_to_poi_pool(self.test_user, sample_poi)

    def test_remove_user_from_pool(self):
        wait_time_service.remove_user_from_poi_pool(self.test_user, sample_poi)
        self.assertFalse(wait_time_service.get_user_current_poi_pool(self.test_user))
        self.assertRaises(
            UserNotInPoolError,
            wait_time_service.remove_user_from_poi_pool,
            self.test_user,
            sample_poi,
        )

    def test_get_user_current_poi_pool(self):
        self.assertEqual(
            wait_time_service.get_user_current_poi_pool(self.test_user),
            self.sample_pool,
        )

    def test_get_wait_time_from_poi_pool(self):
        self.assertEqual(
            self.sample_pool.current_average_wait_time,
            wait_time_service.get_wait_time_from_poi_pool(sample_poi),
        )

import unittest
from unittest.mock import patch, ANY, call

from app.events import service as event_service
from app.user.api import User
from app.locations.poi import POI


@patch("app.events.service.firestore_db")
class TestEventService(unittest.TestCase):
    """Test the event service"""

    @classmethod
    def setUpClass(self):
        self.email = "test@sample.ca"
        self.poi_id = "SAMPLE_POI"
        self.points_awarded = 25
        self.user = User(self.email, "XJFEKDG", 0)
        self.poi = POI(
            self.poi_id, "Testing poi", "Testing", None, None, None, None, None
        )

    def test_generate_account_signup_event(self, firebase_mock):
        event_service.generate_account_signup_event(self.user)
        firebase_mock().collection().add.assert_called_once_with(
            {
                "type": "account_signup_event",
                "user": self.email,
                "payload": None,
                "created": ANY,
            }
        )

    def test_generate_account_delete_event(self, firebase_mock):
        event_service.generate_account_delete_event(self.user)
        firebase_mock().collection().add.assert_called_once_with(
            {
                "type": "account_delete_event",
                "user": self.email,
                "payload": None,
                "created": ANY,
            }
        )

    def test_generate_waittime_submit_event(self, firebase_mock):
        event_service.generate_waittime_submit_event(
            self.user, self.poi, 50, self.points_awarded
        )
        calls = [
            call(
                {
                    "type": "waittime_submit_event",
                    "user": self.email,
                    "payload": {
                        "poi_id": self.poi_id,
                        "estimate_submitted": 50,
                    },
                    "created": ANY,
                }
            ),
            call(
                {
                    "type": "reward_points_add_event",
                    "user": self.email,
                    "payload": {
                        "source": "waittime_submit",
                        "points_change": self.points_awarded,
                    },
                    "created": ANY,
                }
            ),
        ]
        firebase_mock().collection().add.assert_has_calls(calls, any_order=True)

    def test_generate_waittime_confirm_event(self, firebase_mock):
        event_service.generate_waittime_confirm_event(
            self.user, self.poi, self.points_awarded
        )
        calls = [
            call(
                {
                    "type": "waittime_confirm_event",
                    "user": self.email,
                    "payload": {"poi_id": self.poi_id},
                    "created": ANY,
                }
            ),
            call(
                {
                    "type": "reward_points_add_event",
                    "user": self.email,
                    "payload": {
                        "source": "waittime_confirm",
                        "points_change": self.points_awarded,
                    },
                    "created": ANY,
                }
            ),
        ]
        firebase_mock().collection().add.assert_has_calls(calls, any_order=True)

    def test_generate_referral_event_same_user(self, firebase_mock):
        with self.assertRaises(ValueError):
            event_service.generate_referral_event(
                self.user, self.user, self.points_awarded
            )

    def test_generate_referral_event(self, firebase_mock):
        referral_email = "refferer@sample.com"
        same_referral_user = User(referral_email, "ASDKGUE")

        event_service.generate_referral_event(
            self.user, same_referral_user, self.points_awarded
        )

        calls = [
            call(
                {
                    "type": "reward_points_add_event",
                    "user": self.email,
                    "payload": {
                        "source": "referred_bonus",
                        "points_change": self.points_awarded,
                    },
                    "created": ANY,
                }
            ),
            call(
                {
                    "type": "reward_points_add_event",
                    "user": referral_email,
                    "payload": {
                        "source": "referral_bonus",
                        "points_change": self.points_awarded,
                    },
                    "created": ANY,
                }
            ),
        ]
        firebase_mock().collection().add.assert_has_calls(calls, any_order=True)

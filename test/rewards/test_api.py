import unittest
from unittest.mock import ANY, patch, Mock
import json
from datetime import datetime, timezone
from freezegun import freeze_time

from app.user.user import User
from app.firebase import firestore_db, EVENTS_COLLECTION, USERS_COLLECTION
from app.events.event import Event, EventType, RewardPointsAddPayload, RewardSource
from test.mixins.flask_client_mixin import FlaskTestClientMixin
from test.mixins.firebase_mixin import FirebaseTestMixin
import app.events.event


class TestRewardsApi(unittest.TestCase, FlaskTestClientMixin, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        self.with_test_flask_client(self)

    def setUp(self):
        self.with_rest_defaults()

        # Create referral codes for test users
        self.user_referral_code = "ABCDEF"
        self.referrer_user_code = "XYZDEF"
        self.user = User("sample@test.com", self.user_referral_code)
        self.referrer_user = User("referrer@test.com", self.referrer_user_code)
        self.with_user_accounts(self.user, self.referrer_user)

        # Create sample events
        self.events = [
            Event(
                EventType.REWARD_POINTS_ADD,
                self.user.email,
                RewardPointsAddPayload(RewardSource.WAITTIME_CONFIRM, 10),
                datetime(2023, 2, 13, 12, 30, 0).astimezone(timezone.utc),
            ),
            Event(
                EventType.REWARD_POINTS_ADD,
                self.user.email,
                RewardPointsAddPayload(RewardSource.WAITTIME_SUBMIT, 20),
                datetime(2023, 2, 10, 12, 30, 0).astimezone(timezone.utc),
            ),
            Event(
                EventType.ACCOUNT_SIGNUP,
                self.user.email,
                None,
                datetime(2023, 1, 10, 12, 30, 0).astimezone(timezone.utc),
            ),
        ]
        for event in self.events:
            firestore_db().collection(EVENTS_COLLECTION).add(event.to_dict())

    def tearDown(self):
        self.delete_user_accounts()
        self.clear_all_firestore_data()

    def test_submit_referral_code_invalid_code(self):
        response = self.client.post(
            f"{self.base_url}/user/referral/invalid23",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_referral_code_onboarded_user(self):
        firestore_db().collection(USERS_COLLECTION).document(self.user.email).update(
            {
                "hasCompletedOnboarding": True,
            }
        )
        response = self.client.post(
            f"{self.base_url}/user/referral/XYZDEF",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_referral_code_already_used_code(self):
        firestore_db().collection(USERS_COLLECTION).document(self.user.email).update(
            {
                "hasUsedReferralCode": True,
            }
        )
        response = self.client.post(
            f"{self.base_url}/user/referral/XYZDEF",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_referral_code_code_not_found(self):
        response = self.client.post(
            f"{self.base_url}/user/referral/NOTFND",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_submit_referral_code_use_own_code(self):
        response = self.client.post(
            f"{self.base_url}/user/referral/{self.user_referral_code}",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    @patch("app.events.event.datetime")
    def test_submit_referral_code_success(self, mock_dt):
        mock_date = datetime(2023, 2, 10, 12, 30, 0)
        mock_dt.fromtimestamp.return_value = mock_date
        # Clear all events for testing
        self.clear_all_documents_in_collection(EVENTS_COLLECTION)
        response = self.client.post(
            f"{self.base_url}/user/referral/{self.referrer_user_code}",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 204)

        # Verify users have been updated
        updated_user = User.from_dict(
            self.user.email,
            firestore_db()
            .collection(USERS_COLLECTION)
            .document(self.user.email)
            .get()
            .to_dict(),
        )
        updated_referrer_user = User.from_dict(
            self.referrer_user.email,
            firestore_db()
            .collection(USERS_COLLECTION)
            .document(self.referrer_user.email)
            .get()
            .to_dict(),
        )
        self.assertEqual(updated_user.reward_point_balance, 200)
        self.assertTrue(updated_user.hasUsedReferralCode)
        self.assertEqual(updated_referrer_user.reward_point_balance, 200)

        # Verify events have been created
        events_stream = firestore_db().collection(EVENTS_COLLECTION).stream()
        events_created = list(
            map(lambda e: Event.from_dict(e.to_dict()), events_stream)
        )
        expected_events = [
            Event(
                EventType.REWARD_POINTS_ADD,
                self.user.email,
                RewardPointsAddPayload(RewardSource.REFERRED_BONUS, 200),
                mock_date,
            ),
            Event(
                EventType.REWARD_POINTS_ADD,
                self.referrer_user.email,
                RewardPointsAddPayload(RewardSource.REFERRAL_BONUS, 200),
                mock_date,
            ),
        ]
        self.maxDiff = None
        self.assertCountEqual(
            events_created,
            expected_events,
        )

    def test_list_reward_events_incorrect_limit(self):
        response = self.client.get(
            f"{self.base_url}/user/rewards/events?limit=105",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_list_reward_events_before_query(self):
        response = self.client.get(
            f"{self.base_url}/user/rewards/events?before=2023-02-12T12:30:00.0Z",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(
            json.loads(response.data),
            [
                {
                    "source": RewardSource.WAITTIME_SUBMIT.value,
                    "points": 20,
                    "timestamp": datetime(2023, 2, 10, 12, 30, 0).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                },
            ],
        )
        self.assertEqual(response.status_code, 200)

    def test_list_reward_events(self):
        response = self.client.get(
            f"{self.base_url}/user/rewards/events",
            headers={"Authorization": f"Bearer {self.token(self.user.email)}"},
        )
        self.assertEqual(
            json.loads(response.data),
            [
                {
                    "source": RewardSource.WAITTIME_CONFIRM.value,
                    "points": 10,
                    "timestamp": datetime(2023, 2, 13, 12, 30, 0).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                },
                {
                    "source": RewardSource.WAITTIME_SUBMIT.value,
                    "points": 20,
                    "timestamp": datetime(2023, 2, 10, 12, 30, 0).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                },
            ],
        )
        self.assertEqual(response.status_code, 200)

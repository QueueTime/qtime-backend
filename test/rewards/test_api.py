import unittest
from test.mixins.flask_client_mixin import FlaskTestClientMixin
from test.mixins.firebase_mixin import FirebaseTestMixin
import json
from datetime import datetime, timezone
from app.user.user import User
from app.firebase import firestore_db, EVENTS_COLLECTION
from app.events.event import Event, EventType, RewardPointsAddPayload, RewardSource


class TestRewardsApi(unittest.TestCase, FlaskTestClientMixin, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        self.with_test_flask_client(self)

        self.user = "sample@test.com"
        self.tokens = self.with_user_accounts(self, User(self.user, "ABCDEF"))
        # Create sample events
        self.events = [
            Event(
                EventType.REWARD_POINTS_ADD,
                self.user,
                RewardPointsAddPayload(RewardSource.WAITTIME_CONFIRM, 10),
                datetime(2023, 2, 13, 12, 30, 0).astimezone(timezone.utc),
            ),
            Event(
                EventType.REWARD_POINTS_ADD,
                self.user,
                RewardPointsAddPayload(RewardSource.WAITTIME_SUBMIT, 20),
                datetime(2023, 2, 10, 12, 30, 0).astimezone(timezone.utc),
            ),
            Event(
                EventType.ACCOUNT_SIGNUP,
                self.user,
                None,
                datetime(2023, 1, 10, 12, 30, 0).astimezone(timezone.utc),
            ),
        ]
        for event in self.events:
            firestore_db().collection(EVENTS_COLLECTION).add(event.to_dict())

    @classmethod
    def tearDownClass(self):
        self.delete_user_accounts(self)
        self.clear_all_firestore_data(self)

    def setUp(self):
        self.with_rest_defaults()

    # submit referral code

    def test_list_reward_events_incorrect_limit(self):
        response = self.client.get(
            f"{self.base_url}/user/rewards/events?limit=105",
            headers={"Authorization": f"Bearer {self.tokens[self.user]()}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_list_reward_events_before_query(self):
        response = self.client.get(
            f"{self.base_url}/user/rewards/events?before=2023-02-12T12:30:00.0Z",
            headers={"Authorization": f"Bearer {self.tokens[self.user]()}"},
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
            headers={"Authorization": f"Bearer {self.tokens[self.user]()}"},
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

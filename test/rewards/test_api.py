import unittest
from test.mixins.flask_client_mixin import FlaskTestClientMixin
from test.mixins.firebase_mixin import FirebaseTestMixin
import json
from app.user.user import User


class TestRewardsApi(unittest.TestCase, FlaskTestClientMixin, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        self.with_test_flask_client(self)

        self.user = "sample@test.com"
        self.tokens = self.with_user_accounts(self, User(self.user, "ABCDEF"))

    @classmethod
    def tearDownClass(self):
        self.delete_user_accounts(self)
        self.clear_all_firestore_data(self)

    def setUp(self):
        self.with_rest_defaults()

    def test_list_reward_events(self):
        response = self.client.get(
            f"{self.base_url}/user/rewards/events",
            headers={"Authorization": f"Bearer {self.tokens[self.user]()}"},
        )

        print(json.loads(response.data))
        assert response.status_code == 200

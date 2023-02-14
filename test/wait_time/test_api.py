import unittest
from unittest.mock import patch
from app.user.user import User

from test.mixins.flask_client_mixin import FlaskTestClientMixin
from test.mixins.firebase_mixin import FirebaseTestMixin


class TestWaitTimeApi(unittest.TestCase, FlaskTestClientMixin, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        self.with_test_flask_client(self)
        self.with_rest_defaults()

    def setUp(self):
        self.test_user = User("test@sample.com")
        self.with_user_accounts(self.test_user)

    def tearDown(self):
        self.delete_user_accounts()
        self.clear_all_firestore_data()

    def test_update_user_location(self):
        response = self.client.post(
            f"{self.base_url}/user/location",
            headers={"Authorization": f"Bearer {self.token(self.test_user.email)}"},
        )
        self.assertEqual(response.status_code, 200)

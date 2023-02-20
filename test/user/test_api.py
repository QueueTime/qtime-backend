import unittest
from test.mixins.flask_client_mixin import FlaskTestClientMixin
from test.mixins.firebase_mixin import (
    FirebaseTestMixin,
    _create_user_in_firebase_auth_emulator,
    USER_PASSWORD,
)

from app.user.service import find_user
from app.user.errors import UserNotFoundError
from app.user.user import User


class TestUsersApi(unittest.TestCase, FlaskTestClientMixin, FirebaseTestMixin):
    @classmethod
    def setUpClass(self):
        self.with_firebase_emulators(self)
        self.with_test_flask_client(self)
        self.with_rest_defaults(self)
        self.sample_user = User("sample@test.com", referral_code="ABCDEF")

    def tearDown(self):
        self.delete_user_accounts()
        self.clear_all_firestore_data()

    def test_signup(self):
        # Workaround to have a user in the auth emulator but not in the database
        _create_user_in_firebase_auth_emulator(
            self.sample_user.email, USER_PASSWORD, self.sample_user.email
        )
        response = self.client.post(
            f"{self.base_url}/user/signup",
            headers={"Authorization": f"Bearer {self.token(self.sample_user.email)}"},
        )

        self.assertEqual(response.status_code, 204)
        find_user("sample@test.com")

    def test_delete_user_profile(self):
        self.with_user_accounts(self.sample_user)
        response = self.client.delete(
            f"{self.base_url}/user/delete-account",
            headers={"Authorization": f"Bearer {self.token(self.sample_user.email)}"},
        )
        self.assertEqual(response.status_code, 204)
        self.assertRaises(UserNotFoundError, find_user, "sample@test.com")

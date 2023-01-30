import unittest
from firebase_admin import credentials, initialize_app, firestore
from app.user_api.User import User
from app.user_api.errors import UserNotFoundError
import json

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        self.firestore_db = firestore.client()
        self.users_ref = self.firestore_db.collection('users')
    
    def test_user_push_and_fetch(self):
        user = User(self.users_ref, "test@test.com", "", 0, False, "", 0, 0, {}, False)
        user.push()
        fetched_user = User.get(self.users_ref, "test@test.com")
        self.assertEqual(user.to_json(), fetched_user.to_json())

    def test_error_handling(self):
        self.assertRaises(UserNotFoundError, User.get, self.users_ref, "test@nonexistent.com")

    def tearDown(self):
        self.users_ref.document('test@test.com').delete()


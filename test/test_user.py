import unittest
from firebase_admin import credentials, initialize_app, firestore
from app.user_api.User import User
from app.user_api.errors import UserNotFoundError
from app.user_api import user_service
from app.user_api import user_api
import json


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        cred = credentials.Certificate("./serviceAccountKey.json")
        self.default_app = initialize_app(cred)
        self.firestore_db = firestore.client()
        self.users_ref = self.firestore_db.collection("users")

    def test_user_push_and_fetch(self):
        user = User(self.users_ref, "test@test.com", "", 0, False, "", 0, 0, {}, False)
        user.push()
        fetched_user = User.get(self.users_ref, "test@test.com")
        self.assertEqual(user.to_json(), fetched_user.to_json())

    def test_error_handling(self):
        self.assertRaises(
            UserNotFoundError, User.get, self.users_ref, "test@nonexistent.com"
        )

    def tearDown(self):
        self.users_ref.document("test@test.com").delete()
class TestUserService(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.firestore_db = firestore.client()
        self.users_ref = self.firestore_db.collection('users')
        self.user_service = user_service.User_Service()
        self.test_user = User(self.users_ref, "test@test.com", "", 0, False, "", 0, 0, {}, False)
        self.test_user.push()

    def test_find_user(self):
        self.assertEqual(self.test_user, self.user_service.findUser("test@test.com"))
        self.assertRaises(UserNotFoundError, self.user_service.findUser, "test@nonexistent.com")

    def test_delete_user(self):
        self.assertRaises(UserNotFoundError, self.user_service.deleteUser, User(self.users_ref, "test@nonexistent.com"))
        self.user_service.deleteUser(self.test_user)
        self.assertRaises(UserNotFoundError, User.get, self.users_ref, "test@test.com")
        # cleanup
        self.test_user.push()


    

import unittest
from firebase_admin import credentials, initialize_app, firestore
from app.User import User
import json

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        cred = credentials.Certificate("app/key/serviceAccountKey.json")
        #default_app = initialize_app(cred)     (not needed when running unittest)
        self.firestore_db = firestore.client()
        self.users_ref = self.firestore_db.collection('users')
    
    def test_user_push_and_fetch(self):
        user = User(self.users_ref, "test@test.com", "", 0, False, "", 0, 0, [])
        user.push()
        fetched_user = User.get(self.users_ref, "test@test.com")
        self.assertEqual(user.to_json(), fetched_user.to_json())

    def tearDown(self):
        self.users_ref.document('test@test.com').delete()


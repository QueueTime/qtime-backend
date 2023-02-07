import unittest
from unittest.mock import patch, Mock, MagicMock
from firebase_admin import firestore
from app import firebase
from app.user_api.User import User
from app.user_api.errors import UserNotFoundError
from app.user_api import user_service
from app.user_api import user_api
import json


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.sample_user_dict = {
            "email": "test@test.com",
            "referral_code": "",
            "reward_point_balance": 0,
            "notification_setting": False,
            "time_in_line": 0,
            "num_lines_participated": 0,
            "poi_frequency": {},
            "hasCompletedOnboarding": False,
        }
        self.sample_user = User(
            email="test@test.com",
            referral_code="",
            reward_point_balance=0,
            notification_setting=False,
            time_in_line=0,
            num_lines_participated=0,
            poi_frequency={},
            hasCompletedOnboarding=False,
        )

    def test_to_from_dict(self):
        self.assertEqual(
            self.sample_user.to_json(), User.from_dict(self.sample_user_dict).to_json()
        )


@patch("app.user_api.user_service.users_collection")
class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.sample_user_dict = {
            "email": "test@test.com",
            "referral_code": "",
            "reward_point_balance": 0,
            "notification_setting": False,
            "time_in_line": 0,
            "num_lines_participated": 0,
            "poi_frequency": {},
            "hasCompletedOnboarding": False,
        }
        self.sample_user = User(
            email="test@test.com",
            referral_code="",
            reward_point_balance=0,
            notification_setting=False,
            time_in_line=0,
            num_lines_participated=0,
            poi_frequency={},
            hasCompletedOnboarding=False,
        )

    def test_find_user(self, user_collection_mock):
        user_collection_mock.document().get().to_dict = MagicMock(
            return_value=self.sample_user_dict
        )
        self.assertEqual(self.sample_user, user_service.find_user("test@test.com"))
        user_collection_mock.document().get().exists = False
        self.assertRaises(
            UserNotFoundError, user_service.find_user, "test@nonexistent.com"
        )

    def test_delete_user(self, user_collection_mock):
        user_service.delete_user(self.sample_user)
        user_collection_mock.document().delete.assert_called_once()
        user_collection_mock.document().get().exists = False
        self.assertRaises(
            UserNotFoundError,
            user_service.delete_user,
            User("test@nonexistent.com"),
        )

    def test_update_user(self, user_collection_mock):
        user_service.update_user(self.sample_user)
        user_collection_mock.document().set.assert_called_once()

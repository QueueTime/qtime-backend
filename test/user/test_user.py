import unittest

from app.user.user import User


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.sample_user_dict = {
            "referral_code": "",
            "reward_point_balance": 0,
            "notification_setting": False,
            "time_in_line": 0,
            "num_lines_participated": 0,
            "poi_frequency": {},
            "hasCompletedOnboarding": False,
            "hasUsedReferralCode": False,
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
            hasUsedReferralCode=False,
        )

    def test_to_from_dict(self):
        self.assertEqual(
            self.sample_user.to_json(),
            User.from_dict("test@test.com", self.sample_user_dict).to_json(),
        )

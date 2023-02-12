import unittest
from unittest.mock import patch, Mock

from app.rewards import service as rewards_service


@patch("app.rewards.service.firestore_db")
class TestRewardsService(unittest.TestCase):
    """Test the rewards service"""

    @classmethod
    def setUpClass(self):
        self.email = "test@sample.ca"

    def test_generates_accurate_referral_code(self, firebase_mock):
        firebase_mock().collection().document().get().exists = False
        referral_code = rewards_service.create_unique_referral_code()
        self.assertTrue(len(referral_code) == 6)

    def test_generates_unique_referral_code(self, firebase_mock):
        def func(code):
            mock = Mock()
            mock.get().exists = True if code == "ABCDEF" else False
            return mock

        with patch.object(rewards_service, "_generate_unique_code") as mock:
            mock.side_effect = ["ABCDEF", "XYZABC"]
            firebase_mock().collection().document.side_effect = func
            referral_code = rewards_service.create_unique_referral_code()
            self.assertTrue(referral_code == "XYZABC")

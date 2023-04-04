from typing import Dict, Any
from app.common import BadDataError
import json


class User:
    def __init__(
        self,
        email,
        referral_code="",
        reward_point_balance=0,
        notification_setting=False,
        time_in_line=0,
        num_lines_participated=0,
        poi_frequency={},
        hasCompletedOnboarding=False,
        hasUsedReferralCode=False,
    ):
        self.email = email
        self.referral_code = referral_code
        self.reward_point_balance = reward_point_balance
        self.notification_setting = notification_setting
        self.time_in_line = time_in_line
        self.num_lines_participated = num_lines_participated
        self.poi_frequency = poi_frequency
        self.hasCompletedOnboarding = hasCompletedOnboarding
        self.hasUsedReferralCode = hasUsedReferralCode

    @staticmethod
    def from_dict(email: str, dict: Dict[str, Any]) -> "User":
        """
        Creates a new User object from a Python Dictionary

        Args:
            dict: Dictionary of key-value pairs corresponding to user.

        Returns:
            User: from specified data

        Raises:
            BadDataError: If required data is missing from the dictionary
        """
        try:
            return User(
                email,
                dict["referral_code"],
                dict["reward_point_balance"],
                dict["notification_setting"],
                dict["time_in_line"],
                dict["num_lines_participated"],
                dict["poi_frequency"],
                dict["hasCompletedOnboarding"],
                dict["hasUsedReferralCode"],
            )
        except KeyError as e:
            raise BadDataError("Missing data from user data: " + str(e))

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all properties from the User

        Returns:
            dict: containing key-value pairs with all User data
        """
        dict = self.__dict__.copy()
        # Delete primary key before returning dict
        del dict["email"]
        return dict

    def to_json(self) -> str:
        """Return all properties in a JSON string"""
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        return isinstance(other, User) and self.to_dict() == other.to_dict()

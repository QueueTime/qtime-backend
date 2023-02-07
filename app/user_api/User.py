from app import common
from app.user_api.errors import UserNotFoundError
import json


class User(common.FirebaseDataEntity):
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
    ):
        self.email = email
        self.referral_code = referral_code
        self.reward_point_balance = reward_point_balance
        self.notification_setting = notification_setting
        self.time_in_line = time_in_line
        self.num_lines_participated = num_lines_participated
        self.poi_frequency = poi_frequency
        self.hasCompletedOnboarding = hasCompletedOnboarding

    def from_dict(dict):
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
                dict["email"],
                dict.get("referral_code", ""),
                dict.get("reward_point_balance", 0),
                dict.get("notification_setting", False),
                dict.get("time_in_line", 0),
                dict.get("num_lines_participated", 0),
                dict.get("poi_frequency", {}),
                dict.get("hasCompletedOnboarding", False),
            )
        except KeyError as e:
            raise common.BadDataError("Missing data from user data: " + str(e))

    def to_dict(self):
        """
        Returns a dictionary containing all properties from the User

        Returns:
            dict: containing key-value pairs with all User data
        """
        new_dict = {
            "email": self.email,
            "referral_code": self.referral_code,
            "reward_point_balance": self.reward_point_balance,
            "notification_setting": self.notification_setting,
            "time_in_line": self.time_in_line,
            "num_lines_participated": self.num_lines_participated,
            "poi_frequency": self.poi_frequency,
            "hasCompletedOnboarding": self.hasCompletedOnboarding,
        }
        return new_dict

    def __eq__(self, other):
        return self.email == other.email

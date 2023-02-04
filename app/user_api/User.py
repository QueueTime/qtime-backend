from app import common
from app.user_api.errors import UserNotFoundError
import json


class User(common.FirebaseDataEntity):
    def __init__(
        self,
        db_ref,
        email,
        referral_code="",
        reward_point_balance=0,
        notification_setting=False,
        color_theme="SYSTEM",
        time_in_line=0,
        num_lines_participated=0,
        poi_frequency={},
        hasCompletedOnboarding=False,
    ):
        super().__init__(db_ref)
        self.email = email
        self.referral_code = referral_code
        self.reward_point_balance = reward_point_balance
        self.notification_setting = notification_setting
        self.color_theme = color_theme
        self.time_in_line = time_in_line
        self.num_lines_participated = num_lines_participated
        self.poi_frequency = poi_frequency
        self.hasCompletedOnboarding = hasCompletedOnboarding

    def get(db_ref, id):
        """
        Fetches a specified user from a database.

        Args:
            db_ref: A `CollectionReference` to the users table from Firestore
            id: A string of the user email to fetch

        Returns:
            User: specified by `id`

        Raises:
            UserNotFoundError: if the target user does not exist
        """
        target_data = db_ref.document(id).get()
        if not target_data.exists:
            raise UserNotFoundError(id)
        return User.from_dict(db_ref, target_data.to_dict())

    def from_dict(db_ref, dict):
        """
        Creates a new User object from a Python Dictionary

        Args:
            db_ref: A `CollectionReference` to the users table from Firestore
            dict: Dictionary of key-value pairs corresponding to user.

        Returns:
            User: from specified data

        Raises:
            BadDataError: If required data is missing from the dictionary
        """
        try:
            return User(
                db_ref,
                dict["email"],
                dict.get("referral_code", ""),
                dict.get("reward_point_balance", 0),
                dict.get("notification_setting", False),
                dict.get("color_theme", "SYSTEM"),
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
            "color_theme": self.color_theme,
            "time_in_line": self.time_in_line,
            "num_lines_participated": self.num_lines_participated,
            "poi_frequency": self.poi_frequency,
            "hasCompletedOnboarding": self.hasCompletedOnboarding,
        }
        return new_dict

    def push(self, merge=True):
        """Pushes data to Firebase"""
        target_ref = self.db_reference.document(self.email)
        target_ref.set(self.to_dict(), merge=merge)

    def __eq__(self, other):
        return self.email == other.email

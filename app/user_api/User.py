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
        hasCompletedOnboarding=False
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
        target_data = db_ref.document(id).get()
        if not target_data.exists:
            raise UserNotFoundError(id)
        return User.from_dict(db_ref, target_data.to_dict())

    def from_dict(db_ref, dict):
        try:
            return User(
                db_ref,
                dict["email"],
                dict["referral_code"],
                dict["reward_point_balance"],
                dict["notification_setting"],
                dict["color_theme"],
                dict["time_in_line"],
                dict["num_lines_participated"],
                dict["poi_frequency"],
                dict["hasCompletedOnboarding"]
            )
        except KeyError as e:
            raise common.BadDataError("Missing data from user data: " + str(e))

    def to_dict(self):
        new_dict = {
            "email" : self.email,
            "referral_code" : self.referral_code,
            "reward_point_balance" : self.reward_point_balance,
            "notification_setting" : self.notification_setting,
            "color_theme" : self.color_theme,
            "time_in_line" : self.time_in_line,
            "num_lines_participated" : self.num_lines_participated,
            "poi_frequency" : self.poi_frequency,
            "hasCompletedOnboarding": self.hasCompletedOnboarding
        }
        return new_dict

    def push(self, merge=True):
        target_ref = self.db_reference.document(self.email)
        target_ref.set(self.to_dict(), merge=merge)

    def __eq__(self, other):
        return self.email == other.email

        





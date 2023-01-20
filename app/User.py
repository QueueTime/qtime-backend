from app import common
import json

class User(common.FirebaseDataEntity):

    def __init__(
        self, 
        db_ref,
        email,
        referral_code,
        reward_point_balance,
        notification_setting,
        color_theme,
        time_in_line,
        num_lines_participated,
        poi_frequency
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
    
    def get(db_ref, id):
        target_data = db_ref.document(id).get()
        data = target_data.to_dict()
        new_user = User(
            db_ref,
            data["email"],
            data["referral_code"],
            data["reward_point_balance"],
            data["notification_setting"],
            data["color_theme"],
            data["time_in_line"],
            data["num_lines_participated"],
            data["poi_frequency"]
        )
        return new_user


    def to_dict(self):
        new_dict = {
            "email" : self.email,
            "referral_code" : self.referral_code,
            "reward_point_balance" : self.reward_point_balance,
            "notification_setting" : self.notification_setting,
            "color_theme" : self.color_theme,
            "time_in_line" : self.time_in_line,
            "num_lines_participated" : self.num_lines_participated,
            "poi_frequency" : self.poi_frequency
        }
        return new_dict

    def push(self, merge=True):
        target_ref = self.db_reference.document(self.email)
        target_ref.set(self.to_dict(), merge=merge)

    def __eq__(self, other):
        return self.email == other.email

        





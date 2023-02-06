from app.base_api_error import BaseApiError


class ReferralCodeNotFound(BaseApiError):
    def __init__(self, message):
        super(message, 404)

    def jsonify(self):
        return {"error": "Referral code not found", "message": self.message}, 404


class InvalidReferralOperation(BaseApiError):
    def __init__(self, message):
        super(message, 400)

    def jsonify(self):
        return {"error": "Invalid referral operation", "message": self.message}, 400

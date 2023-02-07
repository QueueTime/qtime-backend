from typing import Tuple, Dict

from app.base_api_error import BaseApiError


class ReferralCodeNotFound(BaseApiError):
    def __init__(self, message: str):
        super().__init__(message, 404)
        self.message = message

    def jsonify(self) -> Tuple[Dict[str, str], int]:
        return {"error": "Referral code not found", "message": self.message}, 404


class InvalidReferralOperation(BaseApiError):
    def __init__(self, message: str):
        super().__init__(message, 400)
        self.message = message

    def jsonify(self) -> Tuple[Dict[str, str], int]:
        return {"error": "Invalid referral operation", "message": self.message}, 400

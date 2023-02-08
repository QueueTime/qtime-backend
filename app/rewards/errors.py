from typing import Tuple, Dict

from app.base_api_error import BaseApiError


class ReferralCodeNotFound(BaseApiError):
    def __init__(self, message: str):
        super().__init__(f"Referral code not found. {message}", 404)


class InvalidReferralOperation(BaseApiError):
    def __init__(self, message: str):
        super().__init__(f"Invalid referral operation. {message}", 400)

# Contains exception types for User API errors

from app.base_api_error import BaseApiError


class UserNotFoundError(BaseApiError):
    def __init__(self, email=None, referral_code=None):
        super().__init__(
            f"User not found for criteria email={email}, referral_code={referral_code}",
            404,
        )


class UserAuthenticationError(BaseApiError):
    def __init__(self, message):
        super().__init__(message, 401)


class UserAlreadyExistsError(BaseApiError):
    def __init__(self, email):
        super().__init__(f"User already exists with email: {email}", 400)

# Contains exception types for User API errors


class UserNotFoundError(Exception):
    def __init__(self, email=None, referral_code=None):
        super().__init__(
            f"User not found for criteria email={email}, referral_code={referral_code}"
        )


class UserAuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)

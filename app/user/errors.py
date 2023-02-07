# Contains exception types for User API errors


class UserNotFoundError(Exception):
    def __init__(self, username):
        super().__init__("User not found: " + username)


class UserAuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)

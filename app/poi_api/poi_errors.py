from app.base_api_error import BaseApiError


class POINotFoundError(BaseApiError):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class InvalidPOISuggestionError(BaseApiError):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)

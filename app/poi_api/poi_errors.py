from app.base_api_error import BaseApiError


class POINotFoundError(BaseApiError):
    def __init__(self, message, error_code=404):
        super().__init__(message, error_code)


class InvalidPOISuggestionError(BaseApiError):
    def __init__(self, message, error_code=400):
        super().__init__(message, error_code)

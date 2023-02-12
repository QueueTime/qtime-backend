from app.base_api_error import BaseApiError


class POINotFoundError(BaseApiError):
    def __init__(self, message):
        super().__init__(f"Poi could not be found:{message}", 404)


class InvalidPOISuggestionError(BaseApiError):
    def __init__(self, message):
        super().__init__(f"Invalid POI suggestion: {message}", 400)

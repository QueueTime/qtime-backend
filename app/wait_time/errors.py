from app.base_api_error import BaseApiError


class POIPoolNotFoundError(BaseApiError):
    def __init__(self, poi_id: str):
        super().__init__(f"Pool not found for POI ID: {poi_id}", 500)


class UserNotInPoolError(BaseApiError):
    def __init__(self, user: str, poi_id: str):
        super().__init__(f"User {user} not found in pool for POI: {poi_id}", 500)

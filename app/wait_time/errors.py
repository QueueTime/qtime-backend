from app.base_api_error import BaseApiError


class POIPoolNotFoundError(BaseApiError):
    def __init__(self, poi_id: str):
        super().__init__(f"Pool not found for POI ID: {poi_id}", 500)


class UserNotInPoolError(BaseApiError):
    def __init__(self, user: str, poi_id: str):
        super().__init__(f"User {user} not found in pool for POI: {poi_id}", 500)


class UserAlreadyInPoolError(BaseApiError):
    def __init__(self, user: str, pool_id: str):
        super().__init__(f"User {user} is already in POI Pool: {pool_id}", 500)

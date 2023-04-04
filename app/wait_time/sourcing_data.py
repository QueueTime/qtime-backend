# Data classes used for sourcing will be placed here
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from app.common import BadDataError
from .errors import UserNotInPoolError
from statistics import mean
from app.common import SimpleMap


###### Payloads for POI pools
class POIPoolEntry(SimpleMap):
    def __init__(self, user: str, start_time: datetime, last_seen: datetime):
        self.user = user
        self.start_time = start_time
        self.last_seen = last_seen

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return POIPoolEntry(**dict)


class POIPoolSummary(SimpleMap):
    def __init__(self, current_average_wait_time: float):
        self.current_average_wait_time = current_average_wait_time

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return POIPoolSummary(**dict)


class RecentWaitTime(SimpleMap):
    def __init__(self, timestamp: datetime, wait_time: float):
        self.timestamp = timestamp
        self.wait_time = wait_time

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return RecentWaitTime(**dict)

# Data classes used for sourcing will be placed here
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from app.common import BadDataError
from .errors import UserNotInPoolError
from statistics import mean


class POIPool:
    """
    User pool corresponding to a specific POI. Timestamps for when a user is added to a pool and when they were last
    seen are recorded for each user in the pool.
    """

    def __init__(
        self,
        poi_id: str,
        pool: Dict[str, Dict[str, datetime]] = {},
        recent_wait_times: Dict[str, float] = {},
        current_average_wait_time: Optional[float] = None,
    ):
        """
        :param poi_id: ID of the POI as string
        :param pool: Pool data dict formatted as {"user": {"start_time": datetime, "last_seen": datetime}, ...}
        :param recent_wait_times: Recently served user data dict formatted as {"<ISO-timestamp>": float, ...}
        :param current_average_wait_time: Current average time in minutes a user spends in a pool
        """
        self.poi_id = poi_id
        self.pool = pool
        self.recent_wait_times = recent_wait_times
        self.current_average_wait_time = (
            self._recompute_average_wait_time()
            if current_average_wait_time is None
            else current_average_wait_time
        )

    @staticmethod
    def from_dict(poi_id: str, dict: Dict[str, Any]) -> "POIPool":
        """
        Create a new POIPool from a dict in the following format:
        {
            "current_average_wait_time": float,
            "pool": {
                "email": {
                    "start_time": datetime,
                    "last_seen": datetime
                         },...
                    },
            "recent_wait_times": {
                "<ISO-timestamp>": float,
                ...
            }
        }

        :param poi_id: ID of the POI
        :param dict: Dict containing pool data in the above format
        :returns: POIPool initialized with data from the given dictionary
        """
        try:
            return POIPool(
                poi_id=poi_id,
                pool=dict["pool"],
                recent_wait_times=dict["recent_wait_times"],
                current_average_wait_time=dict["current_average_wait_time"],
            )
        except KeyError as e:
            raise BadDataError(f"Missing data from POIPool data: {str(e)}", 500)

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all properties from the POIPool

        :returns: dictionary containing key-value pairs with all POIPool data
        """
        dict = self.__dict__.copy()
        # Delete primary key before returning dict
        del dict["poi_id"]
        return dict

    def update_user_in_pool(self, user: str):
        """
        Add a new user to the pool, or update the last_seen timestamp of an existing user if they are already present

        :param user: Email of the user to add
        """
        current_timestamp = datetime.now(timezone.utc)
        if user in self.pool:
            try:
                self.pool[user]["last_seen"] = current_timestamp
            except KeyError as e:
                raise BadDataError(f"Missing data from POI Pool entry: {str(e)}", 500)
        else:
            self.pool[user] = {
                "start_time": current_timestamp,
                "last_seen": current_timestamp,
            }

    def is_user_in_pool(self, user: str) -> bool:
        return user in self.pool

    def remove_user_from_pool(self, user: str):
        """
        Removes a user from the pool. Average wait time per user and total users are updated in the pool
        before removal

        :param user: Email of the user to remove
        """
        # Add time taken to serve user to recent wait times
        current_timestamp = datetime.now(timezone.utc)
        try:
            user_pool_data = self.pool[user]
        except KeyError:
            raise UserNotInPoolError(user, self.poi_id)
        try:
            wait_time = (current_timestamp - user_pool_data["start_time"]).seconds / 60
        except KeyError as e:
            raise BadDataError(f"Missing data from POI Pool entry: {str(e)}", 500)

        self.recent_wait_times[current_timestamp.isoformat()] = wait_time

        del self.pool[user]
        self._recompute_average_wait_time()

    def clear_stale_pool_users(self, ttl: int = 300):
        """
        Clear stale users in the pool last seen before the ttl
        Default is 300 seconds (5 minutes)

        :param ttl: Time to live for each user in the pool in seconds
        """

        current_timestamp = datetime.now(timezone.utc)
        for user in self.pool.copy():
            if (current_timestamp - self.pool[user]["last_seen"]).seconds >= ttl:
                self.remove_user_from_pool(user)

    def clear_stale_wait_times(self, ttl: int = 1800):
        """
        Clear stale wait times in the recent_wait_times dict older than `ttl` specified in seconds.
        Default is 1800 seconds (30 minutes)

        :param ttl: Time to live for each entry in recent wait times in seconds
        """
        current_timestamp = datetime.now(timezone.utc)
        for isotimestamp in self.recent_wait_times.copy():
            timestamp = datetime.fromisoformat(isotimestamp)
            if (current_timestamp - timestamp).seconds >= ttl:
                del self.recent_wait_times[isotimestamp]
        self._recompute_average_wait_time()

    def _recompute_average_wait_time(self) -> float:
        """Recompute current average wait time"""

        # Only compute if recent wait times is nonempty
        if self.recent_wait_times:
            self.current_average_wait_time = mean(self.recent_wait_times.values())
        return self.current_average_wait_time

    def __eq__(self, other):
        return isinstance(other, POIPool) and self.__dict__ == other.__dict__

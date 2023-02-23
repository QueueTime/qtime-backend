# Data classes used for sourcing will be placed here
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta


class POIPool:
    """
    User pool corresponding to a specific POI. Timestamps for when a user is added to a pool and when they were last
    seen are recorded for each user in the pool.
    """

    def __init__(
        self,
        poi_id: str,
        pool_data: Dict[str, Dict[str, datetime]] = {},
        current_average_waittime: Optional[int] = None,
    ):
        """
        :param poi_id: ID of the POI as string
        :param pool_data: Pool data dict formatted as {"email": {"start_time": datetime, "last_seen": datetime}, ...}
        :param current_average_waittime: Current average wait time of users in pool (if available)
        """
        self.poi_id = poi_id
        self.pool_data = pool_data
        self._current_average_waittime = (
            self._compute_average_wait_time()
            if current_average_waittime is None
            else current_average_waittime
        )

    def _compute_average_wait_time(self):
        """Recompute current average wait time"""
        now = datetime.now(timezone.utc)

        total_seconds = 0
        for time in self.pool_data.values():
            time_delta: timedelta = now - time
            total_seconds += time_delta.seconds

        self._current_average_waittime = total_seconds // len(self.pool_data)
        return self._current_average_waittime

    def get_average_wait_time(self):
        """Returns the current average wait time of the pool"""
        return self._current_average_waittime

    def add_user_to_pool(self, email: str):
        """
        Add a new user to the pool

        :param email: Email of the user to add
        """
        current_timestamp = datetime.now(timezone.utc)
        if email in self.pool_data:
            self.pool_data[email]["last_seen"] = current_timestamp
        else:
            self.pool_data[email] = {
                "start_time": current_timestamp,
                "last_seen": current_timestamp,
            }
            self._compute_average_wait_time()

    def remove_user_from_pool(self, email: str):
        """
        Removes a user from the pool

        :param email: Email of the user to remove
        """
        del self.pool_data[email]
        self._compute_average_wait_time()

# Data classes used for sourcing will be placed here
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from app.common import BadDataError


class POIPool:
    """
    User pool corresponding to a specific POI. Timestamps for when a user is added to a pool and when they were last
    seen are recorded for each user in the pool.
    """

    def __init__(
        self,
        poi_id: str,
        pool_data: Dict[str, Dict[str, datetime]] = {},
        current_average_wait_time: Optional[float] = None,
    ):
        """
        :param poi_id: ID of the POI as string
        :param pool_data: Pool data dict formatted as {"user": {"start_time": datetime, "last_seen": datetime}, ...}
        :param current_average_waittime: Current average time in minutes a user spends in a pool
        """
        self.poi_id = poi_id
        self.pool_data = pool_data
        self.current_average_wait_time = (
            self._compute_average_wait_time
            if current_average_wait_time is None
            else current_average_wait_time
        )

    @classmethod
    def from_dict(poi_id: str, dict: Dict[str, Any]) -> "POIPool":
        """
        Create a new POIPool from a dict in the following format:
        {
            "current_average_wait_time": float,
            "pool": {
                "email": {
                    "start_time": datetime
                    "last_seen": datetime
                         },...
                    }
        }

        :param poi_id: ID of the POI
        :param dict: Dict containing pool data in the above format
        :returns: POIPool initialized with data from the given dictionary
        """
        try:
            return POIPool(
                poi_id=poi_id,
                pool_data=dict["pool"],
                current_average_wait_time=dict["current_average_wait_time"],
            )
        except KeyError as e:
            raise BadDataError(f"Missing data from POIPool data: {str(e)}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all properties from the POIPool

        :returns: dictionary containing key-value pairs with all POIPool data
        """
        dict = self.__dict__
        # Delete primary key before returning dict
        del dict["poi_id"]
        return dict

    def update_user_in_pool(self, user: str):
        """
        Add a new user to the pool, or update the last_seen timestamp of an existing user if they are already present

        :param user: Email of the user to add
        """
        current_timestamp = datetime.now(timezone.utc)
        if user in self.pool_data:
            try:
                self.pool_data[user]["last_seen"] = current_timestamp
            except KeyError as e:
                raise BadDataError(f"Missing data from POI Pool entry: {str(e)}")
        else:
            self.pool_data[user] = {
                "start_time": current_timestamp,
                "last_seen": current_timestamp,
            }
            self._compute_average_wait_time()

    def is_user_in_pool(self, user: str) -> bool:
        return user in self.pool_data

    def remove_user_from_pool(self, user: str):
        """
        Removes a user from the pool. Average wait time per user and total users are updated in the pool
        before removal

        :param user: Email of the user to remove
        """
        del self.pool_data[user]
        self._compute_average_wait_time()

    def _compute_average_wait_time(self) -> float:
        """Recompute current average wait time"""
        now = datetime.now(timezone.utc)

        total_seconds = 0
        for entry in self.pool_data.values():
            time_delta: timedelta = now - entry["start_time"]
            total_seconds += time_delta.seconds

        self.current_average_wait_time = (total_seconds / len(self.pool_data)) / 60
        return self.current_average_wait_time

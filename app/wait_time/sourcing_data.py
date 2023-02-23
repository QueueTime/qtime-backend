# Data classes used for sourcing will be placed here
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from common import BadDataError
from math import ceil


class POIPool:
    """
    User pool corresponding to a specific POI. Timestamps for when a user is added to a pool and when they were last
    seen are recorded for each user in the pool.
    """

    def __init__(
        self,
        poi_id: str,
        pool_data: Dict[str, Dict[str, datetime]] = {},
        average_wait_per_user: float = 0,
        total_user_count: int = 0,
    ):
        """
        :param poi_id: ID of the POI as string
        :param pool_data: Pool data dict formatted as {"user": {"start_time": datetime, "last_seen": datetime}, ...}
        :param current_average_waittime: Current average time in minutes a user spends in a pool
        :param total_user_count: The total number of users who have been in the queue during the lifetime of the pool
        """
        self.poi_id = poi_id
        self.pool_data = pool_data
        self.average_wait_per_user = average_wait_per_user
        self.total_user_count = total_user_count

    @classmethod
    def from_dict(poi_id: str, dict: Dict[str, Any]) -> "POIPool":
        """
        Create a new POIPool from a dict in the following format:
        {
            "average_wait_per_user": float,
            "total_user_count": int,
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
                average_wait_per_user=dict["average_wait_per_user"],
                total_user_count=dict["total_user_count"],
            )
        except KeyError as e:
            raise BadDataError(f"Missing data from POIPool data: {str(e)}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all properties from the POIPool

        :returns: dictionary containing key-value pairs with all POIPool data
        """
        return self.__dict__

    def get_wait_time_estimate(self) -> int:
        return ceil(self.average_wait_per_user * len(self.pool_data))

    def add_user_to_pool(self, user: str):
        """
        Add a new user to the pool

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

    def is_user_in_pool(self, user: str) -> bool:
        return user in self.pool_data

    def remove_user_from_pool(self, user: str):
        """
        Removes a user from the pool. Average wait time per user and total users are updated in the pool
        before removal

        :param user: Email of the user to remove
        """
        user_wait_data = self.pool_data[user]
        total_pool_minutes_waited = self.average_wait_per_user * self.total_user_count
        # Get outgoing user's wait time in minutes
        outgoing_user_time_delta = (
            datetime.now(timezone.utc) - user_wait_data["start_time"]
        )
        outgoing_user_wait = outgoing_user_time_delta.seconds / 60
        # Increment new total user count and update average wait per user
        self.total_user_count += 1
        self.average_wait_per_user = (
            total_pool_minutes_waited + outgoing_user_wait
        ) / self.total_user_count
        del self.pool_data[user]

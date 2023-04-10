# Service class for the Wait Time API
from typing import Optional, List
from app.firebase import firestore_db, LOCATION_COLLECTION, POI_POOL_COLLECTION
from app.user.user import User
from app.user.service import find_user, update_user
from app.wait_time.location import UserLocation
from app.locations.poi import POI
from app.events.service import generate_waittime_submit_event
from app.locations.service import get_details_for_POI
from app.rewards.reward_values import POINTS_FOR_TIME_SUBMISSION
from .sourcing_data import POIPoolEntry, POIPoolSummary, RecentWaitTime
from .errors import POIPoolNotFoundError, UserAlreadyInPoolError, UserNotInPoolError
from math import ceil
from datetime import datetime, timezone, timedelta
from app.common import BadDataError


def location_collection():
    return firestore_db().collection(LOCATION_COLLECTION)


def poi_pool_collection():
    return firestore_db().collection(POI_POOL_COLLECTION)


def uid_to_aid(uid: str) -> str:
    """
    Convert a user UID to its associated Anonymous ID (AID)

    :param uid: User's UID
    :returns: string containing user's AID
    """
    # TODO: Implement hashing of UID to generate AID
    # Temporarily just return UID as AID
    return uid


def update_location(location: UserLocation):
    """
    Update location on Firestore database

    :param location: UserLocation data to upload
    """

    location_collection().document(location.aid).set(location.to_dict())


def add_wait_time_suggestion(user: User, poi_id: str, time_estimate: int):
    """
    Add a new wait time suggestion to Firestore

    :param user: User submitting the suggestion
    :param poi_id: ID of the POI as a string
    :param time_estimate: Wait time estimate to submit
    :raises POINotFoundError: If POI ID does not exist
    """
    # TODO: Computation needs to be added here. For now it just creates an event
    # TODO: Should be a generate_waittime_confirm_event if the wait time suggestion matches current wait time
    generate_waittime_submit_event(
        user, get_details_for_POI(poi_id), time_estimate, POINTS_FOR_TIME_SUBMISSION
    )


def compute_wait_time_for_poi(poi: POI) -> int:
    """
    Compute the wait time for a specified POI in minutes

    :param poi: Specified poi to calculate wait time
    :returns: int corresponding to wait time in minutes
    """
    # TODO: Histogram and manual time submission calculations to be added to this
    # Temporarily ignore pool data and just use histogram
    # return ceil(get_wait_time_from_poi_pool(poi))
    # All wait times temporarily 0
    return 0


### POI Pool functions


def add_user_to_poi_pool(user: User, poi: POI):
    """
    Adds a user to the POIPool correpsonding to the specified POI

    :param user: User to add to pool
    :param poi: POI corresponding to desired POIPool
    :raises POIPoolNotFoundError: if there is no POIPool for the specified POI
    """
    user_current_poi = get_user_current_poi(user)
    if user_current_poi:
        if user_current_poi != poi:
            raise UserAlreadyInPoolError(user.email, user_current_poi.id)
        update_user_in_poi(user, poi)
    else:
        current_timestamp = datetime.now(timezone.utc)
        pool_entry = POIPoolEntry(user.email, current_timestamp, current_timestamp)
        _save_poi_pool_entry(poi, pool_entry)


def update_user_in_poi(user: User, poi: POI):
    """
    Updates a user's "last_seen" timestamp in their current POI pool

    :param user: User to update
    :param poi: POI to update user in
    :raises UserNotInPoolError: if user is not in specified POI pool
    """

    pool_entry = _get_poi_pool_entry(user, poi)
    pool_entry.last_seen = datetime.now(timezone.utc)
    _save_poi_pool_entry(poi, pool_entry)


def remove_user_from_poi_pool(
    user: User,
    poi: POI,
    add_to_recent_wait_times: bool = True,
    pool_entry: Optional[POIPoolEntry] = None,
):
    """
    Removes a user from the POI pool correpsonding to the specified POI

    :param user: User to remove from pool
    :param poi: POI corresponding to desired POIPool
    :param add_to_recent_wait_times: boolean specifying if the entry should be added to recent wait times or not
    :param pool_entry: POIPoolEntry that can be optionally given to prevent the entry from being needlessly fetched again
    :raises POIPoolNotFoundError: if there is no POIPool for the specified POI
    :raises UserNotInPoolError: if specified user is not in the desired pool
    """

    if add_to_recent_wait_times:
        if not pool_entry:
            pool_entry = _get_poi_pool_entry(user, poi)
        wait_time_in_minutes = (
            datetime.now(timezone.utc) - pool_entry.start_time
        ).seconds / 60
        add_recent_wait_time_to_poi(poi, wait_time_in_minutes)
    elif not pool_entry:
        wait_time_in_minutes = 0
    else:
        wait_time_in_minutes = (
            datetime.now(timezone.utc) - pool_entry.start_time
        ).seconds / 60

    # Update user statistics
    user.num_lines_participated += 1
    user.time_in_line += wait_time_in_minutes
    try:
        user.poi_frequency[poi.id] += 1
    except KeyError:
        # First time user has visited this POI, add to map
        user.poi_frequency[poi.id] = 1
    update_user(user)

    _delete_poi_pool_entry(user, poi)


def add_recent_wait_time_to_poi(
    poi: POI, wait_time: float, skip_recompute: bool = False
):
    """
    Add a recent wait time to "recent_wait_times" of a POI, and recompute a new average wait time

    :param poi: POI to update
    :param wait_time: float containing wait time in minutes to add
    """

    _add_recent_wait_time(poi, RecentWaitTime(datetime.now(timezone.utc), wait_time))

    # Compute new average wait time
    if not skip_recompute:
        _update_average_wait_time(poi, [wait_time])


def clear_stale_pool_users(poi: POI, ttl: int = 300):
    current_timestamp = datetime.now(timezone.utc)
    stale_timestamp = current_timestamp - timedelta(seconds=ttl)
    query = (
        poi_pool_collection()
        .document(poi.id)
        .collection("pool")
        .where("last_seen", "<=", stale_timestamp)
    )
    new_recent_wait_times: List[float] = []

    # Update running average for every entry removed
    for entry in query.stream():
        pool_entry: POIPoolEntry = POIPoolEntry.from_dict(entry.to_dict())
        wait_time = (current_timestamp - pool_entry.start_time).seconds / 60
        new_recent_wait_times.append(wait_time)
        remove_user_from_poi_pool(
            find_user(pool_entry.user), poi, add_to_recent_wait_times=False
        )
        add_recent_wait_time_to_poi(poi, wait_time, skip_recompute=True)

    _update_average_wait_time(poi, new_recent_wait_times)


def clear_stale_wait_times(poi: POI, ttl: int = 1800):
    current_timestamp = datetime.now(timezone.utc)
    stale_timestamp = current_timestamp - timedelta(seconds=ttl)
    query = (
        poi_pool_collection()
        .document(poi.id)
        .collection("recent_wait_times")
        .where("timestamp", "<=", stale_timestamp)
    )

    removed_wait_times: List[float] = []

    for entry in query.stream():
        wait_time_entry: RecentWaitTime = RecentWaitTime.from_dict(entry.to_dict())
        wait_time = wait_time = (
            current_timestamp - wait_time_entry.timestamp
        ).seconds / 60
        removed_wait_times.append(-wait_time)  # Negative wait times for removed times
        entry.reference.delete()

    _update_average_wait_time(poi, removed_wait_times)


def get_recent_wait_times_count_for_poi(poi: POI) -> int:
    """
    Gets the number of entries in the "recent_wait_times" colleciton for a specified POI

    :param poi: POI to get recent wait times count for
    """
    return (
        poi_pool_collection()
        .document(poi.id)
        .collection("recent_wait_times")
        .count()
        .get()[0][0]
        .value
    )


def get_wait_time_from_poi_pool(poi: POI) -> float:
    """
    Gets the estimated wait time from POIPool data

    :param poi: POI to calculate pool wait time for
    :returns: float corresponding to average wait time in minutes
    """
    pool_summary = _get_poi_pool_summary(poi)
    return pool_summary.current_average_wait_time


def get_user_current_poi(user: User) -> Optional[POI]:
    """
    Gets a POIPool that the specified user is participating in

    :param user: User to search for in pools
    :returns: POI that User is participating in, None if there is none
    """
    query = firestore_db().collection_group("pool").where("user", "==", user.email)
    result = query.get()
    # Raise an error if the user is in more than one pool at once (we should know about this)
    assert len(result) < 2
    if result:
        return get_details_for_POI(result[0].reference.parent.parent.id)

    return None


def _add_recent_wait_time(poi: POI, recent_wait_time: RecentWaitTime):

    poi_pool_collection().document(poi.id).collection("recent_wait_times").add(
        recent_wait_time.to_dict()
    )


def _get_poi_pool_summary(poi: POI) -> POIPoolSummary:
    pool_ref = poi_pool_collection().document(poi.id)
    pool_data = pool_ref.get().to_dict()
    if not pool_data:
        raise POIPoolNotFoundError(poi.id)
    return POIPoolSummary.from_dict(pool_data)


def _update_average_wait_time(poi: POI, new_wait_times: List[float]):
    recent_wait_time_count = get_recent_wait_times_count_for_poi(poi)
    pool_summary = _get_poi_pool_summary(poi)
    total_wait_time_minutes = (
        pool_summary.current_average_wait_time * recent_wait_time_count
    ) + sum(new_wait_times)
    if recent_wait_time_count:
        new_average = total_wait_time_minutes / recent_wait_time_count
    else:
        new_average = 0
    pool_summary.current_average_wait_time = new_average
    _update_poi_pool_summary(pool_summary, poi)


def _update_poi_pool_summary(pool_summary: POIPoolSummary, poi: POI):
    poi_pool_collection().document(poi.id).set(pool_summary.to_dict())


def _delete_poi_pool_entry(user: User, poi: POI):
    poi_pool_collection().document(poi.id).collection("pool").document(
        user.email
    ).delete()


def _get_poi_pool_entry(user: User, poi: POI) -> POIPoolEntry:
    pool_entry_ref = (
        poi_pool_collection().document(poi.id).collection("pool").document(user.email)
    )
    pool_entry_data = pool_entry_ref.get().to_dict()
    if not pool_entry_data:
        raise UserNotInPoolError(user.email, poi.id)
    return POIPoolEntry.from_dict(pool_entry_data)


def _save_poi_pool_entry(poi: POI, pool_entry: POIPoolEntry):
    poi_pool_collection().document(poi.id).collection("pool").document(
        pool_entry.user
    ).set(pool_entry.to_dict())

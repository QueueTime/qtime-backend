# Service class for the Wait Time API
from typing import Optional
from app.firebase import firestore_db, LOCATION_COLLECTION, POI_POOL_COLLECTION
from app.user.user import User
from app.wait_time.location import UserLocation
from app.locations.poi import POI
from app.events.service import generate_waittime_submit_event
from app.locations.service import get_details_for_POI
from app.rewards.reward_values import POINTS_FOR_TIME_SUBMISSION
from .sourcing_data import POIPool
from .errors import POIPoolNotFoundError
from math import ceil


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
    :returns:
    """
    # TODO: Histogram and manual time submission calculations to be added to this
    return ceil(compute_wait_time_from_poi_pool(poi))


### POI Pool functions
def get_pool_for_poi(poi: POI) -> POIPool:
    """
    Fetches a POIPool from a specified POI

    :param poi: POI corresponding to desired POIPool
    :returns: POIPool corresponding to specified POI
    :raises POIPoolNotFoundError: if there is no POIPool for the specified POI
    """
    return _get_pool_for_poi_id(poi.id)


def save_poi_pool(pool: POIPool):
    """
    Saves a POIPool to Firestore

    :param pool: POIPool to save
    """
    poi_pool_collection().document(pool.poi_id).set(pool.to_dict())


def add_user_to_poi_pool(user: User, poi: POI):
    """
    Adds a user to the POIPool correpsonding to the specified POI

    :param user: User to add to pool
    :param poi: POI corresponding to desired POIPool
    :raises POIPoolNotFoundError: if there is no POIPool for the specified POI
    """
    poi_pool: POIPool = get_pool_for_poi(poi)
    poi_pool.update_user_in_pool(user.email)
    save_poi_pool(poi_pool)


def remove_user_from_poi_pool(user: User, poi: POI):
    """
    Removes a user from the POIPool correpsonding to the specified POI

    :param user: User to remove from pool
    :param poi: POI corresponding to desired POIPool
    :raises POIPoolNotFoundError: if there is no POIPool for the specified POI
    :raises UserNotInPoolError: if specified user is not in the desired pool
    """
    poi_pool: POIPool = get_pool_for_poi(poi)
    poi_pool.remove_user_from_pool(user.email)
    save_poi_pool(poi_pool)


def compute_wait_time_from_poi_pool(poi: POI) -> float:
    """
    Computes the wait time estimated from POIPool data

    :param poi: POI to calculate pool wait time for
    :returns: float corresponding to average wait time in minutes
    """
    poi_pool: POIPool = get_pool_for_poi(poi)
    return poi_pool.current_average_wait_time


def get_user_current_poi_pool(user: User) -> Optional[POIPool]:
    """
    Gets a POIPool that the specified user is participating in

    :param user: User to search for in pools
    :returns: POIPool that User is participating in, None if there is none
    """
    query = poi_pool_collection().where(f"pool.{user.email}", "!=", "")
    result = query.get()
    # Raise an error if the user is in more than one pool at once (we should know about this)
    assert len(result) < 2
    if result:
        return _get_pool_for_poi_id(result[0].id)

    return None


def _get_pool_for_poi_id(poi_id: str) -> POIPool:
    pool_ref = poi_pool_collection().document(poi_id).get()
    if not pool_ref.exists:
        raise POIPoolNotFoundError(poi_id)
    return POIPool.from_dict(poi_id, pool_ref.to_dict())

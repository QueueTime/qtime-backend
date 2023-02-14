# Service class for the Wait Time API

from app.firebase import firestore_db, LOCATION_COLLECTION
from app.user.user import User
from app.wait_time.location import Location
from app.events.service import generate_waittime_submit_event
from app.locations.poi.service import get_details_for_POI
from app.rewards.reward_values import POINTS_FOR_TIME_SUBMISSION


def location_collection():
    return firestore_db().collection(LOCATION_COLLECTION)


def uid_to_aid(uid: str) -> str:
    """
    Convert a user UID to its associated Anonymous ID (AID)

    :param uid: User's UID
    :returns: string containing user's AID
    """
    # TODO: Implement hashing of UID to generate AID
    # Temporarily just return UID as AID
    return uid


def update_location(location: Location):
    """
    Update location on Firestore database

    :param location: Location data to upload
    """

    location_collection().document(location.aid).set(location.to_dict())


def add_wait_time_suggestion(user: User, poi_id: str, time_estimate: int):
    """
    Add a new wait time suggestion to Firestore
    """
    # TODO: Computation needs to be added here. For now it just creates an event
    # TODO: Should be a generate_waittime_confirm_event if the wait time suggestion matches current wait time

    generate_waittime_submit_event(
        user, get_details_for_POI(poi_id), time_estimate, POINTS_FOR_TIME_SUBMISSION
    )

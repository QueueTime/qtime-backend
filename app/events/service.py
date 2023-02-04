from app.firebase import firestore_db, EVENTS_COLLECTION
from app.user_api.user_api import User
from .event import (
    Event,
    EventType,
    WaitTimeSubmitPayload,
    WaitTimeConfirmPayload,
    RewardPointsAddPayload,
    RewardSource,
)
from app.poi_api.poi import POI


def generate_account_signup_event(user: User):
    """
    Generate an event for when a user signs up for the first time.

    :param user: The user who signed up
    """
    _save_to_events_collection(Event(EventType.ACCOUNT_SIGNUP, user.email))


def generate_account_delete_event(user: User):
    """
    Generate an event for when a user deletes their account.

    :param user: The user who deleted their account
    """
    _save_to_events_collection(Event(EventType.ACCOUNT_DELETION, user.email))


def generate_waittime_submit_event(
    user: User, poi: POI, estimate_submitted: int, points_awarded: int
):
    """
    Generate an event for when a user submits a wait time estimate.

    :param user: User who submitted the wait time estimate
    :param poi: POI that the user submitted the wait time estimate for
    :param estimate_submitted: Estimate submitted by the user
    :param points_awarded: Number of points awarded to the user for submitting the wait time estimate
    """
    _save_to_events_collection(
        Event(
            EventType.WAITTIME_SUBMIT,
            user.email,
            payload=WaitTimeSubmitPayload(estimate_submitted, poi._id),
        )
    )
    _generate_reward_point_change_event(
        user.email, RewardSource.WAITTIME_SUBMIT, points_awarded
    )


def generate_waittime_confirm_event(user: User, poi: POI, points_awarded: int):
    """
    Generate an event for when a user confirms a wait time estimate.

    :param user: User who confirmed the wait time estimate
    :param poi: POI that the user confirmed the wait time estimate for
    :param points_awarded: Number of points awarded to the user for confirming the wait time estimate
    """
    _save_to_events_collection(
        Event(
            EventType.WAITTIME_CONFIRM,
            user.email,
            payload=WaitTimeConfirmPayload(poi._id),
        )
    )
    _generate_reward_point_change_event(
        user.email, RewardSource.WAITTIME_CONFIRM, points_awarded
    )


def generate_referral_event(
    user: User, user_with_referral_code: User, points_awarded: int
):
    """
    Generate an event when a user signs up using a referral code.

    :param user: User who signed up using a referral code
    :param user_with_referral_code: User who's referral code was used
    :param points_awarded: Number of points awarded to both users
    """
    _generate_reward_point_change_event(
        user.email, RewardSource.REFERRED_BONUS, points_awarded
    )
    _generate_reward_point_change_event(
        user_with_referral_code.email, RewardSource.REFERRAL_BONUS, points_awarded
    )


def _generate_reward_point_change_event(
    email: str, source: RewardSource, points_change: int
):
    """
    Generate a general point change event.

    :param email: Email of the user who's points are being added
    :param source: Source of the reward points being added
    :param points_change: Number of points being added or subtracted
    """
    _save_to_events_collection(
        Event(
            EventType.REWARD_POINTS_ADD,
            email,
            payload=RewardPointsAddPayload(source, points_change),
        )
    )


def _save_to_events_collection(event: Event):
    """
    Save an event to the events collection in Firestore.

    :param event: Event to save
    """
    firestore_db.collection(EVENTS_COLLECTION).add(event.to_dict())

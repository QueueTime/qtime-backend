from datetime import datetime
from typing import Optional
from firebase_admin._user_mgt import UserRecord
import re

from app.common import SimpleMap, BadDataError
from app.events.service import find_all_reward_events_for_user, generate_referral_event
from app.auth import with_auth_user
from app.events.event import Event
from app.user_api.user_service import find_user_by_referral_code, find_user, update_user
from app.user_api.errors import UserNotFoundError
from .errors import ReferralCodeNotFound, InvalidReferralOperation

POINTS_FOR_REFERRAL = 200


class RewardEventApiResponse(SimpleMap):
    def __init__(self, source: str, points: int, timestamp: datetime):
        self.source = source
        self.points = points
        self.timestamp = timestamp

    @staticmethod
    def from_event(event: Event) -> "RewardEventApiResponse":
        return RewardEventApiResponse(
            event.payload.source.value, event.payload.points_change, event.created
        )


@with_auth_user
def submit_referral_code(user: UserRecord, code: str, **kwargs):
    if not re.match(r"^[A-Z]{6}$", code):
        err_msg = "Invalid referral code format, must be 6 capital letters."
        return BadDataError(err_msg).jsonify(), 400

    try:
        referred_user = find_user(user.email)
    except UserNotFoundError:
        err_msg = f"User with email {user.email} not found."
        return InvalidReferralOperation(err_msg).jsonify(), 404

    if referred_user.hasCompletedOnboarding:
        err_msg = "User has already completed onboarding. Cannot use referral code after onboarding."
        return InvalidReferralOperation(err_msg).jsonify(), 400

    try:
        user_with_code = find_user_by_referral_code(code)
    except UserNotFoundError:
        err_msg = f"User with referral code {code} not found."
        ReferralCodeNotFound(err_msg).jsonify(), 404

    if user_with_code.email == referred_user.email:
        err_msg = "Invalid operation. Refer refer yourself."
        return InvalidReferralOperation(err_msg).jsonify(), 400

    referred_user.reward_point_balance += POINTS_FOR_REFERRAL
    user_with_code.reward_point_balance += POINTS_FOR_REFERRAL

    update_user(referred_user)
    update_user(user_with_code)
    generate_referral_event(referred_user, user_with_code, POINTS_FOR_REFERRAL)

    return None, 204


@with_auth_user
def list_reward_events(
    user: UserRecord, before: Optional[str] = None, limit: int = 30, **kwargs
):
    """
    API endpoint to list reward events for a user. Returns a list of reward events in reverse chronological order.

    :param user: Firebase user record of the user to list reward events for
    :param before: Optional datetime query param to start listing reward events before
    :param limit: Optional limit query param to limit the number of reward events returned
    :return: List of reward events for the user
    """
    if limit > 100:
        return BadDataError("Limit cannot be greater than 100").jsonify(), 400

    try:
        before_datetime = (
            datetime.strptime(before, "%Y-%m-%dT%H:%M:%S.%fZ") if before else None
        )
    except ValueError as e:
        return BadDataError(str(e)).jsonify(), 400

    return [
        RewardEventApiResponse.from_event(e).to_dict()
        for e in find_all_reward_events_for_user(user.email, limit, before_datetime)
    ], 200

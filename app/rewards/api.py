from datetime import datetime
from typing import Optional
import re

from app.common import SimpleMap, BadDataError
from app.events.service import find_all_reward_events_for_user, generate_referral_event
from app.auth import with_auth_user
from app.events.event import Event
from app.user.service import find_user_by_referral_code, find_user, update_user
from app.user.errors import UserNotFoundError
from app.user.user import User
from .errors import ReferralCodeNotFound, InvalidReferralOperation
from .reward_values import POINTS_FOR_REFERRAL


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
def submit_referral_code(user: User, code: str, **kwargs):
    if not re.match(r"^[A-Z]{6}$", code):
        err_msg = "Invalid referral code format, must be 6 capital letters."
        return BadDataError(err_msg).buildError()

    if user.hasCompletedOnboarding:
        err_msg = "User has already completed onboarding. Cannot use referral code after onboarding."
        return InvalidReferralOperation(err_msg).buildError()

    if user.hasUsedReferralCode:
        err_msg = (
            "User has already used a referral code. Cannot use multiple referral codes."
        )
        return InvalidReferralOperation(err_msg).buildError()

    try:
        user_with_code = find_user_by_referral_code(code)
    except UserNotFoundError:
        err_msg = f"User with referral code {code} not found."
        return ReferralCodeNotFound(err_msg).buildError()

    if user_with_code.email == user.email:
        err_msg = "Invalid operation. Cannot refer to yourself."
        return InvalidReferralOperation(err_msg).buildError()

    user.reward_point_balance += POINTS_FOR_REFERRAL
    user.hasUsedReferralCode = True
    user_with_code.reward_point_balance += POINTS_FOR_REFERRAL

    update_user(user)
    update_user(user_with_code)
    generate_referral_event(user, user_with_code, POINTS_FOR_REFERRAL)

    return None, 204


@with_auth_user
def list_reward_events(
    user: User, before: Optional[str] = None, limit: int = 30, **kwargs
):
    """
    API endpoint to list reward events for a user. Returns a list of reward events in reverse chronological order.

    :param user: Firebase user record of the user to list reward events for
    :param before: Optional datetime query param to start listing reward events before
    :param limit: Optional limit query param to limit the number of reward events returned
    :return: List of reward events for the user
    """
    if limit > 100:
        return BadDataError("Limit cannot be greater than 100").buildError()

    try:
        before_datetime = (
            datetime.strptime(before, "%Y-%m-%dT%H:%M:%S.%fZ") if before else None
        )
    except ValueError as e:
        return BadDataError(str(e)).buildError()

    return [
        RewardEventApiResponse.from_event(e).to_dict()
        for e in find_all_reward_events_for_user(user.email, limit, before_datetime)
    ], 200

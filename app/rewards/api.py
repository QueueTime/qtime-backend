from datetime import datetime
from typing import Optional
from firebase_admin._user_mgt import UserRecord

from app.common import SimpleMap, BadDataError
from app.events.service import find_all_reward_events_for_user
from app.auth import with_auth_user
from app.events.event import Event


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
def submit_referral_code(user: UserRecord, code: str):
    print(code)


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

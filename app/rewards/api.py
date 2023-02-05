from datetime import datetime
from typing import Optional

from app.common import SimpleMap, BadDataError
from app.events.service import find_all_reward_events_for_user


class RewardEventApiResponse(SimpleMap):
    def __init__(self, source: str, points: int):
        self.source = source
        self.points = points


def submit_referral_code(code):
    print(code)


# TODO: Add token and user finding logic
def list_reward_events(before: Optional[str] = None):
    try:
        before_datetime = (
            datetime.strptime(before, "%Y-%m-%dT%H:%M:%S.%fZ") if before else None
        )
    except ValueError as e:
        return BadDataError(str(e)).jsonify(), 400

    return [
        e.to_dict()
        for e in find_all_reward_events_for_user("A@test.com", before_datetime)
    ], 200

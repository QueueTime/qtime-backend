from enum import Enum
from datetime import datetime, timezone
from typing import Dict, Any
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from app.common import SimpleMap


class EventType(Enum):
    """Types of events logged"""

    ACCOUNT_SIGNUP = "account_signup_event"
    ACCOUNT_DELETION = "account_delete_event"
    WAITTIME_SUBMIT = "waittime_submit_event"
    WAITTIME_CONFIRM = "waittime_confirm_event"
    REWARD_POINTS_ADD = "reward_points_add_event"
    REWARD_REDEMPTION = "reward_redemption_event"


class RewardSource(Enum):
    """Ways users can earn rewards points"""

    REFERRAL_BONUS = "referral_bonus"  # For users who referred new users
    REFERRED_BONUS = "referred_bonus"  # For new users who were referred
    WAITTIME_CONFIRM = "waittime_confirm"
    WAITTIME_SUBMIT = "waittime_submit"


class WaitTimeSubmitPayload(SimpleMap):
    """Payload for wait time submission event"""

    def __init__(self, estimate_submitted: int, poi_id: str):
        """
        :param estimate_submitted: The wait time estimate submitted by the user
        :param poi_id: The id of the POI that the user submitted the wait time for
        """
        self.estimate_submitted = estimate_submitted
        self.poi_id = poi_id


class WaitTimeConfirmPayload(SimpleMap):
    """Payload for the wait time confirmation event"""

    def __init__(self, poi_id: str):
        """
        :param poi_id: The id of the POI that the user confirmed the wait time for
        """
        self.poi_id = poi_id


class RewardPointsAddPayload:
    def __init__(self, source: RewardSource, points_change: int):
        """
        :param source: The source of the reward points earned by the user
        :param points_change: The +/- change in reward points
        """
        self.source = source
        self.points_change = points_change

    def to_dict(self):
        return {
            "source": self.source.value,
            "points_change": self.points_change,
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return RewardPointsAddPayload(
            RewardSource(dict["source"]), dict["points_change"]
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, RewardPointsAddPayload)
            and self.to_dict() == other.to_dict()
        )

    def __repr__(self):
        return f"RewardPointsAddPayload(source={self.source}, points_change={self.points_change})"


# TODO: Implement Reward redemption events upon implementing of reward redemption
class RewardRedemptionPayload:
    pass


class Event:
    def __init__(
        self,
        type: EventType,
        user: str,
        payload: Any = None,
        created: datetime = datetime.now(timezone.utc),
    ):
        """
        Tracking Event used for logging of user actions in the app.

        :param type: Event type
        :param user: The id of the user that caused the event
        :param payload: Additional data associated with the event
        :param created: Datetime event was created
        """
        self.type = type
        self.user = user
        self.payload = payload
        self.created = created

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "user": self.user,
            "payload": self.payload.to_dict() if self.payload is not None else None,
            "created": self.created,
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Event":
        """Parse a dict into an Event object"""
        event_type = EventType(dict["type"])

        if event_type == EventType.WAITTIME_SUBMIT:
            payload = WaitTimeSubmitPayload.from_dict(dict["payload"])
        elif event_type == EventType.WAITTIME_CONFIRM:
            payload = WaitTimeConfirmPayload.from_dict(dict["payload"])
        elif event_type == EventType.REWARD_POINTS_ADD:
            payload = RewardPointsAddPayload.from_dict(dict["payload"])
        else:  # (EventType.ACCOUNT_SIGNUP, EventType.ACCOUNT_DELETION)
            payload = None

        if type(dict["created"]) == DatetimeWithNanoseconds:
            created = datetime.fromtimestamp(dict["created"].timestamp())
        else:
            created = dict["created"]

        return Event(event_type, dict["user"], payload, created)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Event) and self.to_dict() == other.to_dict()

    def __hash__(self):
        return hash((self.type, self.user, self.payload, self.created))

    def __repr__(self):
        return f"Event(type={self.type}, user={self.user}, payload={self.payload}, created={self.created})"

###
# Common classes and utility methods used throughout the entire application
###

from abc import ABC, abstractmethod, abstractclassmethod
from firebase_admin import auth
from .user.errors import UserAuthenticationError
from werkzeug.exceptions import Unauthorized
import json


class FirebaseDataEntity(ABC):
    """
    Base class for data classes to be used wth Firestore.
    """

    def __init__(self):
        """
        Initialize new data instance. Additional parameters should be added to child classes
        for any needed fields.
        """

    @abstractclassmethod
    def from_dict(dict):
        """Class function that creates a new data class from a Python dictionary"""
        raise NotImplementedError("Base class cannot be used")

    def to_json(self):
        """Return all properties in a JSON string"""
        return json.dumps(self.to_dict())

    @abstractmethod
    def to_dict(self):
        """Return all properties in a Python dict"""
        raise NotImplementedError("Base class cannot be used")

    @abstractmethod
    def __eq__(self, other):
        """Compares equality by looking at primary keys"""
        raise NotImplementedError("Base class cannot be used")


class BadDataError(Exception):
    """Used when receiving unexpected data from Firebase or clients"""

    def __init__(self, message):
        super().__init__(message)


def decode_token(token):
    """
    Decodes a JWT token using Firebase

    Args:
        token: A string of the encoded JWT

    Returns:
        dict: A dictionary of the key-value pairs from the decoded JWT

    Raises:
        Unauthorized: if the token is invalid or expired
        ValueError: if `token` is not a string or is empty
    """
    try:
        return auth.verify_id_token(token)
    except (
        auth.InvalidIdTokenError,
        auth.ExpiredIdTokenError,
    ) as e:
        raise Unauthorized("Invalid token") from e

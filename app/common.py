###
# Common classes and utility methods used throughout the entire application
###

from abc import ABC, abstractmethod, abstractclassmethod
from firebase_admin import auth
from user_api.errors import UserAuthenticationError
import json


class FirebaseDataEntity(ABC):
    """
    Base class for data classes to be used wth Firestore. Supports both fetching an entity
    from Firestore by ID or pushing/updating a new entity on the remote database
    """

    def __init__(self, db_ref):
        """
        Initialize new data instance with a specified CollectionReference. Additional parameters should be added to child classes
        for any needed fields.
        """
        self.db_reference = db_ref

    @abstractclassmethod
    def get(db_ref, id):
        """Class function that fetches a specified entity from a given Firebase reference by ID and creates a new Python instance"""
        raise NotImplementedError("Base class cannot be used")

    @abstractclassmethod
    def from_dict(dict):
        """Class function that creates a new data class from a Python dictionary"""
        raise NotImplementedError("Base class cannot be used")

    @abstractmethod
    def push(self):
        """Pushes data to Firebase"""
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
        UserAuthenticationError: if an error occurs authenticating the token
        ValueError: if `token` is not a string or is empty
    """
    try:
        return auth.verify_id_token(token)
    except (
        auth.InvalidIdTokenError,
        auth.ExpiredIdTokenError,
        auth.CertificateFetchError,
    ) as e:
        raise UserAuthenticationError(str(e)) from e

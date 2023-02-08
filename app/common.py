###
# Common classes and utility methods used throughout the entire application
###

from abc import ABC, abstractmethod, abstractclassmethod
import json
from typing import Dict, Any

from app.base_api_error import BaseApiError


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


class BadDataError(BaseApiError):
    """Used when receiving unexpected data from Firebase or clients"""

    def __init__(self, message):
        super().__init__(message, 400)


class SimpleMap:
    """If an object has a simple mapping allow it to be converted to a dict straight from its attributes"""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return SimpleMap(**dict)

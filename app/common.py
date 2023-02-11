###
# Common classes and utility methods used throughout the entire application
###

from abc import ABC, abstractmethod, abstractclassmethod
import json
from typing import Dict, Any

from app.base_api_error import BaseApiError


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

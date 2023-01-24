# Common classes and utility methods used by POI API

from abc import ABC, abstractmethod


class POIApi(ABC):
    @abstractmethod
    def get_all_POI(self):
        """List all points of interests in the POI Collection"""
        raise NotImplementedError("Base class cannot be used")

    @abstractmethod
    def get_POI(self, poi_id):
        """Returns the object of a single POI specified"""
        raise NotImplementedError("Base class cannot be used")

    @abstractmethod
    def suggest_new_POI():
        """Allows client to suugest a new POI to be added to the POI Collection"""
        raise NotImplementedError("Base class cannot be used")

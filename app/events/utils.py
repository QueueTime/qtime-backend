from typing import Dict, Any


class SimpleMap:
    """If an object has a simple mapping allow it to be converted to a dict straight from its attributes"""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

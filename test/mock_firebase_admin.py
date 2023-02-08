from unittest.mock import Mock
import sys
import types
from typing import Any

module_name = "firebase_admin"
firebase_admin: Any = types.ModuleType(module_name)
sys.modules[module_name] = firebase_admin
firebase_admin.firestore = Mock(name=module_name + ".firestore")
firebase_admin.auth = Mock(name=module_name + ".auth")

from unittest.mock import Mock
import sys
import types
from typing import Any

# Mocks the firebase_admin module
#
# Usage
# Add this import line *above* any modules that would import firebase_admin
# from test.mock_firebase_admin import firebase_admin # Mock firebase_admin module
#
# Add to this file as needed for additional methods and attributes on the module

module_name = "firebase_admin"
firebase_admin: Any = types.ModuleType(module_name)
sys.modules[module_name] = firebase_admin
firebase_admin.firestore = Mock(name=module_name + ".firestore")
firebase_admin.auth = Mock(name=module_name + ".auth")

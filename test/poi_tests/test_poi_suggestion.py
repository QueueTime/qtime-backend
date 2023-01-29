# run with: python -m unittest test/poi_tests/test_poi_suggestion.py
import unittest
from app.poi_api.poi_suggestion import POI_suggestions


class TestPOI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.poi_suggestion = POI_suggestions(
            pid="0",
            suggestion_name="Petting Zoo",
            notes="Goat baa",
            submission_time="23:00",
            submitted_by="Bob Alice",
        )

    def test_get_pid(self):
        self.assertEqual(self.poi_suggestion.get_pid(), "0")

    def test_to_dict(self):
        poi_suggestion_dict = {
            "_pid": "0",
            "suggestion_name": "Petting Zoo",
            "notes": "Goat baa",
            "submission_time": "23:00",
            "submitted_by": "Bob Alice",
        }
        self.assertEquals(self.poi_suggestion.to_dict(), poi_suggestion_dict)

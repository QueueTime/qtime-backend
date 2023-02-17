import unittest
from app.locations.poi_suggestion import POI_suggestion


class TestPOI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.poi_suggestion = POI_suggestion(
            pid="0",
            suggestion_name="Test",
            notes="Test",
            submission_time="23:00",
            submitted_by="alice@gmail.com",
        )
        self.poi_suggestion_dict = {
            "_pid": "0",
            "suggestion_name": "Test",
            "notes": "Test",
            "submission_time": "23:00",
            "submitted_by": "alice@gmail.com",
        }

    # def test_to_dict(self):
    #     self.assertEquals(self.poi_suggestion.to_dict(), self.poi_suggestion_dict)

    def test_from_dict(self):
        self.assertEquals(
            POI_suggestion.from_dict(self.poi_suggestion_dict), self.poi_suggestion
        )

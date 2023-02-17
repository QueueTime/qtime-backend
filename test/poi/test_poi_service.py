# import unittest
# from unittest.mock import patch, ANY, call, MagicMock
# from app.locations.service import list_POI
# from app.locations.poi_suggestion import POI_suggestion
# from app.locations.errors import POINotFoundError, InvalidPOISuggestionError
# from app.user.api import User
# from app.locations.poi import POI


# @patch("app.locations.service.firestore_db")
# class TestPOIService(unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.email = "test@sample.ca"
#         self.poi_id = "SAMPLE_POI"
#         self.points_awarded = 25
#         self.user = User(self.email, "XJFEKDG", 0)
#         self.poi = POI(
#             self.poi_id, "Testing poi", "Testing", None, None, None, None, None
#         )
#         self.sample_poi_dict = {
#             "_id": "test",
#             "address": "123 test dr.",
#             "class": "EATERY",
#             "hours_of_operation": {"Monday": "0"},
#             "image_url": "https://test.com",
#             "location": {"longitude": "0", "latitude": "0"},
#             "name": "Test",
#             "type": "queue",
#         }

#     def test_list_POI(self, firebase_mock):
#         firebase_mock().document().get().to_dict = MagicMock(
#             return_value=self.sample_poi_dict
#         )
#         self.assertEqual(self.sample_poi_dict, list_POI())

#     def test_get_POI(self):
#         pass

#     def test_get_POI_POINotFoundError(self):
#         pass

#     # TODO: Update test as ID is no longer returned
#     # Testing that poi suggestion has been added to the data base by checking matching id
#     # def test_suggest_new_POI(self):
#     #     poi_suggestion_id = self.poi_service.suggest_new_POI(self.poi_suggestion)[
#     #         "poi_suggestion_id"
#     #     ]
#     #     self.poi_suggestion_id = poi_suggestion_id
#     #     get_poi_suggestion = (
#     #         self.poi_sug_ref.document(poi_suggestion_id).get().to_dict()
#     #     )
#     #     self.assertEqual(self.poi_suggestion_id, get_poi_suggestion["_pid"])

#     # def test_suggest_new_POI_InvalidPOISuggestionError(self):
#     #     with self.assertRaises(InvalidPOISuggestionError):
#     #         poi_suggestion_error = {
#     #             "submitted_by": "P-body and Atlas",
#     #         }
#     #         self.poi_service.suggest_new_POI(poi_suggestion_error)

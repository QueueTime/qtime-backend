import unittest
from test.mixins import FlaskTestClientMixin


class TestBaseApi(unittest.TestCase, FlaskTestClientMixin):
    @classmethod
    def setUpClass(self):
        FlaskTestClientMixin.setUpClass()

    def setUp(self):
        return super().setup_rest_defaults()

    def test_health(self):
        response = self.client.get(f"{self.base_url}/health")
        assert response.status_code == 200

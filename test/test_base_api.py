import unittest
from test.mixins.flask_client_mixin import FlaskTestClientMixin


class TestBaseApi(unittest.TestCase, FlaskTestClientMixin):
    @classmethod
    def setUpClass(self):
        self.with_test_flask_client(self)

    def setUp(self):
        return self.with_rest_defaults()

    def test_health(self):
        response = self.client.get(f"{self.base_url}/health")
        assert response.status_code == 200

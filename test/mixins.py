import connexion
from manage import start_server

flask_app = start_server("TestFlaskApp")


class FlaskTestClientMixin:
    """
    Mixin for testing rest requests with a flask app.

    Usage:
        class MyTest(unittest.TestCase, FlaskTestClientMixin):
            @classmethod
            def setUpClass(self):
                FlaskTestClientMixin.setUpClass()

            def setUp(self):
                return super().setup_rest_defaults()

            def test_x(self):
                response = self.client.get(f"{self.base_url}/my-endpoint")
                # Response is a werkzeug.wrappers.response.Response object: https://werkzeug.palletsprojects.com/en/2.2.x/wrappers/#werkzeug.wrappers.Response
    """

    @classmethod
    def setUpClass(self):
        self.client = flask_app.app.test_client()

    def setup_rest_defaults(self):
        self.base_url = "/api"

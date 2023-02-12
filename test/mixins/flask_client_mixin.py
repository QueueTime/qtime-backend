from setup import start_server


class FlaskTestClientMixin:
    """
    Mixin for testing rest requests with a flask app.

    Usage:
        class MyTest(unittest.TestCase, FlaskTestClientMixin):
            @classmethod
            def setUpClass(self):
                self.with_test_flask_client(self)

            def setUp(self):
                return self.with_rest_defaults()

            def test_x(self):
                response = self.client.get(f"{self.base_url}/my-endpoint")
                # Response is a werkzeug.wrappers.response.Response object: https://werkzeug.palletsprojects.com/en/2.2.x/wrappers/#werkzeug.wrappers.Response
    """

    def with_test_flask_client(self):
        flask_app = start_server("TestFlaskApp")
        self.client = flask_app.app.test_client()

    def with_rest_defaults(self):
        self.base_url = "/api"

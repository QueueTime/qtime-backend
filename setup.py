import connexion
from utils import combine_specifications
from firebase_admin import credentials, initialize_app
from app.error_handlers import handle_base_api_error, handle_generic_exception
from app.base_api_error import BaseApiError
from werkzeug.exceptions import HTTPException

FIREBASE_CERT_PATH = "serviceAccountKey.json"

# Initializing Firestore database
def initialize_firebase(cert_path: str):
    initialize_app(credentials.Certificate(cert_path))


def start_server(name: str):
    app = connexion.App(name)
    # Tell app to read the combined openapi specification
    app.add_api(
        combine_specifications(
            "./base_swagger.yaml",
            "./app/locations/spec.yaml",
            "./app/user/spec.yaml",
            "./app/rewards/spec.yaml",
            "./app/wait_time/spec.yaml",
        )
    )
    # Register error handlers
    app.add_error_handler(BaseApiError, handle_base_api_error)
    app.add_error_handler(Exception, handle_generic_exception)

    return app

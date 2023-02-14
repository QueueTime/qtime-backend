import connexion
from utils import combine_specifications
from firebase_admin import credentials, initialize_app

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
            "./app/poi_api/spec.yaml",
            "./app/user/spec.yaml",
            "./app/rewards/spec.yaml",
        )
    )
    return app

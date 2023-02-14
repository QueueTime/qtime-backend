import connexion
from utils import combine_specifications
from firebase_admin import credentials, initialize_app


# Initializing Firestore database
# Can import firestore_db to utilize database
def initialize_firebase():
    initialize_app(credentials.Certificate("serviceAccountKey.json"))


initialize_firebase()
app = connexion.App(__name__)
# Tell app to read the combined openapi specification
app.add_api(
    combine_specifications(
        "./base_swagger.yaml",
        "./app/locations/spec.yaml",
        "./app/user/spec.yaml",
        "./app/rewards/spec.yaml",
    )
)


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    app.run(debug=True)

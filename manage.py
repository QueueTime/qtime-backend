import os

from setup import initialize_firebase, start_server, FIREBASE_CERT_PATH


initialize_firebase(FIREBASE_CERT_PATH)
app = start_server(__name__)


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    env = os.environ.get("ENV", "dev")
    if env == "prod":
        # Run the app in production mode with waitress.
        from waitress import serve

        serve(app, host="0.0.0.0", port=5000)
    elif env == "dev":
        app.run(debug=True)
    else:
        raise Exception("Unsupported environment, must one of [dev, prod].")

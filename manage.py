from setup import initialize_firebase, start_server, FIREBASE_CERT_PATH

initialize_firebase(FIREBASE_CERT_PATH)
app = start_server(__name__)


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    app.run(debug=True)

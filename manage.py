import connexion
from utils import combine_specifications

app = connexion.App(__name__)
# Tell app to read the combined openapi specification
app.add_api(
    combine_specifications(
        "./base_swagger.yaml",
        "./app/poi_api/spec.yaml",
        "./app/user_api/spec.yaml",
        "./app/rewards/spec.yaml",
    )
)


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    app.run(debug=True)

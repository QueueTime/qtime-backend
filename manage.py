import connexion
from utils import combine_specifications
from pathlib import Path

app = connexion.App(__name__)
# Telling app to read the combined openapi specification
app.add_api(
    combine_specifications(
        Path("./base_swagger.yaml"),
        Path("./app/poi_api/spec.yaml"),
        Path("./app/user_api/spec.yaml"),
    )
)


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    app.run(debug=True)

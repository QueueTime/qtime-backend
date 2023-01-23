import connexion

# connecting swagger.yml configuration file with the Flask app
# specification_dir tells Connexion which directory to look for the config file
app = connexion.App(__name__, specification_dir="./")
# Telling app to read the swagger.yml file from specification_dir
app.add_api("swagger.yml")


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    app.run(debug=True)

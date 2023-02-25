<h1 align="center">
  <img src="https://avatars.githubusercontent.com/u/116905733?s=200&v=4" height="200"/><br>
  QTime Mobile Application
</h1>

<h4 align="center">Cross-platform wait time tracking mobile application</h4>

<blockquote align="center">
  <em>QTime (QueueTime)</em> is a mobile application designed to track wait times and occupancy levels for services across McMaster's campus to help students plan their day.
</blockquote>

# qtime-backend

Python flask backend for the QTime system.

## Getting Started

- Clone the project: `git clone https://github.com/QueueTime/qtime-backend.git`

### Setup the server

- Create a virtual environment: `python3 -m venv env`
- Activate the virtual environment: `activate env/bin/activate`
- Install the required packages: `python3 -m pip install -r requirements.txt`

**Note**: At any if you wish to deactivate the virtual environment run `deactivate`.

### Add your Firebase service key

This project uses Firebase APIs to communicate with the Firestore database and manage authentication. In order to connect to Firebase we need to generate a private service key.

To generate a private key file for your service account:

- In the Firebase console, open Settings > [Service Accounts](https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk).
- Select "Python" as the target admin SDK and click _Generate new private key_.
- Copy the contents of the downloaded JSON file and replace the contents of the [serviceAccount.sample.json](./serviceAccount.sample.json) file. Rename the file to `serviceAccountKey.json`.

**Note**: This service account key is **private** and should not be shared.

## Dependencies

This project manages many external dependencies. If adding or removing dependencies update the [requirements.txt](./requirements.txt) file by running

```sh
python3 -m pip freeze > requirements.txt
```

### API Specification

This project leverages [Connexion](https://pypi.org/project/connexion/) as a framework to manage http requests based on OpenAPI specifications.

### Linting

This project leverages the opinionated [Black](https://github.com/psf/black) formatter for code formatting and [mypy](https://mypy.readthedocs.io/en/stable/) for static typechecking.

## Testing

This project leverages [Unittest](https://docs.python.org/3/library/unittest.html) as a unit testing framework to run tests.

Run the following commands to test a module

```
python -m unittest tests/test_target.py
```

The full instructions for testing with the command line are found in the [Unittest documentation](https://docs.python.org/3/library/unittest.html#command-line-interface).

### Testing with Firebase Emulators

In order to test functionality that connects to firebase we use firebase emulators to emulate a firebase instance.

- Follow the [install steps](https://firebase.google.com/docs/emulator-suite/install_and_configure#install_the_local_emulator_suite) to setup firebase emulators.
  - Run `firebase --version` to ensure you installed the firebase cli.
- Setup the firestore emulator with the following command

```
firebase setup:emulators:firestore
```

- Start the emulators with the command

```
firebase emulators:start --only firestore,auth --project qtime-bd47e --import=./sample_firebase_data
```

- You should now be able to visit the [firestore emulator UI](http://127.0.0.1:4000/firestore) and [firebase auth emulator UI](http://127.0.0.1:4000/auth) pages.

- Export the following environment variables before running the flask app

```
export FIRESTORE_EMULATOR_HOST="localhost:8080"
export FIREBASE_AUTH_EMULATOR_HOST="localhost:9099"
```

- Fetch a user authentication token by making a POST http call:

```
POST http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=key

{
  "email": "<USER_EMAIL>",
  "password": "<PASSWORD>"
}
```

- Export data from the firebase emulator with the command. The emulator must be running.

```
firebase emulators:export ./sample_firebase_data --project qtime-bd47e
```

### Firebase Utility Script

The firebase utility script is used to simplify management tasks for Firebase and the Firestore database. It is located in `scripts/manage_firebase.py`. Currently, the following command line arguments are supported:

- `--add-pois`: Update the `POI` collection on Firestore with a list of POI data given in a file in JSON format. Example:

```
python manage_firebase.py --add-pois ./pois.json
```

- `--add-property`, `--remove-property`: These options will add a new field to every document in a collection or remove a field from all documents in a collection respectively. To add a new property, the following syntax is used:

```
--add-property collection_path=<COLLECTION_PATH> name=<FIELD_NAME> type=[string | number | boolean | map | array | timestamp] value=<VALUE>
```

Example commands:

```
python manage_firebase.py --remove-property collection_path=users name=hasCompletedOnboarding
```

This will delete the `hasCompletedOnboarding` field from all documents in the users collection.

```
python manage_firebase.py --add-property collection_path=users name=has_completed_onboarding type=boolean value=true
```

This will add a new boolean field to all documents in the users collection called `has_completed_onboarding` with a default value of true.

Command line help for the utility is also available by providing the `-h` or `--help` argument.

## Deploying

The QTime backend is deployed to [AWS Lightsail](https://aws.amazon.com/lightsail/) automatically on push to master using the `Deploy` workflow. The steps to manually deploy are below:

1. Install [Docker](https://docs.docker.com/engine/install/), [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and the [Lightsail Plugin](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-install-software) if you haven't already.
2. Create a docker image of the backend with

```
docker build -t qtime-container .
```

Note: (You can run this image as a container with `docker run -p 5000:5000 qtime-container`)

3. Push the image to AWS Lightsail

```
aws lightsail push-container-image \
  --service-name qtime \
  --label qtime-latest  \
  --image qtime-container:latest
```

This will return information about the image you just pushed, take note of container number assigned. It should look like `qtime.qtime-latest.X`.

4. Deploy your container to AWS Lightsail, replacing the image name in the command below.

```
aws lightsail create-container-service-deployment \
  --service-name qtime \
  --containers "{
    "flask": {
      "image": "qtime.qtime-latest.X",
      "ports": {
        "5000": "HTTP"
      }
    }
  }" \
  --public-endpoint "{
    "containerName": "flask",
    "containerPort": 5000,
    "healthCheck": {
      "path": "/api/health",
      "successCodes": "200"
    }
  }"
```

5. It will take a few minutes for the new deployment to finish. Once finished you should be able to access https://queuetime.tech/api/health to verify the service is up.

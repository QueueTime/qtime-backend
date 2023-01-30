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

### Formatting

This project leverages the opinionated [Black](https://github.com/psf/black) formatter for code formatting.

## Testing

This project leverages [Unittest](https://docs.python.org/3/library/unittest.html) as a unit testing framework to run tests.

Run the following commands to test a module

```
python -m unittest tests/test_target.py
```

The full instructions for testing with the command line are found in the [Unittest documentation](https://docs.python.org/3/library/unittest.html#command-line-interface).

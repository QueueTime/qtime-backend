import os
from typing import Callable, Dict, Any, Optional
import requests

from setup import initialize_firebase, FIREBASE_CERT_PATH
from app.firebase import (
    firestore_db,
    USERS_COLLECTION,
    EVENTS_COLLECTION,
    REFERRAL_CODES_COLLECTION,
)
from app.user.user import User

FIRESTORE_PROJECT_ID = "qtime-bd47e"

# AUTH CONSTANTS
FIRESTORE_AUTH_EMULATOR_HOST = "localhost:9099"
AUTH_SIGNUP_URL = f"http://{FIRESTORE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:signUp"
AUTH_SIGNIN_URL = f"http://{FIRESTORE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
AUTH_DELETE_ALL_URL = f"http://{FIRESTORE_AUTH_EMULATOR_HOST}/emulator/v1/projects/{FIRESTORE_PROJECT_ID}/accounts"
USER_PASSWORD = "password"

# FIRESTORE CONSTANTS
FIRESTORE_EMULATOR_HOST = "localhost:8080"
FIRESTORE_DELETE_ALL_URL = f"http://{FIRESTORE_EMULATOR_HOST}/emulator/v1/projects/{FIRESTORE_PROJECT_ID}/databases/(default)/documents"


class FirebaseTestMixin:
    """Mixin for testing with Firebase."""

    def with_firebase_emulators(self):
        """
        Initialize the firebase app connection and set env variables to use emulators.
        """
        os.environ["FIRESTORE_EMULATOR_HOST"] = FIRESTORE_EMULATOR_HOST
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = FIRESTORE_AUTH_EMULATOR_HOST
        initialize_firebase(FIREBASE_CERT_PATH)

    def with_user_accounts(self, *users: User) -> Dict[str, Callable]:
        """
        Creates users in firebase auth & users collection for testing.

        Note: Firebase Auth will lower case all emails when creating user accounts.

        :param users: Iterable of users to create
        :returns: Dictionary of user emails to functions to fetch user auth tokens
        """
        token_fetchers: Dict[str, Callable] = {}

        for user in users:
            _create_user_in_firebase_auth_emulator(
                user.email, USER_PASSWORD, user.email
            )
            _create_document_in_collection(USERS_COLLECTION, user.to_dict(), user.email)
            token_fetchers[user.email] = lambda: _fetch_user_auth_token(
                user.email, USER_PASSWORD
            )
        return token_fetchers

    def clear_all_documents_in_collection(self, collection_name: str):
        """
        Clear all documents in a collection.

        :param collection_name: Name of collection to clear
        """
        collection = firestore_db().collection(collection_name)
        for doc in collection.stream():
            doc.reference.delete()

    def clear_all_firestore_data(self):
        """Clears all data in the firestore emulator."""
        requests.delete(
            FIRESTORE_DELETE_ALL_URL, headers={"Authorization": "Bearer owner"}
        )

    def delete_user_accounts(self):
        """Clears all user accounts in the firebase auth emulator."""
        requests.delete(AUTH_DELETE_ALL_URL, headers={"Authorization": "Bearer owner"})


def _create_user_in_firebase_auth_emulator(
    email: str, password: str, display_name: str
):
    """
    Creates a user in the firebase auth emulator.

    :param email: Email of user to create
    :param password: Password of user to create
    :param display_name: Display name of user to create
    """
    requests.post(
        AUTH_SIGNUP_URL,
        json={
            "email": email,
            "password": password,
            "displayName": display_name,
        },
        headers={"Authorization": "Bearer owner"},
    )


def _fetch_user_auth_token(email: str, password) -> str:
    """
    Fetch an auth token for a user in the firebase auth emulator.

    :param email: Email of user to fetch token for
    :returns: Auth token for user
    """
    r = requests.post(
        AUTH_SIGNIN_URL,
        json={"email": email, "password": password},
        headers={"Authorization": "Bearer owner"},
    )
    return r.json()["idToken"]


def _create_document_in_collection(
    collection_name: str,
    data: Dict[str, Any],
    document_id: Optional[str] = None,
):
    """
    Creates a document in a collection in the firebase emulator.

    :param collection: Collection to create document in
    :param document: Document to create
    :param data: Document data
    :throws ValueError: If collection is not supported for testing
    """
    ref = firestore_db().collection(collection_name)
    if document_id:
        ref.document(document_id).set(data)
    else:
        ref.add(data)

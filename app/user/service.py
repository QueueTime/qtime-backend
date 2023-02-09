# This file contains service functions for the user API
from app.user.user import User
from app.user.errors import UserNotFoundError, UserAlreadyExistsError
from app.rewards.service import (
    create_unique_referral_code,
    save_referral_code,
    delete_referral_code,
)
from app.events.service import (
    generate_account_signup_event,
    generate_account_delete_event,
)
from app.firebase import firestore_db, USERS_COLLECTION

users_collection = firestore_db.collection(USERS_COLLECTION)


def find_user(email: str) -> User:
    """Given email, find and return corresponding User. Raises UserNotFoundError if user not found

    :param email: A string of the target user email
    :returns: An associated User object with the specified email
    :raises UserNotFoundError: if user with specified email does not exist
    :raises BadDataError: if user data retrieved is missing essential data
    """
    user_ref = users_collection.document(email).get()
    if not user_ref.exists:
        raise UserNotFoundError(email)
    return User.from_dict(email, user_ref.to_dict())


def find_user_by_referral_code(referral_code: str) -> User:
    """Given referral code, find and return corresponding User. Raises UserNotFoundError if user not found

    :param referral_code: A string of the target user referral code
    :returns: An associated User object with the specified referral code
    :raises UserNotFoundError: if user with specified referral code does not exist
    :raises BadDataError: if user data retrieved is missing essential data
    """
    user_ref = users_collection.where("referral_code", "==", referral_code).get()
    if not user_ref:
        raise UserNotFoundError(referral_code)
    return User.from_dict(user_ref[0].id, user_ref[0].to_dict())


def create_user(email: str) -> User:
    """
    Creates a new user with a specified email

    :param email: email of new user to create
    :returns: User object associated with the new user
    :raises UserAlreadyExists: if a user with the specified email already exists in the database
    """
    if users_collection.document(email).get().exists:
        raise UserAlreadyExistsError(email)

    new_user = User(email=email, referral_code=create_unique_referral_code())
    save_referral_code(new_user.referral_code)
    update_user(new_user)
    generate_account_signup_event(new_user)
    return new_user


def update_user(user: User):
    """Push updated User object to Firestore"""
    users_collection.document(user.email).set(user.to_dict(), merge=True)


def delete_user(user: User):
    """
    Deletes a specified user

    :param user: User object for target user to delete
    :raises UserNotFoundError: If target user does not exist
    """
    target_user_snapshot = users_collection.document(user.email)
    if not target_user_snapshot.get().exists:
        raise UserNotFoundError(user.email)
    target_user_snapshot.delete()
    delete_referral_code(user.referral_code)
    generate_account_delete_event(user)

    # TODO if there are any other references to the user that need to be deleted from other places,
    # add them here


def update_notification(user, setting):
    """Updates notification preference for specfied user"""
    user.notification_setting = setting
    update_user(user)

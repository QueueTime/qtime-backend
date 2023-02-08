# This file contains service functions for the user API
from app.user.User import User
from app.user.errors import UserNotFoundError, UserAuthenticationError
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


def update_user(user: User):
    """Push updated User object to Firestore"""
    users_collection.document(user.email).set(user.to_dict(), merge=True)


def get_points(user: User):
    """Returns user's reward points balance"""
    return user.reward_point_balance


def get_POI_frequency(user: User):
    """Return POI object"""
    pass  # TODO


def get_num_lines_participated(user: User):
    """Returns number of lines participated in by a User"""
    return user.num_lines_participated


def get_total_line_time(user: User):
    """Return total time in line spent by User as an integer"""
    return user.time_in_line


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
    # TODO if there are any other references to the user that need to be deleted from other places,
    # add them here


def update_notification(user, setting):
    """Updates notification preference for specfied user"""
    user.notification_setting = setting
    update_user(user)

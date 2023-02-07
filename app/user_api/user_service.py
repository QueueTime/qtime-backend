# This file contains service functions for the user API
from app.user_api.User import User
from app.user_api.errors import UserNotFoundError, UserAuthenticationError
from app.firebase import firestore_db, USERS_COLLECTION

users_collection = firestore_db.collection(USERS_COLLECTION)


class User_Service:
    """This is the service class for the User API"""

    def findUser(self, email: str) -> User:
        """Given email, find and return corresponding User. Raises UserNotFoundError if user not found

        :param email: A string of the target user email
        :returns: An associated User object with the specified email
        :raises UserNotFoundError: if user with specified email does not exist
        :raises BadDataError: if user data retrieved is missing essential data
        """
        user_ref = users_collection.document(email).get()
        if not user_ref.exists:
            raise UserNotFoundError(email)
        return User.from_dict(user_ref.to_dict())

    def updateUser(self, user: User):
        """Push updated User object to Firestore"""
        users_collection.document(user.email).set(user.to_dict(), merge=True)

    def getPoints(self, user: User):
        """Returns user's reward points balance"""
        return user.reward_point_balance

    def getPOIFrequency(self, user: User):
        """Return POI object"""
        pass  # TODO

    def getNumLinesParticipated(self, user: User):
        """Returns number of lines participated in by a User"""
        return user.num_lines_participated

    def getTotalLineTime(self, user: User):
        """Return total time in line spent by User as an integer"""
        return user.time_in_line

    def deleteUser(self, user: User):
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

    def updateNotification(self, user, setting):
        """Updates notification preference for specfied user"""
        user.notification_setting = setting
        self.updateUser(user)

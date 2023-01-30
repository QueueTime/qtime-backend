# This file contains service functions for the user API
from app.user_api.User import User
from app.user_api.errors import UserNotFoundError, UserAuthenticationError
from firebase_admin import firestore

class User_Service():
    ''' This is the service class for the User API'''
    def __init__(self):
        self.users_ref = firestore.client().collection('users')
    

    def findUser(self, email):
        '''Given email, find and return corresponding User. Raises UserNotFoundError if user not found'''
        return User.get(self.users_ref, email)

    def updateUser(self, user):
        '''Push updated User object to Firestore'''
        user.push()

    def getPoints(self, user):
        '''Returns user's reward points balance'''
        return user.reward_point_balance

    def getPOIFrequency(self, user):
        '''Return POI object '''
        pass    # TODO

    def getNumLinesParticipated(self, user):
        '''Returns number of lines participated in by a User'''
        return user.num_lines_participated

    def getTotalLineTime(self ,user):
        '''Return total time in line spent by User as an integer'''
        return user.time_in_line

    def deleteUser(self, user):
        ''' Deletes a specified user'''
        target_user_snapshot = self.users_ref.document(user.email)
        if not target_user_snapshot.get().exists:
            raise UserNotFoundError(user.email)
        target_user_snapshot.delete()
        # TODO if there are any other references to the user that need to be deleted from other places,
        # add them here

    def changeTheme(self, user, theme):
        '''Updates theme for a specified User'''
        user.color_theme = theme
        user.push()

    def updateNotification(user, setting):
        '''Updates notification preference for specfied user'''
        user.notification_setting = setting
        user.push()
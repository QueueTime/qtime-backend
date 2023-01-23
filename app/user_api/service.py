# This file contains service functions for the user API
from app.user_api.User import User
from app.user_api.errors import UserNotFoundError, UserAuthenticationError
from firebase_admin import firestore

users_ref = firestore.client().collection('users')

def findUser(email):
    '''Given email, find and return corresponding User. Raises UserNotFoundError if user not found'''
    return User.get(users_ref, email)

def updateUser(user):
    '''Push updated User object to Firestore'''
    user.push()

def getPoints(user):
    '''Returns user's reward points balance'''
    return user.reward_point_balance

def getPOIFrequency(user):
    '''Return POI object '''
    pass    # TODO

def getNumLinesParticipated(user):
    '''Returns number of lines participated in by a User'''
    return user.num_lines_participated

def getTotalLineTime(user):
    '''Return total time in line spent by User as an integer'''
    return user.time_in_line

def signInUser(user):
    '''Signs in a specified User'''
    pass    # TODO

def signOutUser(user):
    '''Signs out a specified user'''
    pass    # TODO

def deleteUser(user):
    ''' Deletes a specified user'''
    target_user = users_ref.document(user.email).get()
    if not target_user.exists:
        raise UserNotFoundError(user.email)
    target_user.delete()
    # TODO if there are any other references to the user that need to be deleted from other places,
    # add them here

def changeTheme(user, theme):
    '''Updates theme for a specified User'''
    user.color_theme = theme
    user.push()

def updateNotification(user, setting):
    '''Updates notification preference for specfied user'''
    user.notification_setting = setting
    user.push()
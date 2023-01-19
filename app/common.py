###
# Common classes and utility methods used throughout the entire application
###

import json

# Base class for data classes
class FirebaseDataEntity:
    '''
    Base class for data classes to be used wth Firestore. Supports both fetching an entity 
    from Firestore by ID or pushing/updating a new entity on the remote database
    '''
    def __init__(self, db_ref):
        '''
        Initialize new data instance with a specified CollectionReference. Additional parameters should be added to child classes
        for any needed fields.
        '''
        self.db_reference = db_ref

    def get(db_ref, id):
        ''' Class function that fetches a specified entity from a given Firebase reference by ID and creates a new Python instance '''
        raise NotImplementedError("Base class cannot be used")

    def push(self):
        ''' Pushes data to Firebase '''
        raise NotImplementedError("Base class cannot be used")

    def to_json(self):
        ''' Return all properties in a JSON string '''
        json.dump(self.to_dict())

    def to_dict(self):
        ''' Return all properties in a Python dict '''
        raise NotImplementedError("Base class cannot be used")
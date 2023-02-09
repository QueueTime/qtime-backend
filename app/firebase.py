from firebase_admin import firestore

EVENTS_COLLECTION = "events"
USERS_COLLECTION = "users"
REFERRAL_CODES_COLLECTION = "referral_codes"

firestore_db = firestore.client()

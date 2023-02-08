from firebase_admin import firestore

EVENTS_COLLECTION = "events"
USERS_COLLECTION = "users"
REFERRAL_CODES_COLLECTION = "referral_codes"

# # Initializing Firestore database
# # Can import firestore_db to utilize database
# cred = credentials.Certificate("serviceAccountKey.json")
# default_app = initialize_app(cred)
firestore_db = firestore.client()

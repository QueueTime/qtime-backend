from firebase_admin import firestore

EVENTS_COLLECTION = "events"
USERS_COLLECTION = "users"
REFERRAL_CODES_COLLECTION = "referral_codes"
POI_COLLECTION = "POI"
POI_PROPOSAL_COLLECTION = "POI_proposal"


def firestore_db():
    return firestore.client()

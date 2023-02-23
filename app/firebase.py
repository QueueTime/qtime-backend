from firebase_admin import firestore

EVENTS_COLLECTION = "events"
USERS_COLLECTION = "users"
REFERRAL_CODES_COLLECTION = "referral_codes"
LOCATION_COLLECTION = "location"
POI_COLLECTION = "POI"
POI_PROPOSAL_COLLECTION = "POI_proposal"
POI_POOL_COLLECTION = "poi_pool"


def firestore_db():
    return firestore.client()

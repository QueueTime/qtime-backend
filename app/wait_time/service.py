# Service class for the Wait Time API

from app.firebase import firestore_db, POI_QUEUE_COLLECTION

poi_queue_collection = firestore_db.collection(POI_QUEUE_COLLECTION)

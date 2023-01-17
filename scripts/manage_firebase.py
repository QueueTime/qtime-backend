import firebase_admin
from firebase_admin import credentials, firestore
import argparse
import json
import os

DEFAULT_FIREBASE_KEY_PATH = "../app/key/serviceAccountKey.json"

# Add new command line arguments here
parser = argparse.ArgumentParser()
parser.add_argument('--add-poi', metavar='poi_json_path', required=True)
parser.add_argument('--firebase-key', '-k', default=DEFAULT_FIREBASE_KEY_PATH) # Required for now
parser = parser.parse_args()

# Connect to Firebase using given key
firebase_key_path = parser.firebase_key
if not os.path.exists(firebase_key_path):
    print(f"Missing private key for Firestore database ({firebase_key_path} missing)")
    exit(1)

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add new POI from given JSON file
poi_json_path = parser.add_poi
with open(poi_json_path, 'r') as json_file:
    poi_dict = json.loads(json_file.read())
    new_poi_ref = db.collection('POI').document(poi_dict["_id"])
    new_poi_ref.set(poi_dict, merge=True)


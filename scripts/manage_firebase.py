import firebase_admin
from firebase_admin import credentials, firestore
import argparse
from typing import Any, Dict, List
from sys import argv
import json
import os
from datetime import datetime, timezone

DEFAULT_FIREBASE_KEY_PATH = "../serviceAccountKey.json"
FIREBASE_FIELD_TYPES = [
    "string",
    "number",
    "boolean",
    "map",
    "array",
    "timestamp",
]


def parse_list_args_to_dict(args: List[str]) -> Dict[str, Any]:
    """
    Given list of properties in format key=value, return dict in format {"key": value}

    :param args: list of properties
    :returns: dict containing key-value pairs
    """
    new_dict = {}
    for arg in args:
        arg_split = arg.split("=")
        new_dict[arg_split[0]] = arg_split[1]
    return new_dict


def parse_value_with_type(value: str, type: str) -> Any:
    """
    Parse a given string value into a specified type (given as a string)

    :param value: value to parse
    :param type: type to parse into
    :returns: value parsed into specified type
    :raises ValueError: If value cannot be parsed into type
    """
    if type == "number":
        return float(value)
    elif type == "boolean":
        if value.lower() == "false":
            return False
        else:
            return True
    elif type == "map" or type == "array":
        return json.loads(value)
    elif type == "timestamp":
        if value == "now":
            return datetime.now(timezone.utc)
        else:
            return datetime.fromisoformat(value)


# Add new command line arguments here
parser = argparse.ArgumentParser()
parser.add_argument("--add-pois", metavar="poi_json_path")
parser.add_argument("--add-wait-time-base", metavar="wait_time_base_json_path")
parser.add_argument(
    "--add-wait-time-histogram", metavar="wait_time_histogram_json_path"
)
parser.add_argument("--firebase-key", "-k", default=DEFAULT_FIREBASE_KEY_PATH)
parser.add_argument(
    "--add-property",
    metavar="",
    help=f"""
    Adds a new field to all documents in a specified collection. Usage:
    manage_firebase.py --add-property 
    collection_path=<COLLECTION_PATH> name=<FIELD_NAME> type=[{' | '.join(FIREBASE_FIELD_TYPES)}]
    value=<VALUE>
    """,
    nargs=4,
)
parser.add_argument(
    "--remove-property",
    metavar="",
    help="""
    Deletes a specified field from all documents in a specified collection. Usage:
    manage_firebase.py --remove-property
    collection_path=<COLLECTION_PATH> name=<FIELD_NAME>
    """,
    nargs=2,
)
args = parser.parse_args()

# Connect to Firebase using given key
firebase_key_path = args.firebase_key
if not os.path.exists(firebase_key_path):
    print(f"Missing private key for Firestore database ({firebase_key_path} missing)")
    exit(1)

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add new wait time base document given JSON file
wait_time_base_json_path = args.add_wait_time_base
# Add new wait time histogram
wait_time_histogram_json_path = args.add_wait_time_histogram
# Add new POI from given JSON file
poi_json_path = args.add_pois
if poi_json_path:
    try:
        with open(poi_json_path, "r") as json_file:
            poi_list = json.loads(json_file.read())
            for poi in poi_list:
                new_poi_ref = db.collection("POI").document(poi["_id"])
                new_poi_ref.set(poi, merge=True)
    except FileNotFoundError as e:
        print(e)
        quit(1)
# Add wait time base collection
elif wait_time_base_json_path:
    try:
        with open(wait_time_base_json_path, "r") as json_file:
            wait_time_base_list = json.loads(json_file.read())
            for wait_time_poi in wait_time_base_list:
                new_wait_time_poi_ref = db.collection("histogram").document(
                    wait_time_poi["poi_name"]
                )
                new_wait_time_poi_ref.set(wait_time_poi, merge=True)
    except FileNotFoundError as e:
        print(e)
        quit(1)
# Add wait time histograms
elif wait_time_histogram_json_path:
    try:
        with open(wait_time_histogram_json_path, "r") as json_file:
            wait_time_histogram_list = json.loads(json_file.read())
            for wait_time_hist in wait_time_histogram_list:
                poi_name = wait_time_hist["poi_name"]
                day_key = wait_time_hist["day"]
                new_wait_time_hist_ref = (
                    db.collection("histogram")
                    .document(poi_name)
                    .collection("histogram_data")
                    .document(day_key)
                )
                new_wait_time_hist_ref.set(wait_time_hist, merge=True)
    except FileNotFoundError as e:
        print(e)
        quit(1)
elif args.add_property:
    options = parse_list_args_to_dict(args.add_property)
    if options["type"] not in FIREBASE_FIELD_TYPES:
        print("Unknown data type:", options["type"])
        quit(1)
    try:
        value = parse_value_with_type(options["value"], options["type"])
        name = options["name"]
        collection_path = options["collection_path"]
    except KeyError as e:
        print("Missing option:", str(e))
        quit(1)
    document_list = db.collection(collection_path).stream()
    print(f"Updating all documents in {collection_path}...")
    documents_updated = 0
    for document in document_list:
        print(f"Updated {documents_updated} documents.", end="\r")
        new_document = document.to_dict()
        new_document[name] = value
        db.collection(collection_path).document(document.id).set(
            new_document, merge=True
        )
        documents_updated += 1
    print(
        f'\nSuccessfully added the property {name}: "{str(value)}" to all documents in {collection_path}'
    )
elif args.remove_property:
    options = parse_list_args_to_dict(args.remove_property)
    try:
        collection_path = options["collection_path"]
        name = options["name"]
    except KeyError as e:
        print("Missing option:", str(e))
        quit(1)
    document_list = db.collection(collection_path).stream()
    print(f"Updating all documents in {collection_path}...")
    documents_updated = 0
    for document in document_list:
        print(f"Updated {documents_updated} documents.", end="\r")
        new_document = document.to_dict()
        try:
            del new_document[name]
        except KeyError:
            continue  # Ignore if document already does not have the field
        db.collection(collection_path).document(document.id).set(new_document)
        documents_updated += 1
    print(
        f'\nSuccessfully deleted the "{name}" field from all documents in {collection_path}'
    )
else:
    parser.print_help()

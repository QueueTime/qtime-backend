from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app

EVENTS_COLLECTION = "events"

# Initializing Firestore database
# Can import firestore_db to utilize database
cred = credentials.Certificate("serviceAccountKey.json")
default_app = initialize_app(cred)
firestore_db = firestore.client()

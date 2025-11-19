import firebase_admin
from firebase_admin import credentials, firestore
import os

cred = credentials.Certificate('sjcj-firebase.json')  # Mets ton fichier JSON ici
firebase_admin.initialize_app(cred)

db = firestore.client()
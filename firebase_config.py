import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Sur Vercel → on prend la clé depuis l’environnement (SÉCURISÉ)
if os.getenv('FIREBASE_SERVICE_ACCOUNT'):
    service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
    cred = credentials.Certificate(service_account_info)
# Sur ton ordi en local → fallback sur le fichier (pratique pour tester)
elif os.path.exists('sjcj-firebase-key.json'):
    cred = credentials.Certificate('sjcj-firebase-key.json')
else:
    raise Exception("Firebase : aucune clé trouvée – ajoute FIREBASE_SERVICE_ACCOUNT sur Vercel ou le fichier local")

# Initialise une seule fois
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firebase CONNECTÉ EN MODE RÉEL – tout est bon !!")
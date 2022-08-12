import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json


def init_db():
    PRIVATE_KEY_ID_FS = os.environ.get('PRIVATE_KEY_ID_FS')
    PRIVATE_KEY_FS = os.environ.get('PRIVATE_KEY_FS').replace('\\n', '\n')
    CLIENT_EMAIL_FS = os.environ.get('CLIENT_EMAIL_FS')
    CLIENT_ID_FS = os.environ.get('CLIENT_ID_FS')

    # Use a service account
    cred = credentials.Certificate(
        {
        "type": "service_account",
        "project_id": "findremote",
        "private_key_id": PRIVATE_KEY_ID_FS,
        "private_key": PRIVATE_KEY_FS,
        "client_email": CLIENT_EMAIL_FS,
        "client_id": CLIENT_ID_FS,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-p9cw7%40findremote.iam.gserviceaccount.com"
        }
    )

    firebase_admin.initialize_app(cred)
    
    return firestore.client()



def get_listings(db):
    listings = db.collection(u'listings_light').stream()

    return [listing.to_dict() for listing in listings]



def get_listing(db, job_id):
    listing = db.collection(u'listings').document(job_id).get().to_dict()

    return listing




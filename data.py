import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import os
import json



def time_diff(listing_time, current_time):
    diff_sec = current_time - listing_time

    if diff_sec < 3600:
        diff = '1h'
    elif diff_sec < 86400:
        hours = str(int(diff_sec/3600))
        diff = hours + 'h'
    else:
        days = str(int(diff_sec/86400))
        diff = days + 'd'
    
    return diff



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



def get_listings(db, role=None, start_after=None, end_before=None, limit=20, forwards='True'):

    query_ref = db.collection(u'listings').where('status', '==', 'active')

    # if role is filtered
    query_filtered = query_ref.where(role, '==', True) if role != None else query_ref    

    # pagination
    if forwards == 'True':
        if start_after != None:
            query_sliced = query_filtered.where('unix_timestamp', '<', int(start_after))
        else:
            query_sliced = query_filtered

        query_ordered = query_sliced.order_by('unix_timestamp', direction=firestore.Query.DESCENDING)
        
        listings = query_ordered.limit(limit).get()
    
    else:
        """
        # it should have worked as follows but due to firestore bug it doesn't
        # https://github.com/googleapis/python-firestore/issues/536
        query_ordered = query_filtered.order_by('unix_timestamp')
        query_sliced = query_ordered.end_before({'unix_timestamp': end_before})
        listings = query_sliced.limit_to_last(limit).get()
        listings.reverse()
        """

        query_sliced = query_filtered.where('unix_timestamp', '>', int(end_before))
        query_ordered = query_sliced.order_by('unix_timestamp')
        listings = query_ordered.limit(limit-1).get()
        listings.reverse()
    
    # format docs as dict
    listings_formated = [listing.to_dict() for listing in listings]

    # add listings age
    current_time = int(time.time())
    for listing in listings_formated:
        listing['age'] = time_diff(listing['unix_timestamp'], current_time)

    return listings_formated



def get_listing(db, job_id):
    listing = db.collection(u'listings').document(job_id).get().to_dict()

    return listing




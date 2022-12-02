import os, os.path

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtubepartner"
    ]
CLIENT_SECRETS_FILE = 'client_secrets.json'


def get_authenticated_service():
    creds = None
    # Access and refresh tokens are stored in token.pickle.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def deauthentication():
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
    else:
        print("File not found.")
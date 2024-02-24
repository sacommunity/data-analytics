from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
import os

# Define OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
CLIENT_SECRETS_FILE = './credentials/credentials.json'
# Set up the OAuth 2.0 flow

# Start the OAuth 2.0 Authorization Flow

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
creds = flow.run_local_server(port=0)
with open('./credentials/token.json', 'w') as token:
    token.write(creds.to_json())
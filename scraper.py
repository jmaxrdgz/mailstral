from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import base64
from email import message_from_bytes

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, max_results=10):
    # Email list
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        parts = payload.get('parts', [])
        email_data = {}
        
        # Headers
        for header in headers:
            if header['name'] == 'From':
                email_data['From'] = header['value']
            if header['name'] == 'To':
                email_data['To'] = header['value']
            if header['name'] == 'Subject':
                email_data['Subject'] = header['value']
        
        # Content
        if 'body' in payload and 'data' in payload['body']:
            email_data['Body'] = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        elif parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    email_data['Body'] = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        print(email_data)

if __name__ == '__main__':
    service = authenticate_gmail()
    fetch_emails(service)

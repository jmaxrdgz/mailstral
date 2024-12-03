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
    # Email list (filter to 'SENT' emails)
    results = service.users().messages().list(userId='me', labelIds=['SENT'], maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        parts = payload.get('parts', [])
        email_data = {}
        
        # Headers (From, To, Subject, In-Reply-To)
        for header in headers:
            if header['name'] == 'From':  # Sender
                email_data['From'] = header['value']
            if header['name'] == 'To':  # Recipient
                email_data['To'] = header['value']
            if header['name'] == 'Subject':  # Subject
                email_data['Subject'] = header['value']
            if header['name'] == 'In-Reply-To':  # Email being replied to
                email_data['In-Reply-To'] = header['value']
        
        # Thread
        thread_id = msg.get('threadId')
        thread = service.users().threads().get(userId='me', id=thread_id).execute()
        
        # Received body
        received_body = ''
        for msg_in_thread in thread['messages']:
            if msg_in_thread['id'] != message['id']:  # Skip the sent message itself
                received_payload = msg_in_thread.get('payload', {})
                if 'body' in received_payload and 'data' in received_payload['body']:
                    received_body = base64.urlsafe_b64decode(received_payload['body']['data']).decode('utf-8')
                elif 'parts' in received_payload:
                    for part in received_payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            received_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
        
        # Sent body
        sent_body = ''
        if 'body' in payload and 'data' in payload['body']:
            sent_body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        elif parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    sent_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

        # Print email details
        print("Sent Email Details:")
        print(f"From: {email_data.get('From', 'N/A')}")
        print(f"To: {email_data.get('To', 'N/A')}")
        print(f"Subject: {email_data.get('Subject', 'N/A')}")
        print(f"In-Reply-To: {email_data.get('In-Reply-To', 'N/A')}")
        print(f"Sent Email Body: {sent_body if sent_body else 'No body content'}")
        print(f"Received Email Body: {received_body if received_body else 'No received body'}")
        print("-" * 40)

if __name__ == '__main__':
    service = authenticate_gmail()
    fetch_emails(service)


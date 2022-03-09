# import the required libraries
from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import base64
import email
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from os.path import join, dirname
from twilio.rest import Client
from dotenv import dotenv_values
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

tw_dotenv_path = join(dirname(__file__), "twilio.env")
dotenv_values(tw_dotenv_path)
twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_auth = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(twilio_sid, twilio_auth)
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
  
    service = build('gmail', 'v1', credentials=creds)
  
    result = service.users().messages().list(userId='me', labelIds=["INBOX"], q="is:unread").execute()
  
    messages = result.get('messages', [])

    if not messages:
        message = client.messages.create(body="You have no new messages",
                                         from_="+15203412910",
                                         to="+19032461634")
    else:
        message_count= 0
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute
            message_count = message_count + 1
        message = client.messages.create(body="You have " + str(message_count) + " new messages",
                                         from_="+15203412910",
                                         to="+19032461634")
  
if __name__ == '__main__':
    main()
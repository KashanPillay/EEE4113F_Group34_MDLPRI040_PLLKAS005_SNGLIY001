import os
import pickle
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
OPENED_EMAILS_FILE = "opened_emails.txt"


def authenticate_gmail():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def get_email_body(msg_data):
    if 'data' in msg_data['payload']['body']:
        return base64.urlsafe_b64decode(msg_data['payload']['body']['data']).decode()
    if 'parts' in msg_data['payload']:
        for part in msg_data['payload']['parts']:
            if 'body' in part and 'data' in part['body']:
                return base64.urlsafe_b64decode(part['body']['data']).decode()
    return None


def get_subject(msg_data):
    headers = msg_data['payload']['headers']
    for header in headers:
        if header['name'] == 'Subject':
            return header['value']
    return None


def load_opened_emails():
    if os.path.exists(OPENED_EMAILS_FILE):
        with open(OPENED_EMAILS_FILE, "r") as file:
            return set(file.read().splitlines())
    return set()


def save_opened_email(email_id):
    with open(OPENED_EMAILS_FILE, "a") as file:
        file.write(email_id + "\n")


def get_emails(only_opened=False):
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])
    opened_emails = load_opened_emails()
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        subject = get_subject(msg_data)
        email_body = get_email_body(msg_data)
        email_id = msg["id"]

        if subject and email_body:
            emails.append((email_id, subject, email_body))
            if not only_opened:
                save_opened_email(email_id)

    if only_opened:
        emails = [email for email in emails if email[0] in opened_emails]

    return emails


if __name__ == "__main__":
    check_gmail()

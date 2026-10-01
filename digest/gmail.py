import base64
from pathlib import Path

from django.core.mail.backends.base import BaseEmailBackend
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import AuthorizedSession, Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SEND_URL = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'
TIMEOUT = 30


class GmailAuthRequired(Exception):
    pass


def authorize(client_file, token_file):
    flow = InstalledAppFlow.from_client_secrets_file(str(client_file), SCOPES)
    credentials = flow.run_local_server(port=0)
    Path(token_file).write_text(credentials.to_json(), encoding='utf-8')
    return credentials


def load_credentials(token_file):
    token_file = Path(token_file)
    if not token_file.exists():
        raise GmailAuthRequired('Gmail has not been authorised on this machine yet.')
    credentials = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not credentials.valid:
        try:
            credentials.refresh(Request())
        except RefreshError as error:
            raise GmailAuthRequired(f'The Gmail authorisation expired or was revoked ({error}).')
        token_file.write_text(credentials.to_json(), encoding='utf-8')
    return credentials


class GmailApiBackend(BaseEmailBackend):
    def __init__(self, token_file=None, fail_silently=False, **kwargs):
        super().__init__(**kwargs)
        self.token_file = token_file
        self.fail_silently = fail_silently

    def send_messages(self, email_messages):
        session = AuthorizedSession(load_credentials(self.token_file))
        sent = 0
        for message in email_messages:
            raw = base64.urlsafe_b64encode(message.message().as_bytes()).decode()
            response = session.post(SEND_URL, json={'raw': raw}, timeout=TIMEOUT)
            response.raise_for_status()
            sent += 1
        return sent

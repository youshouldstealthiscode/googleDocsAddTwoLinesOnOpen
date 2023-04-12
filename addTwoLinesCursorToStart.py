import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import uuid

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

def main():
    creds = None
    if 'token.json' in os.listdir():
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

    service = build('docs', 'v1', credentials=creds)

    # Replace the DOCUMENT_ID variable with the ID of your Google Doc
    DOCUMENT_ID = 'YOUR_DOCUMENT_ID'

    # Add two empty lines to the beginning of the document
    requests = [{
        'insertText': {
            'location': {
                'index': 1
            },
            'text': '\n\n'
        }
    }]

    # Set the cursor position at the beginning of the document for input
    cursor_position_request = {
        'updateCursorPosition': {
            'cursorPosition': {
                'index': 0,
                'segmentId': ''
            },
            'suggestionMode': 'ALWAYS',
            'collaboratorId': uuid.uuid4().hex
        }
    }
    requests.append(cursor_position_request)

    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
    print(f'Updated document with ID "{DOCUMENT_ID}".')

if __name__ == '__main__':
    main()

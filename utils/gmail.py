import time
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.send']


class Gmail():
    def __init__(self, user_id='me', alerts_label=['Academia'], data_path='./',digest_address=''):
        # set user_id
        self.user_id = user_id
        # set label
        self.alerts_label = alerts_label
        # set data path
        self.data_path = data_path
        self.token_path = os.path.join(self.data_path, 'token.json')
        self.credentials_path = os.path.join(self.data_path, 'credentials.json')
        # set digest address
        self.digest_address = digest_address
        # set credentials
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_label_ids(self, label_names):
        # find corresponding label ids
        results = self.service.users().labels().list(userId=self.user_id).execute()
        labels = results.get('labels', [])
        
        label_ids = []
        for name in label_names:
            for label in labels:
                if label['name']==name:
                    label_ids.append(label['id'])
        return label_ids

    def fetch_labeled_msg_ids(self):
        # get label ids
        label_ids = self.get_label_ids(self.alerts_label)
        # fetch the corresponding messages with label ids
        try:
            response = self.service.users().messages().list(userId=self.user_id, labelIds=label_ids).execute()
            message_ids = []
            if 'messages' in response:
                message_ids.extend(response['messages'])
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId=self.user_id, labelIds=label_ids, pageToken=page_token).execute()
                message_ids.extend(response['messages'])
            return message_ids
        except Exception as e:
            print(f'An error has occurred: {e}')
            return []

    def fetch_msg_by_ids(self, msg_ids):
        msgs = []
        for msg_id in msg_ids:
            try:
                message = self.service.users().messages().get(userId=self.user_id, id=msg_id['id']).execute()
                msgs.append(message)
            except Exception as e:
                print(f'An error has occurred: {e}')
        return msgs

    def mark_msg_read(self, msg_ids):
        # set messages with the label as read
        body = {"addLabelIds": [], "removeLabelIds": ["UNREAD"]}
        for msg in msg_ids:
            self.service.users().messages().modify(userId=self.user_id, id=msg['id'], body=body).execute()

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text, 'html')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_digest(self, formatted_message):
        if self.digest_address == '':
            print('No digest email address provided!')
            return ''
        try:
            message = self.create_message('me', self.digest_address, f"Scholar Alerts Digest {time.strftime('%Y-%m-%d')}", formatted_message)
            send_resp = (self.service.users().messages().send(userId=self.digest_address, body=message)
               .execute())
            return send_resp['id']
        except Exception as e:
            print(f'An error has occurred: {e}')
            return ''


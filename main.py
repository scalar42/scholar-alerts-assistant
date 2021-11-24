import os
from utils.gmail import Gmail
from utils.assistant import Assistant
from utils.formatter import Formatter


USER_ID = "me"

SCHOLAR_LABEL = ["UNREAD", "Your-alert-label"] # Note: Remember to change the "Your-alert-label"
DIGEST_ADDRESS = "your-gmail-address@gmail.com" # Note: Remember to change the "your-gmail-address@gmail.com"

DATA_PATH = "./data/"

if __name__ == '__main__':
    # check the path
    os.makedirs(name=DATA_PATH, exist_ok=True)

    # create the utils
    gmail = Gmail(USER_ID, SCHOLAR_LABEL, DATA_PATH, DIGEST_ADDRESS)
    assistant = Assistant(DATA_PATH)
    formatter = Formatter()

    # get the latest email
    msg_ids = gmail.fetch_labeled_msg_ids()
    msgs = gmail.fetch_msg_by_ids(msg_ids)

    # parse the messages and remove duplicated entries
    entries = assistant.parse_msgs(msgs)
    unique_entries = assistant.remove_duplicate_entries(use_db=True)

    if len(unique_entries) != 0:
        # format the messages
        formatted_message = formatter.convert_to_html(unique_entries)

        # send the email
        gmail.send_digest(formatted_message)

        # mark the alert messages as read
        gmail.mark_msg_read(msg_ids)

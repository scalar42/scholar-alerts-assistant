import os
from utils.gmail import Gmail
from utils.assistant import Assistant
from utils.formatter import Formatter

VERBOSE = 1
DELETE_MODE = False

USER_ID = "me"

SCHOLAR_LABEL = [
    "UNREAD",
    "Academia",
]  # Note: Remember to change the "Your-alert-label"
DIGEST_ADDRESS = "daoxusheng@gmail.com"  # Note: Remember to change the "your-gmail-address@gmail.com"

DATA_PATH = "./data/"

if __name__ == "__main__":
    # check the path
    os.makedirs(name=DATA_PATH, exist_ok=True)

    # create the utils
    gmail = Gmail(USER_ID, SCHOLAR_LABEL, DATA_PATH, DIGEST_ADDRESS)
    assistant = Assistant(DATA_PATH)
    formatter = Formatter()

    # get the latest email
    msg_ids = gmail.fetch_labeled_msg_ids()
    msgs = gmail.fetch_msg_by_ids(msg_ids)
    if VERBOSE > 0:
        print(f"[INFO] {len(msg_ids)} Emails with {{SCHOLAR_LABEL}} labels found.")

    # parse the messages and remove duplicated entries
    entries = assistant.parse_msgs(msgs)
    unique_entries = assistant.remove_duplicate_entries(use_db=True)
    if VERBOSE > 0:
        print(f"[INFO] {len(unique_entries)} in {len(entries)} unique entries found.")

    # filter the messages from blacklists
    filtered_entries = assistant.filter_unwanted_entries(use_bl=True)
    if VERBOSE > 0:
        print(
            f"[INFO] Removed {assistant.discarded_cnt} entries by blacklist: {assistant.bl}"
        )
    # filtered_entries = unique_entries

    # sort by keywords
    sorted_entries = assistant.update_prioritized_entries()
    if VERBOSE > 0:
        print(f"[INFO] {len(assistant.prioritized_entries)} entries prioritized.")

    if len(sorted_entries) != 0:
        # format the messages
        formatted_message = formatter.convert_to_html(sorted_entries)

        # send the email
        gmail.send_digest(formatted_message, len(sorted_entries))
        if VERBOSE > 0:
            print(f"[INFO] Digest Message sent.")

        # mark the alert messages as read or delete
        if DELETE_MODE:
            gmail.delete_msg(msg_ids)
            if VERBOSE > 0:
                print(f"[INFO] {len(msg_ids)} messages deleted.")
        else:
            gmail.mark_msg_read(msg_ids)
            if VERBOSE > 0:
                print(f"[INFO] {len(msg_ids)} messages marked as read.")

    print(f"[LOG] Updated {len(sorted_entries)} paper entries.")

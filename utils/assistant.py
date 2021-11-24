import json
import base64
import os.path
from html.parser import HTMLParser
from .parser import Paper, Parser

class Assistant:
    def __init__(self, db_path):
        self.db_path = os.path.join(db_path, "db.json")
        self.db = None
        self.entries = []
        self.parser = Parser()

    def parse_msgs(self, msgs):
        for msg in msgs:
            msg = msg['payload']['body']['data']
            msg = base64.urlsafe_b64decode(msg).decode('utf-8')
            self.parser.feed(msg)
            self.entries.extend(self.parser.get_papers())
        return self.entries

    def remove_duplicate_entries(self, use_db=False):
        self.entries = list(set(self.entries))
        if use_db:
            if self.db is None:
                self.load_db()
            self.entries = [ entry for entry in self.entries if entry.title not in self.db ]
            self.update_db(self.entries)
            self.save_db()

        return self.entries

    def load_db(self):
        try:
            with open(self.db_path) as f:
                self.db = set(json.load(f))
        except Exception as e:
            self.db = set()

    def update_db(self, entries):
        for entry in entries:
            self.db.add(entry.title)

    def save_db(self):
        os.makedirs(name=os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w') as f:
            json.dump(list(self.db), f)

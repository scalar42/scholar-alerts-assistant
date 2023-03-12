import json
import base64
import os.path
from html.parser import HTMLParser
from .parser import Paper, Parser


class Assistant:
    def __init__(self, db_path):
        self.db_path = os.path.join(db_path, "db.json")
        self.db = None
        self.bl_path = os.path.join(db_path, "blacklist.json")
        self.bl = None
        self.kw_path = os.path.join(db_path, "keywords.json")
        self.kw = None
        self.prioritized_entries = []
        self.entries = []
        self.discarded_cnt = 0
        self.parser = Parser()

    def parse_msgs(self, msgs):
        '''
        Parse messages'''
        for msg in msgs:
            msg = msg["payload"]["body"]["data"]
            msg = base64.urlsafe_b64decode(msg).decode("utf-8")
            self.parser.feed(msg)
            self.entries.extend(self.parser.get_papers())
        return self.entries

    def remove_duplicate_entries(self, use_db=False):
        '''
        Remove duplicate entries'''
        self.entries = list(set(self.entries))
        if use_db:
            if self.db is None:
                self.load_db()
            self.entries = [
                entry for entry in self.entries if entry.title not in self.db
            ]
            self.update_db(self.entries)
            self.save_db()

        return self.entries

    def filter_unwanted_entries(self, use_bl=False):
        '''
        Filter unwanted entries'''
        if use_bl:
            if self.bl is None:
                self.load_bl()

            for bl_word in self.bl:
                for e in self.entries:
                    if bl_word.lower() in str(e).lower():
                        self.entries.remove(e)
                        self.discarded_cnt += 1
            # self.save_db()
        return self.entries

    def update_prioritized_entries(self):
        '''
        Update prioritized entries'''
        def match_keyword(string, keywords):
            '''
            Check if string contains any of the keywords'''
            for kw in keywords:
                if kw.lower() in string.lower():
                    return True
            return False
        if self.kw is None:
            self.load_kw()
        self.prioritized_entries = [e for e in self.entries if match_keyword(e.title, self.kw)]
        self.entries = self.prioritized_entries + [e for e in self.entries if not match_keyword(e.title, self.kw)]
        return self.entries

    def load_kw(self):
        '''
        Load keywords from file'''
        try:
            with open(self.kw_path) as f:
                self.kw = set(json.load(f))
        except Exception as e:
            self.kw = set()

    def load_bl(self):
        '''
        Load blacklist from file'''
        try:
            with open(self.bl_path) as f:
                self.bl = set(json.load(f))
        except Exception as e:
            self.bl = set()

    def load_db(self):
        '''
        Load database from file'''
        try:
            with open(self.db_path) as f:
                self.db = set(json.load(f))
        except Exception as e:
            self.db = set()

    def update_db(self, entries):
        '''
        Update database with new entries'''
        for entry in entries:
            self.db.add(entry.title)

    def save_db(self):
        '''
        Save database to file'''
        os.makedirs(name=os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w+") as f:
            json.dump(list(self.db), f)

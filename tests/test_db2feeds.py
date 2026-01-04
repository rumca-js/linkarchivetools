from datetime import datetime
from pathlib import Path
import shutil
import unittest
from sqlalchemy import create_engine

from linkarchivetools import (
   Db2Feeds,
)
from linkarchivetools.utils.reflected import ReflectedTable


class Db2FeedsTest(unittest.TestCase):
    def copy_input(self):
        path = Path("input.db")
        if path.exists():
            path.unlink()

        shutil.copy("example/db.db", "input.db")

    def add_entry_with_tags(self):
        engine = create_engine(f"sqlite:///input.db")
        with engine.connect() as connection:
            table = ReflectedTable(engine=engine, connection=connection)

            data = {}
            data["link"] = "https://youtube.com/channel/12345678"
            data["title"] = "Test title"
            data["manual_status_code"] = 0
            data["source_url"] = ""
            data["permanent"] = False
            data["bookmarked"] = False
            data["status_code"] = 200
            data["contents_type"] = 0
            data["page_rating_contents"] = 0
            data["page_rating_visits"] = 0
            data["page_rating_votes"] = 80
            data["page_rating"] = 0

            entry_id = table.insert_json_data("linkdatamodel", data)

            data = {}
            data["entry_id"] = entry_id
            data["tag"] = "test tag"

            table.insert_json_data("entrycompactedtags", data)

            data = {}
            data["entry_id"] = entry_id
            data["stars"] = 123
            data["followers_count"] = 123
            data["date_updated"] = datetime.now()

            table.insert_json_data("socialdata", data)

    def test_init(self):
        self.copy_input()

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")

    def test_convert__standard(self):
        self.copy_input()

        self.add_entry_with_tags()

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")
        feeds.convert()

    def test_convert__with_read_internet(self):
        self.copy_input()

        self.add_entry_with_tags()

        feeds = Db2Feeds(input_db="input.db", output_db="output.db", remote_server="https://127.0.0.1:3000", read_internet_links=True)
        feeds.convert()

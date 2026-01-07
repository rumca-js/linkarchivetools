from datetime import datetime
from pathlib import Path
import shutil
import unittest
from sqlalchemy import create_engine

from linkarchivetools import (
   Db2Feeds,
)
from linkarchivetools.utils.reflected import (
   ReflectedTable,
   ReflectedEntryTable,
   ReflectedEntryCompactedTags,
   ReflectedSocialData,
)


class Db2FeedsTest(unittest.TestCase):
    def copy_input(self):
        path = Path("input.db")
        if path.exists():
            path.unlink()

        shutil.copy("example/db.db", "input.db")

        path = Path("output.db")
        if path.exists():
            path.unlink()

    def get_default_entry_data(self, url):
        data = {}
        data["link"] = url
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
        return data

    def add_entry_with_tags(self, file_name):
        engine = create_engine(f"sqlite:///{file_name}")
        with engine.connect() as connection:
            data = self.get_default_entry_data(url="https://youtube.com/channel/12345678")
            table = ReflectedEntryTable(engine=engine, connection=connection)
            table.truncate()
            entry_id = table.insert_entry_json(data)

            data = {}
            data["entry_id"] = entry_id
            data["tag"] = "test tag"

            table = ReflectedEntryCompactedTags(engine=engine, connection=connection)
            table.insert_json_data(data)

            data = {}
            data["entry_id"] = entry_id
            data["stars"] = 123
            data["followers_count"] = 123
            data["date_updated"] = datetime.now()

            table = ReflectedSocialData(engine=engine, connection=connection)
            table.insert_json_data(data)

            data = self.get_default_entry_data(url="https://google.com")
            table = ReflectedEntryTable(engine=engine, connection=connection)
            entry_id = table.insert_entry_json(data)

    def add_entry_with_tags2(self, file_name):
        engine = create_engine(f"sqlite:///{file_name}")
        with engine.connect() as connection:
            data = self.get_default_entry_data(url="https://youtube.com/channel/123456789")
            table = ReflectedEntryTable(engine=engine, connection=connection)
            table.truncate()
            entry_id = table.insert_entry_json(data)

            data = {}
            data["entry_id"] = entry_id
            data["tag"] = "test tag"

            table = ReflectedEntryCompactedTags(engine=engine, connection=connection)
            table.insert_json_data(data)

            data = {}
            data["entry_id"] = entry_id
            data["stars"] = 123
            data["followers_count"] = 123
            data["date_updated"] = datetime.now()

            table = ReflectedSocialData(engine=engine, connection=connection)
            table.insert_json_data(data)

            data = self.get_default_entry_data(url="https://linkedin.com")
            table = ReflectedEntryTable(engine=engine, connection=connection)
            entry_id = table.insert_entry_json(data)

    def test_constructor(self):
        self.copy_input()

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")

        path = Path("output.db")
        self.assertTrue(path.is_file())

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 0)

    def test_convert__standard(self):
        self.copy_input()
        self.add_entry_with_tags("input.db")

        engine = create_engine(f"sqlite:///input.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 2)

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")
        # call tested function
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=12345678"))
            self.assertEqual(table.count(), 1)

        # check that if we add new things into input output is not cleared

        self.add_entry_with_tags2("input.db")

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")
        # call tested function
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=12345678"))
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=123456789"))
            self.assertEqual(table.count(), 2)

    def test_convert__clean(self):
        self.copy_input()
        self.add_entry_with_tags("input.db")

        engine = create_engine(f"sqlite:///input.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 2)

        feeds = Db2Feeds(input_db="input.db", output_db="output.db", clean=True)
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=12345678"))
            self.assertEqual(table.count(), 1)

        # check that if we add new things into input output is cleared

        self.add_entry_with_tags2("input.db")

        feeds = Db2Feeds(input_db="input.db", output_db="output.db", clean=True)
        # call tested function
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=123456789"))
            self.assertEqual(table.count(), 1)

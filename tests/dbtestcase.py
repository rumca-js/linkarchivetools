import unittest
from datetime import datetime
from pathlib import Path
import shutil
from sqlalchemy import create_engine

from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
   ReflectedEntryCompactedTags,
   ReflectedSocialData,
)


class DbTestCase(unittest.TestCase):
    def create_db(self, file_name):
        path = Path(file_name)
        if path.exists():
            path.unlink()

        shutil.copy("example/db.db", file_name)

        engine = create_engine(f"sqlite:///{file_name}")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            table.truncate()

    def clean_out(self):
        path = Path("output.db")
        if path.exists():
            path.unlink()

    def add_entry_with_tags(self, file_name):
        engine = create_engine(f"sqlite:///{file_name}")
        with engine.connect() as connection:
            data = self.get_default_entry_data(url="https://youtube.com/channel/12345678")
            table = ReflectedEntryTable(engine=engine, connection=connection)
            entry_id = table.insert_json(data)

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
            entry_id = table.insert_json(data)

    def add_entry_with_tags2(self, file_name):
        engine = create_engine(f"sqlite:///{file_name}")
        with engine.connect() as connection:
            data = self.get_default_entry_data(url="https://youtube.com/channel/123456789")
            table = ReflectedEntryTable(engine=engine, connection=connection)
            entry_id = table.insert_json(data)

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
            entry_id = table.insert_json(data)

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

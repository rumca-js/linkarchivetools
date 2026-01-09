from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine

from linkarchivetools import (
   Db2Feeds,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class Db2FeedsTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")

        path = Path("output.db")
        self.assertTrue(path.is_file())

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 0)

    def test_convert__standard(self):
        self.create_db("input1.db")
        self.create_db("input2.db")
        self.clean_out()
        self.add_entry_with_tags("input1.db")
        self.add_entry_with_tags2("input2.db")

        engine = create_engine(f"sqlite:///input1.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 2)

        feeds = Db2Feeds(input_db="input1.db", output_db="output.db")
        # call tested function
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=12345678"))
            self.assertEqual(table.count(), 1)

        # check that if we add new things into input output is not cleared

        feeds = Db2Feeds(input_db="input2.db", output_db="output.db")
        # call tested function
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=12345678"))
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=123456789"))
            self.assertEqual(table.count(), 2)

    def test_convert__clean(self):
        self.create_db("input1.db")
        self.create_db("input2.db")
        self.clean_out()
        self.add_entry_with_tags("input1.db")
        self.add_entry_with_tags2("input2.db")

        engine = create_engine(f"sqlite:///input1.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 2)

        feeds = Db2Feeds(input_db="input1.db", output_db="output.db", clean=True)
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=12345678"))
            self.assertEqual(table.count(), 1)

        # check that if we add new things into input output is cleared


        feeds = Db2Feeds(input_db="input2.db", output_db="output.db", clean=True)
        # call tested function
        feeds.convert()

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertTrue(table.is_entry_link("https://www.youtube.com/feeds/videos.xml?channel_id=123456789"))
            self.assertEqual(table.count(), 1)

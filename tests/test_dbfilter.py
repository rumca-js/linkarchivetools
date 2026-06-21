import unittest
from pathlib import Path
from sqlalchemy import create_engine

from linkarchivetools import DbFilter
from linkarchivetools.utils.reflected import ReflectedGenericTable, ReflectedEntryTable
from .dbtestcase import DbTestCase


class DbFilterTest(DbTestCase):
    def get_row_count(self, db_path, table_name):
        engine = create_engine(f"sqlite:///{db_path}")
        with engine.connect() as connection:
            table = ReflectedGenericTable(engine, connection, table_name)
            return table.count()

    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        filter = DbFilter(input_db="input.db", output_db="output.db")
        self.assertTrue(filter.is_valid())

        path = Path("output.db")
        self.assertTrue(path.is_file())
        filter.close()

    def test_filter_bookmarks(self):
        self.create_db("input.db")
        self.clean_out()

        # Add some entries into input.db
        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)

            # Entry 1: Bookmarked
            data1 = self.get_default_entry_data("https://google.com")
            data1["bookmarked"] = True
            entry_table.insert_json(data1)

            # Entry 2: Not bookmarked
            data2 = self.get_default_entry_data("https://yahoo.com")
            data2["bookmarked"] = False
            entry_table.insert_json(data2)

        # Run filter
        db_filter = DbFilter(input_db="input.db", output_db="output.db")
        db_filter.filter_bookmarks()
        db_filter.close()

        # Check output db
        engine = create_engine("sqlite:///output.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)
            self.assertEqual(entry_table.count(), 1)
            # The remaining entry should be the bookmarked one
            entries = list(entry_table.get_entries())
            self.assertEqual(entries[0].link, "https://google.com")

    def test_filter_votes(self):
        self.create_db("input.db")
        self.clean_out()

        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)

            # Entry 1: with votes
            data1 = self.get_default_entry_data("https://google.com")
            data1["page_rating_votes"] = 10
            entry_table.insert_json(data1)

            # Entry 2: without votes
            data2 = self.get_default_entry_data("https://yahoo.com")
            data2["page_rating_votes"] = 0
            entry_table.insert_json(data2)

        db_filter = DbFilter(input_db="input.db", output_db="output.db")
        db_filter.filter_votes()
        db_filter.close()

        engine = create_engine("sqlite:///output.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)
            self.assertEqual(entry_table.count(), 1)
            entries = list(entry_table.get_entries())
            self.assertEqual(entries[0].link, "https://google.com")

    def test_filter_redundant(self):
        self.create_db("input.db")
        self.clean_out()

        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)

            # Entry 1: Bookmarked=True, page_rating_votes=0 (not redundant)
            data1 = self.get_default_entry_data("https://google.com")
            data1["bookmarked"] = True
            data1["page_rating_votes"] = 0
            entry_table.insert_json(data1)

            # Entry 2: Bookmarked=False, page_rating_votes=5 (not redundant)
            data2 = self.get_default_entry_data("https://yahoo.com")
            data2["bookmarked"] = False
            data2["page_rating_votes"] = 5
            entry_table.insert_json(data2)

            # Entry 3: Bookmarked=False, page_rating_votes=0 (redundant - will be deleted)
            data3 = self.get_default_entry_data("https://bing.com")
            data3["bookmarked"] = False
            data3["page_rating_votes"] = 0
            entry_table.insert_json(data3)

        db_filter = DbFilter(input_db="input.db", output_db="output.db")
        db_filter.filter_redundant()
        db_filter.close()

        engine = create_engine("sqlite:///output.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)
            self.assertEqual(entry_table.count(), 2)
            links = {entry.link for entry in entry_table.get_entries()}
            self.assertIn("https://google.com", links)
            self.assertIn("https://yahoo.com", links)
            self.assertNotIn("https://bing.com", links)

    def test_truncate(self):
        self.create_db("input.db")
        self.clean_out()

        # Let's verify that some of the tables that should be truncated have rows in the input db.
        # e.g., 'browser' and 'userconfig' should have > 0 rows in the example db.
        input_browser_count = self.get_row_count("input.db", "browser")
        input_userconfig_count = self.get_row_count("input.db", "userconfig")

        self.assertGreater(input_browser_count, 0)
        self.assertGreater(input_userconfig_count, 0)

        # Let's verify that some of the tables that should NOT be truncated have rows in the input db.
        # e.g., 'compactedtags' and 'searchview' should have > 0 rows.
        input_compactedtags_count = self.get_row_count("input.db", "compactedtags")
        input_searchview_count = self.get_row_count("input.db", "searchview")

        self.assertGreater(input_compactedtags_count, 0)
        self.assertGreater(input_searchview_count, 0)

        # Let's instantiate DbFilter and run truncate()
        db_filter = DbFilter(input_db="input.db", output_db="output.db")
        db_filter.truncate()
        db_filter.close()

        # Check output db
        # 1. Truncated tables should now have 0 rows
        self.assertEqual(self.get_row_count("output.db", "browser"), 0)
        self.assertEqual(self.get_row_count("output.db", "userconfig"), 0)

        # 2. Non-truncated tables should still have the same number of rows
        self.assertEqual(
            self.get_row_count("output.db", "compactedtags"),
            input_compactedtags_count,
        )
        self.assertEqual(
            self.get_row_count("output.db", "searchview"),
            input_searchview_count,
        )


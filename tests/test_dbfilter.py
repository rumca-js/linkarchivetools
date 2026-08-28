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

        db_filter = DbFilter(db="input.db")
        self.assertTrue(db_filter.is_valid())

        path = Path("input.db")
        self.assertTrue(path.is_file())
        db_filter.close()

    def test_delete_entries_non_bookmarked(self):
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
        db_filter = DbFilter(db="input.db")
        # call tested function
        db_filter.delete_entries_non_bookmarked()
        db_filter.close()

        # Check input db
        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)
            self.assertEqual(entry_table.count(), 1)
            # The remaining entry should be the bookmarked one
            entries = list(entry_table.get_entries())
            self.assertEqual(entries[0].link, "https://google.com")

    def test_delete_entries_no_votes(self):
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

        db_filter = DbFilter(db="input.db")
        # call tested function
        db_filter.delete_entries_no_votes()
        db_filter.close()

        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)
            self.assertEqual(entry_table.count(), 1)
            entries = list(entry_table.get_entries())
            self.assertEqual(entries[0].link, "https://google.com")

    def test_delete_entries_redundant(self):
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

        db_filter = DbFilter(db="input.db")
        # call tested function
        db_filter.delete_entries_redundant()
        db_filter.close()

        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            entry_table = ReflectedEntryTable(engine, connection)
            self.assertEqual(entry_table.count(), 2)
            links = {entry.link for entry in entry_table.get_entries()}
            self.assertIn("https://google.com", links)
            self.assertIn("https://yahoo.com", links)
            self.assertNotIn("https://bing.com", links)

    def test_truncate_user_tables(self):
        self.create_db("input.db")
        self.clean_out()

        #input_browser_count = self.get_row_count("input.db", "browser")
        input_userconfig_count = self.get_row_count("input.db", "userconfig")

        #self.assertGreater(input_browser_count, 0)
        self.assertGreater(input_userconfig_count, 0)

        input_compactedtags_count = self.get_row_count("input.db", "compactedtags")
        input_searchview_count = self.get_row_count("input.db", "searchview")

        self.assertGreater(input_compactedtags_count, 0)
        self.assertGreater(input_searchview_count, 0)

        db_filter = DbFilter(db="input.db")
        db_filter.truncate_user_tables()
        db_filter.close()

        #self.assertEqual(self.get_row_count("input.db", "browser"), 0)
        self.assertEqual(self.get_row_count("input.db", "userconfig"), 0)

        self.assertEqual(
            self.get_row_count("input.db", "compactedtags"),
            input_compactedtags_count,
        )
        self.assertEqual(
            self.get_row_count("input.db", "searchview"),
            input_searchview_count,
        )

    def test_truncate_dynamic_data(self):
        self.create_db("input.db")
        self.clean_out()

        #input_browser_count = self.get_row_count("input.db", "browser")
        input_userconfig_count = self.get_row_count("input.db", "userconfig")

        #self.assertGreater(input_browser_count, 0)
        self.assertGreater(input_userconfig_count, 0)

        input_compactedtags_count = self.get_row_count("input.db", "compactedtags")
        input_searchview_count = self.get_row_count("input.db", "searchview")

        self.assertGreater(input_compactedtags_count, 0)
        self.assertGreater(input_searchview_count, 0)

        db_filter = DbFilter(db="input.db")
        db_filter.truncate_dynamic_data()
        db_filter.close()

        #self.assertEqual(self.get_row_count("input.db", "browser"), 0)
        self.assertTrue(self.get_row_count("input.db", "userconfig") > 0)

        self.assertEqual(
            self.get_row_count("input.db", "compactedtags"),
            input_compactedtags_count,
        )
        self.assertEqual(
            self.get_row_count("input.db", "searchview"),
            input_searchview_count,
        )

    def test_truncate_configuration_tables(self):
        self.create_db("input.db")
        self.clean_out()

        #input_browser_count = self.get_row_count("input.db", "browser")
        input_userconfig_count = self.get_row_count("input.db", "userconfig")

        #self.assertGreater(input_browser_count, 0)
        self.assertGreater(input_userconfig_count, 0)

        input_compactedtags_count = self.get_row_count("input.db", "compactedtags")
        input_searchview_count = self.get_row_count("input.db", "searchview")

        self.assertGreater(input_compactedtags_count, 0)
        self.assertGreater(input_searchview_count, 0)

        db_filter = DbFilter(db="input.db")
        db_filter.truncate_configuration_tables()
        db_filter.close()

        #self.assertEqual(self.get_row_count("input.db", "browser"), 0)
        self.assertTrue(self.get_row_count("input.db", "userconfig") > 0)

        self.assertEqual(
            self.get_row_count("input.db", "compactedtags"),
            input_compactedtags_count,
        )
        self.assertEqual(
            self.get_row_count("input.db", "searchview"),
            input_searchview_count,
        )

    def test_obfuscate(self):
        self.create_db("input.db")
        self.clean_out()

        db_filter = DbFilter(db="input.db")
        # Run filter
        db_filter.obfuscate()

        db_filter.close()

    def test_obfuscate__connection(self):
        self.create_db("input.db")
        self.clean_out()
        self.truncate_table("input.db", "user")

        users_count = self.get_row_count("input.db", "user")
        self.assertEqual(users_count, 0)

        user_id = self.add_user("input.db", "test")

        users_count = self.get_row_count("input.db", "user")
        self.assertEqual(users_count, 1)

        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            db_filter = DbFilter(engine=engine, connection=connection)
            # Run filter
            db_filter.obfuscate()

            db_filter.close()

        users_count = self.get_row_count("input.db", "user")
        self.assertEqual(users_count, 1)

        engine = create_engine("sqlite:///input.db")
        with engine.connect() as connection:
            users = ReflectedGenericTable(engine, connection, table_name="user")
            users = users.get_where({})
            for user in users:
                print(user)

from pathlib import Path
import shutil
import unittest
from sqlalchemy import create_engine

from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
   ReflectedSourceTable,
   ReflectedTable,
)
from .dbtestcase import DbTestCase


class UtilsReflectedEntryTableTest(DbTestCase):
    def test_insert_entry_json(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            entry_json = {
               "link" : "https://test.com"
            }
            table.truncate()
            
            self.assertEqual(table.count(), 0)
            # call tested function
            table.insert_entry_json(entry_json)
            self.assertEqual(table.count(), 1)


class UtilsReflectedSourceTableTest(DbTestCase):
    def test_insert_json(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        with engine.connect() as connection:
            table = ReflectedSourceTable(engine=engine, connection=connection)
            source_json = {
               "url" : "https://test.com",
               "enabled" : True,
               "source_type" : "",
               "title" : "",
               "category_name": "",
               "subcategory_name": "",
               "export_to_cms": False,
               "remove_after_days": 5,
               "language": "",
               "age": 0,
               "fetch_period": 3600,
               "auto_tag": "",
               "entries_backgroundcolor_alpha": 1.0,
               "entries_backgroundcolor": "",
               "entries_alpha": 1.0,
               "proxy_location": "",
               "auto_update_favicon":False,
            }
            table.truncate()
            
            self.assertEqual(table.count(), 0)
            # call tested function
            table.insert_json(source_json)
            self.assertEqual(table.count(), 1)

    def test_is_url(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        with engine.connect() as connection:
            table = ReflectedSourceTable(engine=engine, connection=connection)
            source_json = {
               "url" : "https://test.com",
               "enabled" : True,
               "source_type" : "",
               "title" : "",
               "category_name": "",
               "subcategory_name": "",
               "export_to_cms": False,
               "remove_after_days": 5,
               "language": "",
               "age": 0,
               "fetch_period": 3600,
               "auto_tag": "",
               "entries_backgroundcolor_alpha": 1.0,
               "entries_backgroundcolor": "",
               "entries_alpha": 1.0,
               "proxy_location": "",
               "auto_update_favicon":False,
            }
            table.truncate()

            # call tested function
            self.assertFalse(table.is_url("https://test.com"))
            table.insert_json(source_json)
            # call tested function
            self.assertTrue(table.is_url("https://test.com"))

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
    def test_insert_json(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()
        
        self.assertEqual(table.count(), 0)
        # call tested function
        entry_id = table.insert_json(entry_json)
        self.assertEqual(table.count(), 1)
        self.assertTrue(entry_id)

    def test_is__link(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()

        # call tested function
        self.assertFalse(table.exists(link="https://test.com"))
        table.insert_json(entry_json)
        # call tested function
        self.assertTrue(table.exists(link="https://test.com"))

    def test_update(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()

        entry_id = table.insert_json(entry_json)

        # call tested function
        table.update_json_data(entry_id, {"title" : "New title"})

        entry = table.get(entry_id)
        self.assertTrue(entry)
        self.assertEqual(entry.title, "New title")

    def test_get(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()
        
        self.assertEqual(table.count(), 0)
        # call tested function
        entry_id = table.insert_json(entry_json)

        self.assertTrue(entry_id)
        entry = table.get(entry_id)
        self.assertTrue(entry)

    def test_get_where__conditions_map(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()
        
        self.assertEqual(table.count(), 0)
        # call tested function
        entry_id = table.insert_json(entry_json)

        self.assertTrue(entry_id)
        entries = table.get_where(conditions_map={"title" : "Test"})
        self.assertTrue(entries)

    def test_get_where__conditions(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")

        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()
        
        self.assertEqual(table.count(), 0)
        # call tested function
        entry_id = table.insert_json(entry_json)

        self.assertTrue(entry_id)
        entries = table.get_where(conditions=[table.get_table().c.title == "Test"])
        self.assertTrue(entries)

    def test_get_where__order_by(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedEntryTable(engine=engine, connection=None)
        entry_json = {
           "link" : "https://test.com",
           "title" : "Test"
        }
        table.truncate()
        
        self.assertEqual(table.count(), 0)
        # call tested function
        entry_id = table.insert_json(entry_json)

        self.assertTrue(entry_id)
        entries = table.get_where(order_by=[table.get_table().c.title.desc()])
        self.assertTrue(entries)


class UtilsReflectedSourceTableTest(DbTestCase):
    def test_insert_json(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedSourceTable(engine=engine, connection=None)
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

    def test_is__url(self):
        self.create_db("input1.db")

        engine = create_engine(f"sqlite:///input1.db")
        table = ReflectedSourceTable(engine=engine, connection=None)
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
        self.assertFalse(table.exists(url="https://test.com"))
        table.insert_json(source_json)
        # call tested function
        self.assertTrue(table.exists(url="https://test.com"))

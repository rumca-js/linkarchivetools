from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine

from linkarchivetools import (
   DbMerge,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class DbMergeTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input1.db")
        self.create_db("input2.db")
        self.clean_out()

        self.add_entry_with_tags("input1.db")
        self.add_entry_with_tags2("input2.db")

        input_dbs = ["input1.db", "input2.db"]

        # call tested function
        merge = DbMerge(input_dbs=input_dbs, output_db="output.db")

        path = Path("output.db")
        self.assertFalse(path.is_file())

    def test_convert__different_entries(self):
        self.create_db("input1.db")
        self.create_db("input2.db")
        self.clean_out()

        self.add_entry_with_tags("input1.db")
        self.add_entry_with_tags2("input2.db")

        input_dbs = ["input1.db", "input2.db"]

        merge = DbMerge(input_dbs=input_dbs, output_db="output.db")
        # call tested function
        merge.convert()

        path = Path("output.db")
        self.assertTrue(path.is_file())

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 4)

    def test_convert__same_entries(self):
        self.create_db("input1.db")
        self.create_db("input2.db")
        self.clean_out()

        self.add_entry_with_tags("input1.db")
        self.add_entry_with_tags("input2.db")

        input_dbs = ["input1.db", "input2.db"]

        merge = DbMerge(input_dbs=input_dbs, output_db="output.db")
        # call tested function
        merge.convert()

        path = Path("output.db")
        self.assertTrue(path.is_file())

        engine = create_engine(f"sqlite:///output.db")
        with engine.connect() as connection:
            table = ReflectedEntryTable(engine=engine, connection=connection)
            self.assertEqual(table.count(), 2)

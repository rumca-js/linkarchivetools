import unittest
from types import SimpleNamespace

from linkarchivetools import (
   DbAnalyzer,
)
from .dbtestcase import DbTestCase


class Db2AnalyzerTest(DbTestCase):
    def test_init(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")

        analyzer = DbAnalyzer(input_db="input.db")
        self.assertTrue(True)

    def test_print_summary(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        args = SimpleNamespace(search=None, ignore_case=True, verbosity=0)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        analyzer.print_summary()
        self.assertTrue(True)

    def test_search__none(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        args = {}

        analyzer = DbAnalyzer(input_db="input.db")
        analyzer.search()
        self.assertTrue(True)

    def test_search__search(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "*youtube.com*"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=0, table=False, order_by=None, asc=True, desc=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        analyzer.search()
        self.assertTrue(True)

    def test_get_entries(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "*youtube.com*"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=0, table=False, order_by=None, asc=True, desc=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)

        entries = []
        for entry in analyzer.get_entries():
            entries.append(entry)

        self.assertTrue(len(entries) > 0)

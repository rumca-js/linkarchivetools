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

        # call tested function
        analyzer = DbAnalyzer(input_db="input.db")
        self.assertTrue(True)

    def test_print_tables(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        args = SimpleNamespace(search=None, ignore_case=True, verbosity=1)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        analyzer.print_tables()
        self.assertTrue(True)

    def test_print_tables__print_columns(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        args = SimpleNamespace(search=None, ignore_case=True, verbosity=1)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        analyzer.print_tables(print_columns=True)
        self.assertTrue(True)

    def test_search__none(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        args = {}

        analyzer = DbAnalyzer(input_db="input.db")
        # call tested function
        for item in analyzer.search():
            pass

        self.assertTrue(True)

    def test_search__generic(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "*youtube.com*"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=1, table=False, order_by=None, asc=True, desc=False, json=False, rss=False, channel=False, title=False, description=False, votes=False, social=False, tags=False, source=False, date_created=False, date_published=False, status=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        for item in analyzer.search():
            pass

        self.assertTrue(True)

    def test_search__link(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "link=*youtube.com*"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=1, table=False, order_by=None, asc=True, title=False, desc=False, json=False, rss=False, channel=False, description=False, social=False, votes=False, tags=False, source=False, date_created=False, date_published=False, status=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        for item in analyzer.search():
            pass

        self.assertTrue(True)

    def test_search__tags(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "tags__tag=video"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=1, table=False, order_by=None, asc=True, desc=False, json=False, rss=False, channel=False, description=False, social=False, votes=False, tags=False, source=False, date_created=False, date_published=False, status=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        for item in analyzer.search():
            pass

        self.assertTrue(True)

    def test_search__source(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "source__url=https://*"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=1, table=False, order_by=None, asc=True, desc=False, json=False, rss=False, channel=False, description=False, social=False, votes=False,tags=False, source=False, date_created=False, date_published=False, status=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        for item in analyzer.search():
            pass

        self.assertTrue(True)

    def test_search__json(self):
        self.create_db("input.db")
        self.add_entry_with_tags("input.db")
        search = "*youtube.com*"
        args = SimpleNamespace(search=search, ignore_case = True, verbosity=1, table=False, order_by=None, asc=True, desc=False, json=True, title=False, rss=False, channel=False, description=False, social=False, votes=False, tags=False, source=False, date_created=False, date_published=False, status=False)

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        # call tested function
        for item in analyzer.search():
            pass

        self.assertTrue(True)

import unittest
from types import SimpleNamespace

from linkarchivetools import (
   DbAnalyzer,
)


class Db2AnalyzerTest(unittest.TestCase):
    def test_init(self):
        analyzer = DbAnalyzer(input_db="input.db")

    def test_print_summary(self):
        analyzer = DbAnalyzer(input_db="input.db")
        analyzer.print_summary()

    def test_search__none(self):
        args = {}

        analyzer = DbAnalyzer(input_db="input.db")
        analyzer.search()

    def test_search__search(self):
        #search = "*youtube.com*"
        #args = SimpleNamespace(search=search, ignore_case = True)

        search = "*youtube.com*"
        args = {"search":search, "ignore_case" : True}

        analyzer = DbAnalyzer(input_db="input.db", args=args)
        analyzer.search()

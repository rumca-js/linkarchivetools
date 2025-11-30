import unittest
from linkarchivetools import (
   DbAnalyzer,
)


class Db2AnalyzerTest(unittest.TestCase):
    def test_init(self):
        analyzer = DbAnalyzer(input_db="input.db")

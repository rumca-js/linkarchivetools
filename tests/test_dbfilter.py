import unittest
from linkarchivetools import (
   DbFilter,
)


class Db2FeedsTest(unittest.TestCase):
    def test_constructor(self):
        filter = DbFilter(input_db="input.db", output_db="output.db")

    def test_filter_votes(self):
        filter = DbFilter(input_db="input.db", output_db="output.db")

        # call tested function
        filter.filter_votes()

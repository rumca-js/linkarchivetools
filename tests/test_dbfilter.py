import unittest
from linkarchivetools import (
   DbFilter,
)


class Db2FeedsTest(unittest.TestCase):
    def test_init(self):
        filter = DbFilter(input_db="input.db", output_db="output.db")

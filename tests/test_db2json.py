import unittest
from linkarchivetools import (
   Db2JSON,
)


class Db2JSONTest(unittest.TestCase):
    def test_constructor(self):
        converter = Db2JSON(input_db="input.db", output_dir=".")

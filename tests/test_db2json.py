from linkarchivetools import (
   Db2JSON,
)

from .dbtestcase import DbTestCase


class Db2JSONTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        converter = Db2JSON(input_db="input.db", output_dir=".")

    def test_convert(self):
        self.create_db("input.db")
        self.clean_out()

        converter = Db2JSON(input_db="input.db", output_dir=".")
        converter.convert()

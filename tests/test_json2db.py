from pathlib import Path
import shutil
import unittest

from linkarchivetools import (
   JSON2Db,
)
from linkarchivetools.utils.reflected import ReflectedTable


class JSON2DbTest(unittest.TestCase):
    def copy_input(self):
        path = Path("input.db")
        if path.exists():
            path.unlink()

        shutil.copy("example/bookmark_0.json", "input.json")
        shutil.copy("example/db.db", "db.db")

    def test_init(self):
        self.copy_input()

        handler = JSON2Db(input_file="input.json", output_db="output.db")
        handler.convert()

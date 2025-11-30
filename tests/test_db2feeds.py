from pathlib import Path
import shutil
import unittest

from linkarchivetools import (
   Db2Feeds,
)


class Db2FeedsTest(unittest.TestCase):
    def copy_input(self):
        path = Path("input.db")
        if path.exists():
            path.unlink()

        shutil.copy("example/db.db", "input.db")

    def test_init(self):
        self.copy_input()

        feeds = Db2Feeds(input_db="input.db", output_db="output.db")

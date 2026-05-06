from linkarchivetools.model import (
   DbConnection,
   BlockEntry,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class BlockEntryTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        block_list = BlockEntry(connection=connection)
        self.assertEqual(block_list.count(), 0)

    def test_add(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        block_list = BlockEntry(connection=connection)
        block_list.add("https://google.com")
        self.assertEqual(block_list.count(), 1)

    def test_is_blocked(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        block_list = BlockEntry(connection=connection)
        block_list.add("https://google.com")
        self.assertEqual(block_list.count(), 1)

        self.assertFalse(block_list.is_blocked("https://youtube.com"))
        self.assertTrue(block_list.is_blocked("https://google.com"))

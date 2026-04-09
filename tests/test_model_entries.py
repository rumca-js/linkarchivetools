from linkarchivetools.model import (
   DbConnection,
   Entries,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class EntriesTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        entries = Entries(connection=connection)
        self.assertEqual(entries.count(), 0)

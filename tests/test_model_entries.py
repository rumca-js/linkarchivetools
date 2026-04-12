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

    def test_add(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        entries = Entries(connection=connection)
        self.assertEqual(entries.count(), 0)

        entry_json = {}
        entry_json["link"] = "https://google.com"

        new_id = entries.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

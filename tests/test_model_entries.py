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

        # call tested function
        new_id = entries.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

        self.assertEqual(entries.count(), 1)

    def test_get(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        entries = Entries(connection=connection)
        self.assertEqual(entries.count(), 0)

        entry_json = {}
        entry_json["link"] = "https://google.com"

        new_id = entries.add(entry_json=entry_json)

        self.assertTrue(new_id is not None)
        self.assertEqual(entries.count(), 1)

        # call tested function
        self.assertTrue(entries.get(id=new_id))

    def test_delete(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        entries = Entries(connection=connection)
        self.assertEqual(entries.count(), 0)

        entry_json = {}
        entry_json["link"] = "https://google.com"

        new_id = entries.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

        self.assertEqual(entries.count(), 1)

        # call tested function
        entries.delete(id=int(new_id))

        self.assertEqual(entries.count(), 0)

    def test_delete__get_where(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        entries_controller = Entries(connection=connection)
        self.assertEqual(entries_controller.count(), 0)

        entry_json = {}
        entry_json["link"] = "https://google.com"

        new_id = entries_controller.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

        self.assertEqual(entries_controller.count(), 1)

        entries = entries_controller.get_where({})

        for entry in entries:
            # call tested function
            entries_controller.delete(id=int(entry.id))

        self.assertEqual(entries_controller.count(), 0)

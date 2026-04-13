from linkarchivetools.model import (
   DbConnection,
   EntryTags,
   Entries,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class EntryTagsTest(DbTestCase):
    def setUp(self):
        self.create_db("input.db")
        self.clean_out()

        self.connection = DbConnection("input.db")

    def add_entry(self):
        entries = Entries(connection=self.connection)
        entries.truncate()
        self.assertEqual(entries.count(), 0)

        entry_json = {}
        entry_json["link"] = "https://google.com"

        new_id = entries.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

        return entries.get(new_id)

    def test_constructor(self):
        # call tested function
        tags = EntryTags(connection=self.connection)
        tags.truncate()

        self.assertEqual(tags.count(), 0)

    def test_set(self):
        tags = EntryTags(connection=self.connection)
        tags.truncate()

        self.assertEqual(tags.count(), 0)

        entry = self.add_entry()

        # call tested function
        tags.set(entry_id=entry.id, tags="action, comedy")

        self.assertEqual(tags.count(), 1)

    def test_get(self):
        tags = EntryTags(connection=self.connection)
        tags.truncate()

        self.assertEqual(tags.count(), 0)

        entry = self.add_entry()
        tags.set(entry_id=entry.id, tags="action, comedy")
        self.assertEqual(tags.count(), 1)

        tags = tags.get(entry_id=entry.id)
        self.assertEqual(tags, "action, comedy")

    def test_get_map(self):
        tags = EntryTags(connection=self.connection)
        tags.truncate()

        self.assertEqual(tags.count(), 0)

        entry = self.add_entry()
        tags.set(entry_id=entry.id, tags="action, comedy")
        self.assertEqual(tags.count(), 1)

        tags_map = tags.get_map(entry_id=entry.id)
        self.assertEqual(len(tags_map), 2)
        self.assertEqual(tags_map[0], "action")
        self.assertEqual(tags_map[1], "comedy")

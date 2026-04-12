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
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        tags = EntryTags(connection=connection)
        tags.truncate()

        self.assertEqual(tags.count(), 0)

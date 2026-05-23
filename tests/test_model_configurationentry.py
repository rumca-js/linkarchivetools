from linkarchivetools.model import (
   DbConnection,
   CheckLater,
   Entries,
   ConfigurationEntry,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class ConfigurationEntryTest(DbTestCase):
    def setUp(self):
        self.create_db("input.db")
        self.clean_out()
        self.connection = DbConnection("input.db")

    def test_constructor(self):
        # call tested function
        controller = ConfigurationEntry(connection=self.connection)
        controller.truncate()

        self.assertEqual(controller.count(), 0)

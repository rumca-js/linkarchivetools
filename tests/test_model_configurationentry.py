from pathlib import Path

from linkarchivetools.model import (
   DbConnection,
   CheckLater,
   Entries,
   ConfigurationEntry,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)
from linkarchivetools.dbupdate import DbUpdate

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

    def test_constructor__new(self):
        path = Path("test.db")
        path.touch()

        db_update = DbUpdate(db="test.db")
        db_update.create_tables()

        self.connection = DbConnection("test.db")

        # call tested function
        controller = ConfigurationEntry(connection=self.connection)
        controller.truncate()

        self.assertEqual(controller.count(), 0)

        db_update.close()

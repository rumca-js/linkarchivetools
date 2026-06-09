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


class DbConnectionTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()
        self.connection = DbConnection("input.db")

        self.connection.truncate()
        self.connection.close()

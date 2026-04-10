from linkarchivetools.model import (
   DbConnection,
   Sources,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class SourcesTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        self.assertEqual(sources.count(), 0)

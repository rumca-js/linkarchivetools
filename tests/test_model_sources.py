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

    def test_set(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        source_url = "https://google.com"
        source_properties = {}

        source_id = sources.set(source_url=source_url, source_properties=source_properties)
        self.assertTrue(source_id is not None)

        source = sources.get(source_id)
        self.assertTrue(source is not None)
        self.assertEqual(sources.count(), 1)

    def test_delete(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        source_url = "https://google.com"
        source_properties = {}

        source_id = sources.set(source_url=source_url, source_properties=source_properties)
        self.assertTrue(source_id is not None)

        sources.delete(id = source_id)

from linkarchivetools.model import (
   DbConnection,
   Sources,
   SourceData,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class SourceDataTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        # call tested function
        sourcedata = SourceData(connection=connection)
        sourcedata.truncate()

        self.assertEqual(sources.count(), 0)
        self.assertEqual(sourcedata.count(), 0)

    def test_mark_read(self):
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

        sourcedata = SourceData(connection=connection)
        sourcedata.truncate()

        # call tested function
        sourcedata.mark_read(source)

        self.assertEqual(sourcedata.count(), 1)

        # call tested function
        sourcedata.mark_read(source)

        self.assertEqual(sourcedata.count(), 1)

    def test_is_update_needed_no_source_data(self):
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

        sourcedata = SourceData(connection=connection)
        sourcedata.truncate()

        # call tested function
        self.assertTrue(sourcedata.is_update_needed(source))

    def test_is_update_needed__false(self):
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

        sourcedata = SourceData(connection=connection)
        sourcedata.truncate()

        sourcedata.mark_read(source)

        self.assertEqual(sourcedata.count(), 1)

        # call tested function
        self.assertFalse(sourcedata.is_update_needed(source))

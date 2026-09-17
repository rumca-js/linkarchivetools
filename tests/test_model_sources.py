from pathlib import Path
from linkarchivetools.model import (
   DbConnection,
   Sources,
   SourceData,
)
from linkarchivetools.dbupdate import DbUpdate
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

        source_id = sources.set(source_url=source_url)
        self.assertTrue(source_id is not None)
        self.assertEqual(sources.count(), 1)

        source = sources.get(source_id)
        self.assertTrue(source is not None)

    def test_set__title(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        source_url = "https://google.com"
        source_properties = {"title" : "Googly Title"}

        source_id = sources.set(source_url=source_url, source_properties=source_properties)
        self.assertTrue(source_id is not None)
        self.assertEqual(sources.count(), 1)

        source = sources.get(source_id)
        self.assertTrue(source is not None)
        self.assertEqual(source.title, "Googly Title")

    def test_set__source_type(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        source_url = "https://google.com"

        source_id = sources.set(source_url=source_url, source_type="RSS")
        self.assertTrue(source_id is not None)
        self.assertEqual(sources.count(), 1)

        source = sources.get(source_id)
        self.assertTrue(source is not None)
        self.assertEqual(source.source_type, "RSS")

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

    def test_enable(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        source_url = "https://google.com"

        source_id = sources.set(source_url=source_url)

        self.assertTrue(source_id is not None)
        self.assertEqual(sources.count(), 1)

        source = sources.get(source_id)
        self.assertTrue(source is not None)

        sources.disable(source)

        # call function
        sources.enable(source)

        source = sources.get(source_id)
        self.assertTrue(source.enabled)

    def test_disable(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        source_url = "https://google.com"

        source_id = sources.set(source_url=source_url)

        self.assertTrue(source_id is not None)
        self.assertEqual(sources.count(), 1)

        source = sources.get(source_id)
        self.assertTrue(source is not None)

        # call function
        sources.disable(source)

        source = sources.get(source_id)
        self.assertFalse(source.enabled)

    def test_error(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        sources = Sources(connection=connection)
        sources.truncate()

        sd_controller = SourceData(connection=connection)

        source_url = "https://google.com"

        self.assertEqual(sd_controller.count(), 0)

        source_id = sources.set(source_url=source_url)

        self.assertTrue(source_id is not None)
        self.assertEqual(sources.count(), 1)

        source = sources.get(source_id)
        self.assertTrue(source is not None)

        # call function
        sources.error(source)

        self.assertEqual(sd_controller.count(), 1)

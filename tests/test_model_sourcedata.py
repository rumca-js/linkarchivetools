from datetime import datetime, timedelta

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
        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        self.assertEqual(sources.count(), 0)
        self.assertEqual(sc_controller.count(), 0)

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

        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        # call tested function
        sc_controller.mark_read(source)

        self.assertEqual(sc_controller.count(), 1)

        # call tested function
        sc_controller.mark_read(source)

        self.assertEqual(sc_controller.count(), 1)

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

        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        # call tested function
        self.assertTrue(sc_controller.is_update_needed(source))

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

        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        sc_controller.mark_read(source)

        self.assertEqual(sc_controller.count(), 1)

        # call tested function
        self.assertFalse(sc_controller.is_update_needed(source))

    def test_is_update_needed__true_data(self):
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

        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        data_id = sc_controller.mark_read(source)

        self.assertEqual(sc_controller.count(), 1)

        json_data = {}
        json_data["date_fetched"] = datetime.now() - timedelta(seconds=7200)
        sc_controller.get_table().update_json_data(id=data_id, json_data=json_data)

        # call tested function
        self.assertTrue(sc_controller.is_update_needed(source))

    def test_is_update_needed__false_data(self):
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

        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        data_id = sc_controller.mark_read(source)

        self.assertEqual(sc_controller.count(), 1)

        json_data = {}
        json_data["date_fetched"] = datetime.now() - timedelta(seconds=1800)
        sc_controller.get_table().update_json_data(id=data_id, json_data=json_data)

        # call tested function
        self.assertFalse(sc_controller.is_update_needed(source))

    def test_get_update_seconds(self):
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

        sc_controller = SourceData(connection=connection)
        sc_controller.truncate()

        sc_controller.mark_read(source)

        self.assertEqual(sc_controller.count(), 1)

        seconds = sc_controller.get_update_seconds(source=source)
        self.assertTrue(seconds >= 0)

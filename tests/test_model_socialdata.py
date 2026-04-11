from linkarchivetools.model import (
   DbConnection,
   SocialData,
   Entries,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class SocialDataTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        socialdata = SocialData(connection=connection)
        socialdata.truncate()

        self.assertEqual(socialdata.count(), 0)

    def test_add(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        entries = Entries(connection=connection)
        entries.truncate()

        entry_json_data = {}
        entry_json_data["link"] = "https://google.com"
        entry_id = entries.add(entry_json_data)

        self.assertEqual(entries.count(), 1)
        self.assertTrue(entry_id is not None)

        socialdata = SocialData(connection=connection)
        socialdata.truncate()

        social_data_json = {}

        socialdata.add(entry_id, social_data_json)

        self.assertEqual(socialdata.count(), 1)

from linkarchivetools.model import (
   DbConnection,
   CheckLater,
   Entries,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class CheckLaterTest(DbTestCase):
    def setUp(self):
        self.create_db("input.db")
        self.clean_out()
        self.connection = DbConnection("input.db")

    def test_constructor(self):
        # call tested function
        laters = CheckLater(connection=self.connection)
        laters.truncate()

        self.assertEqual(laters.count(), 0)

    def add_entry(self):
        entries = Entries(connection=self.connection)
        self.assertEqual(entries.count(), 0)

        entry_json = {}
        entry_json["link"] = "https://google.com"

        new_id = entries.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

        entry = entries.get(id=new_id)
        return entry

    def test_check_later(self):
        connection = DbConnection("input.db")

        laters = CheckLater(connection=self.connection)
        laters.truncate()

        self.assertEqual(laters.count(), 0)

        entry = self.add_entry()

        # call tested function
        laters.check_later(entry)

    def test_not_check_later(self):
        connection = DbConnection("input.db")

        laters = CheckLater(connection=self.connection)
        laters.truncate()

        self.assertEqual(laters.count(), 0)

        entry = self.add_entry()

        laters.check_later(entry)
        laters.not_check_later(entry)

        self.assertEqual(laters.count(), 0)

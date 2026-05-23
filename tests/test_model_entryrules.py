from linkarchivetools.model import (
   DbConnection,
   EntryRules,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class EntryRulesTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        rules = EntryRules(connection=connection)
        rules.truncate()

        # call tested function
        self.assertEqual(rules.count(), 0)

    def test_add(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        rules = EntryRules(connection=connection)
        rules.truncate()

        # call tested function
        rules.add_entry_rule("https://google.com")
        self.assertEqual(rules.count(), 1)

    def test_is_blocked(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        rules = EntryRules(connection=connection)
        rules.truncate()
        rules.add_entry_rule("https://google.com")
        self.assertEqual(rules.count(), 1)

        # call tested function
        self.assertFalse(rules.is_url_blocked("https://youtube.com"))
        self.assertTrue(rules.is_url_blocked("https://google.com"))

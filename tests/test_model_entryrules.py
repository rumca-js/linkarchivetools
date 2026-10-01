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

        connection = DbConnection("input.db")

        rules = EntryRules(connection=connection)

        # call tested function
        self.assertEqual(rules.count(), 0)

    def test_add(self):
        self.create_db("input.db")

        connection = DbConnection("input.db")

        rules = EntryRules(connection=connection)

        # call tested function
        rules.add_entry_rule("https://google.com")
        self.assertEqual(rules.count(), 1)

    def test_is_blocked(self):
        self.create_db("input.db")

        connection = DbConnection("input.db")

        rules = EntryRules(connection=connection)

        rules.add_entry_rule("https://google.com", block=True)
        self.assertEqual(rules.count(), 1)

        # call tested function
        self.assertFalse(rules.is_url_blocked("https://youtube.com"))
        self.assertTrue(rules.is_url_blocked("https://google.com"))

    def test_get_rules_for(self):
        self.create_db("input.db")

        connection = DbConnection("input.db")

        rules_controller = EntryRules(connection=connection)

        rules_controller.add_entry_rule("https://google.com", block=True)
        self.assertEqual(rules_controller.count(), 1)

        # call tested function
        rules = rules_controller.get_rules_for(url = "https://youtube.com")

        self.assertEqual(len(rules), 0)

        # call tested function
        rules = rules_controller.get_rules_for(url = "https://google.com")

        self.assertEqual(len(rules), 1)

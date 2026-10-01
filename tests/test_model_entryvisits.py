from linkarchivetools.model import (
   DbConnection,
   EntryVisitHistoryTable,
   EntryTransitionHistoryTable,
   Entries,
)

from .dbtestcase import DbTestCase


class CheckLaterTest(DbTestCase):
    def setUp(self):
        self.create_db("input.db")
        self.clean_out()
        self.connection = DbConnection("input.db")

    def add_entry(self, link=None):
        entries = Entries(connection=self.connection)

        entry_json = {}
        if link is None:
            entry_json["link"] = "https://google.com"
        else:
            entry_json["link"] = link

        new_id = entries.add(entry_json=entry_json)
        self.assertTrue(new_id is not None)

        entry = entries.get(id=new_id)
        return entry

    def test_constructor(self):
        # call tested function
        visits = EntryVisitHistoryTable(connection=self.connection)
        visits.truncate()

        self.assertEqual(visits.count(), 0)

        transitions = EntryTransitionHistoryTable(connection=self.connection)
        self.assertEqual(transitions.count(), 0)

    def test_visited(self):
        visits = EntryVisitHistoryTable(connection=self.connection)
        visits.truncate()

        self.assertEqual(visits.count(), 0)
        transitions = EntryTransitionHistoryTable(connection=self.connection)
        self.assertEqual(transitions.count(), 0)

        entry = self.add_entry()

        # call tested function
        visits.visited(entry)

        self.assertEqual(visits.count(), 1)
        self.assertEqual(transitions.count(), 0)

    def test_visited_two(self):
        visits = EntryVisitHistoryTable(connection=self.connection)
        visits.truncate()

        self.assertEqual(visits.count(), 0)
        transitions = EntryTransitionHistoryTable(connection=self.connection)
        self.assertEqual(transitions.count(), 0)

        entry_google = self.add_entry("https://google.com")
        entry_youtube = self.add_entry("https://youtube.com")

        # call tested function
        visits.visited(entry_google)
        visits.visited(entry_youtube)

        self.assertEqual(visits.count(), 2)
        self.assertEqual(transitions.count(), 1)

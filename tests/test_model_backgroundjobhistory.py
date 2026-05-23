from linkarchivetools.model import (
   DbConnection,
)

from .dbtestcase import DbTestCase


class BackgroundJobHistoryTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        self.assertEqual(connection.backgroundjobhistory.count(), 0)

from linkarchivetools.model import (
   DbConnection,
   AppLoggingService,
)

from .dbtestcase import DbTestCase


class AppLoggingTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        logs = AppLoggingService(connection=connection)
        self.assertEqual(logs.count(), 0)

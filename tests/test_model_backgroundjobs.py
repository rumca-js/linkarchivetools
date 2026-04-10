from linkarchivetools.model import (
   DbConnection,
   BackgroundJob,
)

from .dbtestcase import DbTestCase


class BackgroundJobTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        jobs = BackgroundJob(connection=connection)
        self.assertEqual(jobs.count(), 0)

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

    def test_insert_json_data(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        jobs = BackgroundJob(connection=connection)

        json_data = {}
        json_data["enabled"] = True
        json_data["job_name"] = "Test name"
        json_data["subject"] = "Test subject"
        jobs.insert_json_data(json_data)

        self.assertEqual(jobs.count(), 1)

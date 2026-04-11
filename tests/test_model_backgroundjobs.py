from datetime import datetime

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
        jobs.truncate()

        self.assertEqual(jobs.count(), 0)

    def test_insert_json_data(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        jobs = BackgroundJob(connection=connection)
        jobs.truncate()

        json_data = {}
        json_data["enabled"] = True
        json_data["job"] = "Test name"
        json_data["subject"] = "Test subject"
        json_data["date_created"] = datetime.now()
        json_data["priority"] = 0
        json_data["errors"] = 0
        jobs.insert_json_data(json_data)

        self.assertEqual(jobs.count(), 1)

    def test_create_single_job(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        jobs = BackgroundJob(connection=connection)
        jobs.truncate()

        job_id = jobs.create_single_job(job_name="test-job", subject="test subject")

        self.assertEqual(jobs.count(), 1)
        self.assertTrue(job_id is not None)

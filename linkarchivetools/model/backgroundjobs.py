from datetime import datetime
from sqlalchemy import and_
import json
from .basetable import BaseTable


class BackgroundJob(BaseTable):
    JOB_PROCESS_SOURCE = "process-source"
    JOB_LINK_ADD = "link-add"
    JOB_LINK_SAVE = "link-save"
    JOB_LINK_UPDATE_DATA = "link-update-data"
    JOB_LINK_RESET_DATA = "link-reset-data"
    JOB_LINK_RESET_LOCAL_DATA = "link-reset-local-data"
    JOB_LINK_DOWNLOAD_SOCIAL = "link-social-data"
    JOB_LINK_DOWNLOAD = "link-download"
    JOB_LINK_DOWNLOAD_MUSIC = "download-music"
    JOB_LINK_DOWNLOAD_VIDEO = "download-video"
    JOB_DOWNLOAD_FILE = "download-file"  # TODO stor file, should mention DB
    JOB_LINK_SCAN = "link-scan"
    JOB_SOURCE_ADD = "source-add"
    JOB_MOVE_TO_ARCHIVE = "move-to-archive"
    JOB_WRITE_DAILY_DATA = "write-daily-data"
    JOB_WRITE_YEAR_DATA = "write-year-data"
    JOB_WRITE_NOTIME_DATA = "write-notime-data"
    JOB_WRITE_TOPIC_DATA = "write-topic-data"
    JOB_IMPORT_DAILY_DATA = "import-daily-data"
    JOB_IMPORT_BOOKMARKS = "import-bookmarks"
    JOB_IMPORT_SOURCES = "import-sources"
    JOB_IMPORT_INSTANCE = "import-instance"
    JOB_IMPORT_FROM_FILES = "import-from-files"
    JOB_EXPORT_DATA = "export-data"
    JOB_CLEANUP = "cleanup"
    JOB_TRUNCATE_TABLE = "truncate-table"
    JOB_REMOVE = "remove"
    JOB_CHECK_DOMAINS = "check-domains"
    JOB_RUN_RULE = "run-rule"
    JOB_INITIALIZE = "initialize"
    JOB_INITIALIZE_BLOCK_LIST = (
        "initialize-block-list"  # initializes one specific block list
    )
    JOB_REFRESH = "refresh"

    def __init__(self, connection):
        self.connection = connection
        self.set_table("backgroundjob")

    def create_single_job(self, job_name, subject="", args="", user=None, cfg=None):

        args_text = args
        if args_text == "" and cfg:
            args_text = json.dumps(cfg)

        is_job = self.is_job(job_name=job_name, subject=subject)
        if not is_job:
            json_data = {}
            json_data["job"] = job_name
            json_data["task"] = ""
            json_data["subject"] = subject
            json_data["args"] = args_text
            json_data["priority"] = 1
            json_data["errors"] = 0
            json_data["enabled"] = True
            json_data["date_created"] = datetime.now()
            json_data["user_id"] = 0

            return self.connection.backgroundjob.insert_json_data(json_data)

    def is_job(self, job_name, subject=None):
        table = self.connection.backgroundjob.get_table()

        if subject:
            conditions = and_(table.c.job==job_name, table.c.subject==subject)
        else:
            conditions = and_(table.c.job==job_name)

        jobs = self.connection.backgroundjob.get_where_ex(conditions=conditions)
        for job in jobs:
            return True

        return False

    def get(self, id):
        return self.connection.backgroundjob.get(id=id)

    def get_cfg(id, self):
        job = self.get(id)
        if job:
            cfg = {}
            if job.args != "":
                try:
                    cfg = json.loads(job.args)
                except ValueError as E:
                    pass
                except TypeError as E:
                    pass
            return cfg

from sqlalchemy import create_engine
from sqlalchemy import (
    text,
)

from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
   ReflectedSourceTable,
   ReflectedTable,
   ReflectedEntryRules,
   ReflectedConfigurationEntry,
   ReflectedSourceOperationalData,
   ReflectedGenericTable,
   ReflectedSocialData,
)


class DbConnection(object):
    def __init__(self, db_file=None, engine=None, connection=None):
        self.db_file = db_file

        if not engine:
            self.engine = DbConnection.create_engine(self.db_file)
        else:
            self.engine = engine

        if not connection:
            self.connection = self.engine.connect()
        else:
            self.connection = connection

        sql_text = f"PRAGMA journal_mode=WAL;"
        self.connection.execute(text(sql_text))
        self.connection.commit()

        self.entries_table = ReflectedEntryTable(engine=self.engine, connection=self.connection)
        self.sources_table = ReflectedSourceTable(engine=self.engine, connection=self.connection)

        self.configurationentry = ReflectedConfigurationEntry(engine=self.engine, connection=self.connection)
        self.socialdata = ReflectedSocialData(engine=self.engine, connection=self.connection)
        self.sourceoperationaldata = ReflectedSourceOperationalData(engine=self.engine, connection=self.connection)
        self.entry_rules = ReflectedEntryRules(engine=self.engine, connection=self.connection)

        # TODO these are obsolete know
        self.applogging = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="applogging")
        self.backgroundjob = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="backgroundjob")
        self.backgroundjobhistory = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="backgroundjobhistory")
        self.blockentry = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="blockentry")
        self.blockentrylist = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="blockentrylist")
        self.readlater = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="readlater")
        self.searchview = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="searchview")

        self.usertags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="usertags")
        self.compactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="compactedtags")
        self.usercompactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="usercompactedtags")
        self.entrycompactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="entrycompactedtags")
        self.uservotes = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="uservotes")
        self.modelfiles = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="modelfiles")
        self.entrycompactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="entrycompactedtags")
        self.entryvisithistory = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="entryvisithistory")
        self.entrytransitionhistory = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="entrytransitionhistory")
        self.searchhistory = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="searchhistory")

    def create_engine(db_file):
        engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
        return engine

    def truncate(self):
        self.entries_table.truncate()
        self.sources_table.truncate()
        self.configurationentry.truncate()
        self.applogging.truncate()
        self.backgroundjob.truncate()
        self.backgroundjobhistory.truncate()
        self.blockentry.truncate()
        self.blockentrylist.truncate()
        self.entry_rules.truncate()
        self.readlater.truncate()
        self.searchview.truncate()
        self.socialdata.truncate()
        self.sourceoperationaldata.truncate()
        self.usertags.truncate()
        self.compactedtags.truncate()
        self.entrycompactedtags.truncate()
        self.uservotes.truncate()

        table = ReflectedTable(engine=self.engine, connection=self.connection)
        table.vacuum()

    def get_table(self, table_name):
        return ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name=table_name)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

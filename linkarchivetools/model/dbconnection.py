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
    def __init__(self, db_file):
        self.db_file = db_file

        self.engine = DbConnection.create_engine(self.db_file)

        self.connection = self.engine.connect()

        sql_text = f"PRAGMA journal_mode=WAL;"
        self.connection.execute(text(sql_text))
        self.connection.commit()

        self.entries_table = ReflectedEntryTable(engine=self.engine, connection=self.connection)
        self.sources_table = ReflectedSourceTable(engine=self.engine, connection=self.connection)
        self.entry_rules = ReflectedEntryRules(engine=self.engine, connection=self.connection)
        self.configurationentry = ReflectedConfigurationEntry(engine=self.engine, connection=self.connection)
        self.sourceoperationaldata = ReflectedSourceOperationalData(engine=self.engine, connection=self.connection)
        self.applogging = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="applogging")
        self.socialdata = ReflectedSocialData(engine=self.engine, connection=self.connection)
        self.backgroundjob = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="backgroundjob")
        self.usertags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="usertags")
        self.compactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="compactedtags")
        self.usercompactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="usercompactedtags")
        self.entrycompactedtags = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="entrycompactedtags")
        self.uservotes = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="uservotes")
        self.readlater = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="readlater")
        self.searchview = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="searchview")
        self.backgroundjobhistory = ReflectedGenericTable(engine=self.engine, connection=self.connection, table_name="backgroundjobhistory")

    def create_engine(db_file):
        engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
        return engine

    def truncate(self):
        self.entries_table.truncate()
        self.sources_table.truncate()

        table = ReflectedTable(engine=self.engine, connection=self.connection)
        table.vacuum()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

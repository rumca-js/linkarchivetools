"""
Filters out redundant things from database.
Normally for views, analysis you do not need no temporary tables.
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path
import argparse
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
)
from linkarchivetools.model.definitions import create_tables
from linkarchivetools.model import (
    DbConnection,
    Sources,
    Entries,
)
from linkarchivetools.utils.reflected import (
    ReflectedTable,
    ReflectedSourceTable,
    ReflectedEntryTable,
)
from linkarchivetools.tableconfig import (
    get_tables,
    get_user_tables,
    get_dynamic_tables,
    get_configuration_tables,
)


def print_time_diff(start_time):
    elapsed_time_seconds = time.time() - start_time
    elapsed_minutes = int(elapsed_time_seconds // 60)
    elapsed_seconds = int(elapsed_time_seconds % 60)
    print(f"Time: {elapsed_minutes}:{elapsed_seconds}")


class DbUpdate(object):
    """
    Filter class
    """

    def __init__(self, db=None, engine=None, connection=None):
        self.input_db = db
        self.engine = engine
        self.connection = connection
        self.setup()

    def setup(self):
        if not self.connection:
            if self.engine:
                self.connection = self.engine.connect()
            elif self.input_db:
                path = Path(self.input_db)
                if not path.exists():
                    return

                self.engine = create_engine(f"sqlite:///{self.input_db}")
                self.connection = self.engine.connect()
            else:
                print("No db, no engine: Cannot establish connection for filtering")

    def create_tables(self):
        if self.input_db:
            path = Path(self.input_db)
            if not path.exists():
                path.touch()

            self.engine = create_engine(f"sqlite:///{self.input_db}")
            if self.engine:
                create_tables(self.engine)
        elif self.engine:
            create_tables(self.engine)

        self.setup()

    def is_table(self, table_name):
        reflected_table = ReflectedTable(engine=self.engine, connection=self.connection)
        return reflected_table.is_table(table_name)

    def is_column(self, table_name, column_name):
        reflected_table = ReflectedTable(engine=self.engine, connection=self.connection)
        return reflected_table.is_column(table_name, column_name)

    def is_valid(self) -> bool:
        if not self.engine:
            return False
        return True

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def truncate_all_tables(self):
        """
        Truncates tables - all
        """
        truncate_tables = get_tables()
        self.truncate_tables(truncate_tables)

    def truncate_tables(self, tables):
        """
        Removes all users data
        """
        reflected_table = ReflectedTable(engine=self.engine, connection=self.connection)

        for table in tables:
            reflected_table.truncate_table(table)

    def truncate_user_tables(self):
        """
        Removes all users tables
        """
        truncate_tables = get_user_tables()
        self.truncate_tables(truncate_tables)

    def truncate_dynamic_data(self):
        """
        Removes dynamic data
        """
        truncate_tables = get_dynamic_tables()
        self.truncate_tables(truncate_tables)

    def truncate_configuration_tables(self):
        """
        Removes configuration tables probably not use by other people
        """
        truncate_tables = get_configuration_tables()
        self.truncate_tables(truncate_tables)

    def delete_entries_by_confition(self, conditions):
        table = ReflectedTable(engine=self.engine, connection=self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE {conditions};"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def delete_entries_non_bookmarked(self):
        table = ReflectedTable(engine=self.engine, connection=self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False;"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def delete_entries_no_votes(self):
        table = ReflectedTable(engine=self.engine, connection=self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def delete_entries_redundant(self):
        """
        Not bookmarked AND without votes are redundant
        """
        table = ReflectedTable(engine=self.engine, connection=self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False AND page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def insert_links(self, links):
        table = ReflectedEntryTable(engine=self.engine, connection=self.connection)

        for link in links:
            json = {}
            json["link"] = link
            if not table.exists(link=link):
                status = table.insert_json(json)

        table.close
        return True

    def insert_source_urls(self, urls):
        table = ReflectedSourceTable(engine=self.engine, connection=self.connection)

        for url in urls:
            json = {}
            json["url"] = url
            if not table.exists(url=url):
                table.insert_json(json)

        table.close
        return True

    def obfuscate(self):
        """
        Does not remove user tables
        TODO: should remove certain fields from configurationentry
        """
        self.obfuscate_user_table()

        self.truncate_tables({"browser", "dataexport", "usersearchhistory", "apikeys", "credentials", "readlater"})

    def obfuscate_user_table(self):
        """
        Remove passwords from the database
        TODO - implement if only connection was passed
        """
        table_name = 'user'

        if self.engine:
            destination_engine = self.engine

            destination_metadata = MetaData()
            destination_table = Table(table_name, destination_metadata, autoload_with=destination_engine)

            columns = destination_table.columns.keys()
            is_superuser_index = columns.index('is_superuser')

            with destination_engine.connect() as destination_connection:
                result = destination_connection.execute(destination_table.select())

                for row in result:
                    update_stmt = destination_table.update().where(destination_table.c.id == row[0]).values(password='')
                    destination_connection.execute(update_stmt)

                    update_stmt = destination_table.update().where(destination_table.c.id == row[0]).values(email='')
                    destination_connection.execute(update_stmt)

                    if is_superuser_index:
                        if row[is_superuser_index]:
                            update_stmt = destination_table.update().where(destination_table.c.id == row[0]).values(username='admin')
                            destination_connection.execute(update_stmt)
                        else:
                            update_stmt = destination_table.update().where(destination_table.c.id == row[0]).values(username='non-admin')
                            destination_connection.execute(update_stmt)

                destination_connection.commit()

    def vacuum(self):
        """
        Not bookmarked AND without votes are redundant
        """
        table = ReflectedTable(engine=self.engine, connection=self.connection)
        table.vacuum()
        table.close()


class DbUpdaetParser():
    def parse(self):
        parser = argparse.ArgumentParser(description="DB manipulation program")
        parser.add_argument("--db", help="DB to be filtered")

        # main
        parser.add_argument("--create-tables", action="store_true", help="Creates tables. Even missing ones")

        # truncate
        parser.add_argument("--truncate-table", help="Truncate table")
        parser.add_argument("--truncate-tables", help="Truncate specified tables")
        parser.add_argument("--truncate-all-tables", action="store_true", help="Truncate all tables")

        parser.add_argument("--trunc-dynamic-data", action="store_true", help="Truncates dynamic tables")
        parser.add_argument("--trunc-configuration", action="store_true", help="Removes uneceesary configuration")
        parser.add_argument("--trunc-search-data", action="store_true", help="Removes all search data")
        parser.add_argument("--trunc-visits-data", action="store_true", help="Removes all visit data")
        parser.add_argument("--trunc-no-users", action="store_true", help="Prepares for setup with no users")

        # delete
        parser.add_argument("--delete-non-bookmarked", action="store_true", help="Removes non bookmarked")
        parser.add_argument("--delete-no-votes", action="store_true", help="Removes entries without a vote")
        parser.add_argument("--delete-redundant", action="store_true", help="Removes entries that are redundant - not bookmarked, no votes")

        # insert
        parser.add_argument("--insert-link", help="Inserts link")
        parser.add_argument("--insert-links", help="Inserts links")
        parser.add_argument("--insert-source-url", help="Inserts source urls")
        parser.add_argument("--insert-source-urls", help="Inserts source urls")

        # update
        parser.add_argument("--update-entries", action="store_true", help="Updates entries")
        parser.add_argument("--update-sources", action="store_true", help="Updates sources")
        parser.add_argument("--process-sources", action="store_true", help="Processes sources")

        # other
        parser.add_argument("--obfuscate", action="store_true", help="Obfuscates private data")
        parser.add_argument("-v", "--verbosity", help="Verbosity level")

        args = parser.parse_args()

        return parser, args


def main():
    start_time = time.time()
    parser = DbUpdaetParser()
    parser, args = parser.parse()

    update_controller = DbUpdate(db=args.db)

    if args.create_tables:
        update_controller.create_tables()

    if not update_controller.is_valid():
        return

    if args.truncate_table:
        update_controller.truncate_tables({args.truncate_table})
    if args.truncate_tables:
        tables = args.truncate_tables.split(",")
        update_controller.truncate_tables(set(tables))
    if args.truncate_all_tables:
        update_controller.truncate_all_tables()
    if args.trunc_no_users:
        update_controller.truncate_user_tables()
    if args.trunc_dynamic_data:
        update_controller.truncate_dynamic_data()
    if args.trunc_configuration:
        update_controller.truncate_configuration_tables()
    if args.trunc_search_data:
        update_controller.truncate_tables(get_search_tables())
    if args.trunc_visits_data:
        update_controller.truncate_tables(get_visits_tables())

    if args.delete_non_bookmarked:
        update_controller.delete_entries_non_bookmarked()
    if args.delete_no_votes:
        update_controller.delete_entries_no_votes()
    if args.delete_redundant:
        update_controller.delete_entries_redundant()

    if args.obfuscate:
        update_controller.obfuscate()

    # inserts are after truncates, if one wants to clear search
    # then to insert some

    if args.insert_link:
        update_controller.insert_links({args.insert_link})
    if args.insert_links:
        links = args.insert_links.split(",")
        update_controller.insert_links(set(links))

    if args.insert_source_url:
        update_controller.insert_source_urls({args.insert_source_url})
    if args.insert_source_urls:
        urls = args.insert_source_urls.split(",")
        update_controller.insert_source_urls(set(urls))

    if args.update_entries:
        db_connection = DbConnection(engine=update_controller.engine, connection=update_controller.connection)
        entries_controller = Entries(connection=db_connection)
        entries_controller.update_all()
    if args.update_sources:
        db_connection = DbConnection(engine=update_controller.engine, connection=update_controller.connection)
        sources_controller = Sources(connection=db_connection)
        sources_controller.update_all()
    if args.process_sources:
        db_connection = DbConnection(engine=update_controller.engine, connection=update_controller.connection)
        sources_controller = Sources(connection=db_connection)
        sources_controller.process_all()

    update_controller.vacuum()
    update_controller.close()

    print_time_diff(start_time)


if __name__ == "__main__":
    main()

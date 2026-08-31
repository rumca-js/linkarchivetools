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
from linkarchivetools.utils.reflected import ReflectedTable
from linkarchivetools.tableconfig import *


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
            if self.input_db:

                path = Path(self.input_db)
                if not path.exists():
                    print("File {} does not exist".format(path))
                    return

                self.engine = create_engine(f"sqlite:///{self.input_db}")
                self.connection = self.engine.connect()
            elif self.engine:
                self.connection = self.engine.connect()
            else:
                print("No db, no engine: Cannot establish connection for filtering")

    def create_tables(self):
        if self.input_db:
            path = Path(self.input_db)
            if not path.exists():
                path.touch()

            engine = create_engine(f"sqlite:///{self.input_db}")
            if engine:
                create_tables(engine)
        elif self.engine:
            create_tables(self.engine)

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

    def truncate_all(self):
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
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE {conditions};"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def delete_entries_non_bookmarked(self):
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False;"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def delete_entries_no_votes(self):
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def delete_entries_redundant(self):
        """
        Not bookmarked AND without votes are redundant
        """
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False AND page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

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


def parse():
    parser = argparse.ArgumentParser(description="DB manipulation program")
    parser.add_argument("--db", help="DB to be filtered")

    parser.add_argument("--create-tables", action="store_true", help="Creates tables. Even missing ones")
    parser.add_argument("--truncate-tables", help="Truncate table(s). Pass table names")

    parser.add_argument("--trunc-dynamic-data", action="store_true", help="Truncates dynamic tables")
    parser.add_argument("--trunc-configuration", action="store_true", help="Removes uneceesary configuration")
    parser.add_argument("--trunc-search-data", action="store_true", help="Removes all search data")
    parser.add_argument("--trunc-visits-data", action="store_true", help="Removes all visit data")
    parser.add_argument("--delete-non-bookmarked", action="store_true", help="Removes non bookmarked")
    parser.add_argument("--delete-no-votes", action="store_true", help="Removes entries without a vote")
    parser.add_argument("--delete-redundant", action="store_true", help="Removes entries that are redundant - not bookmarked, no votes")

    parser.add_argument("--no-users", action="store_true", help="Prepares for setup with no users")
    parser.add_argument("--obfuscate", action="store_true", help="Obfuscates private data")

    parser.add_argument("-v", "--verbosity", help="Verbosity level")

    args = parser.parse_args()

    return parser, args


def main():
    start_time = time.time()
    parser, args = parse()

    update_controller = DbUpdate(db=args.db)
    if not update_controller.is_valid():
        return

    entries_changed = False
    if args.create_tables:
        entries_changed = True
        update_controller.create_tables()
    if args.truncate_tables:
        entries_changed = True
        update_controller.truncate_tables({args.truncate})
    if args.obfuscate:
        entries_changed = True
        update_controller.obfuscate()
    if args.trunc_no_users:
        entries_changed = True
        update_controller.truncate_user_tables()
    if args.trunc_dynamic_data:
        entries_changed = True
        update_controller.truncate_dynamic_data()
    if args.delete_non_bookmarked:
        entries_changed = True
        update_controller.delete_entries_non_bookmarked()
    if args.delete_no_votes:
        entries_changed = True
        update_controller.delete_entries_no_votes()
    if args.delete_redundant:
        entries_changed = True
        update_controller.delete_entries_redundant()
    if args.trunc_configuration_tables:
        update_controller.truncate_configuration_tables()
    if args.search_data:
        update_controller.truncate_tables(get_search_tables())
    if args.trunc_visits_data:
        update_controller.truncate_tables(get_visits_tables())

    if entries_changed:
        update_controller.cleanup_tables()

    update_controller.vacuum()
    update_controller.close()

    print_time_diff(start_time)


if __name__ == "__main__":
    main()

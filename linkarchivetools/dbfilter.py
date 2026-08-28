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

from linkarchive.utils.reflected import ReflectedTable
from linkarchive.tableconfig import *


class DbFilter(object):
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
        reflected_table = ReflectedTable(self.engine, self.connection)

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
    parser = argparse.ArgumentParser(description="Data filter program")
    parser.add_argument("--db", default="places.db", help="DB to be filtered")

    parser.add_argument("--bookmarked", action="store_true", help="Removes non bookmarked")
    parser.add_argument("--votes", action="store_true", help="Removes entries without a vote")
    parser.add_argument("--no-users", action="store_true", help="Prepares for setup with no users")
    parser.add_argument("--obfuscate", action="store_true", help="Obfuscates private data")
    parser.add_argument("--dynamic-data", action="store_true", help="Truncates dynamic tables")
    parser.add_argument("--redundant", action="store_true", help="Removes entries that are redundant - not bookmarked, no votes")
    parser.add_argument("--configuration", action="store_true", help="Removes uneceesary configuration")
    parser.add_argument("--domains", action="store_true", help="Removes domains")
    parser.add_argument("--search-data", action="store_true", help="Removes search data")
    parser.add_argument("--visits-data", action="store_true", help="Removes visit data")

    parser.add_argument("-v", "--verbosity", help="Verbosity level")

    args = parser.parse_args()

    return parser, args


def main():
    start_time = time.time()
    parser, args = parse()

    thefilter = DbFilter(db=args.db)
    if not thefilter.is_valid():
        return

    entries_changed = False
    if args.no_users:
        entries_changed = True
        thefilter.truncate_user_tables()
    if args.obfuscate:
        entries_changed = True
        thefilter.obfuscate()
    if args.dynamic_data:
        entries_changed = True
        thefilter.truncate_dynamic_data()
    if args.bookmarked:
        entries_changed = True
        thefilter.delete_entries_non_bookmarked()
    if args.votes:
        entries_changed = True
        thefilter.delete_entries_no_votes()
    if args.redundant:
        entries_changed = True
        thefilter.delete_entries_redundant()
    if args.configuration_tables:
        thefilter.truncate_configuration_tables()
    if args.search_data:
        thefilter.truncate_tables(get_search_tables())
    if args.visits_data:
        thefilter.truncate_tables(get_visits_tables())
    if args.domains:
        thefilter.truncate_tables({"domains"})

    if entries_changed:
        thefilter.cleanup_tables()

    thefilter.vacuum()
    thefilter.close()

    end_time = time.time()
    print(f"Done in {end_time}")


if __name__ == "__main__":
    main()

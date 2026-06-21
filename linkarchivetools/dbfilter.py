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

from sqlalchemy import create_engine
from .utils.reflected import ReflectedTable
from .tableconfig import get_tables, get_truncate_tables_no_users, get_truncate_tables_internet


class DbFilter(object):
    """
    Filter class
    """

    def __init__(self, input_db, output_db):
        self.input_db = input_db
        self.output_db = output_db
        self.engine = None
        self.connection = None
        self.setup()

    def setup(self):
        path = Path(self.input_db)
        if not path.exists():
            print("File {} does not exist".format(path))
            return

        new_path = Path(self.output_db)
        if new_path.exists():
            new_path.unlink()

        shutil.copy(self.input_db, self.output_db)

        self.engine = create_engine(f"sqlite:///{self.output_db}")
        self.connection = self.engine.connect()

    def is_valid(self) -> bool:
        if not self.engine:
            return False
        return True

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def truncate_no_users(self):
        """
        TODO remove these hardcoded tables
        with something from table_config
        though it seems it should not clear linkdatamodel
        """
        reflected_table = ReflectedTable(self.engine, self.connection)

        truncate_tables = get_truncate_tables_no_users()

        for table in truncate_tables:
            reflected_table.truncate_table(table)

    def truncate_internet(self):
        """
        TODO remove these hardcoded tables
        with something from table_config
        though it seems it should not clear linkdatamodel
        """
        reflected_table = ReflectedTable(self.engine, self.connection)

        truncate_tables = get_truncate_tables_internet()

        for table in truncate_tables:
            reflected_table.truncate_table(table)

    def filter(self, conditions):
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE {conditions};"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def filter_bookmarks(self):
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False;"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def filter_votes(self):
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def filter_redundant(self):
        """
        Not bookmarked AND without votes are redundant
        """
        table = ReflectedTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False AND page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def cleanup_tables(self):
        """
        table = ReflectedGenericTable(self.engine, self.connection, "entrycompactedtags")
        compacted = table.get_where({})
        for row in compacted


        entrycompactedtags
        usertags
        usercompactedtags
        uservotes
        usercomments
        userbookmarks
        userentrytransitionhistory
        userentryvisithistory
        """
        pass


def parse():
    parser = argparse.ArgumentParser(description="Data analyzer program")
    parser.add_argument("--db", default="places.db", help="DB to be scanned")
    parser.add_argument("--output-db", default="new.db", help="DB to be created")

    parser.add_argument("--bookmarked", action="store_true", help="export bookmarks")
    parser.add_argument("--votes", action="store_true", help="export if votes is > 0")
    parser.add_argument("--truncate-no-users", action="store_true", help="Truncates tables no users")
    parser.add_argument("--truncate-internet", action="store_true", help="Truncates tables for public")

    parser.add_argument("-v", "--verbosity", help="Verbosity level")

    args = parser.parse_args()

    return parser, args


def main():
    start_time = time.time()
    parser, args = parse()

    thefilter = DbFilter(args.db, args.output_db)
    if not thefilter.is_valid():
        return

    entries_changed = False
    if args.truncate_no_users:
        thefilter.truncate_no_users()
    if args.truncate_internet:
        thefilter.truncate_internet()
    if args.bookmarked:
        entries_changed = True
        thefilter.filter_bookmarks()
    if args.votes:
        entries_changed = True
        thefilter.filter_votes()

    if entries_changed:
        thefilter.cleanup_tables()

    thefilter.vacuum()
    thefilter.close()

    end_time = time.time()
    print(f"Done in {end_time}")


if __name__ == "__main__":
    main()

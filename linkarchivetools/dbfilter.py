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
from .utils.reflected import *


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

    def truncate(self):
        table = ReflectedEntryTable(self.engine, self.connection)

        table.truncate_table("userentrytransitionhistory")
        table.truncate_table("userentryvisithistory")
        table.truncate_table("usersearchhistory")
        table.truncate_table("uservotes")
        table.truncate_table("usercompactedtags")
        table.truncate_table("usercomments")
        table.truncate_table("userbookmarks")
        table.truncate_table("user")
        table.truncate_table("userconfig")
        table.truncate_table("sourcedatamodel")
        table.truncate_table("sourcecategories")
        table.truncate_table("sourcesubcategories")
        table.truncate_table("readlater")
        table.truncate_table("modelfiles")
        table.truncate_table("gateway")
        table.truncate_table("entryrules")
        table.truncate_table("domains")
        table.truncate_table("dataexport")
        table.truncate_table("configurationentry")
        table.truncate_table("compactedtags")
        table.truncate_table("blockentrylist")

    def filter(self, conditions):
        table = ReflectedEntryTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE {conditions};"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def filter_bookmarks(self):
        table = ReflectedEntryTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False;"
        # TODO delete depnded things
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def filter_votes(self):
        table = ReflectedEntryTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()

    def filter_redundant(self):
        """
        Not bookmarked AND without votes are redundant
        """
        table = ReflectedEntryTable(self.engine, self.connection)

        sql_text = f"DELETE FROM linkdatamodel WHERE bookmarked=False AND page_rating_votes=0;"
        table.run_sql(sql_text)
        table.vacuum()
        table.close()


def parse():
    parser = argparse.ArgumentParser(description="Data analyzer program")
    parser.add_argument("--db", default="places.db", help="DB to be scanned")
    parser.add_argument("--output-db", default="new.db", help="DB to be created")
    parser.add_argument("--bookmarked", action="store_true", help="export bookmarks")
    parser.add_argument("--votes", action="store_true", help="export if votes is > 0")
    parser.add_argument("--clean", action="store_true", help="cleans db from tables")
    parser.add_argument("-v", "--verbosity", help="Verbosity level")

    args = parser.parse_args()

    return parser, args


def main():
    start_time = time.time()
    parser, args = parse()

    thefilter = DbFilter(args.db, args.output_db)
    if not thefilter.is_valid():
        return

    thefilter.truncate()
    if args.bookmarked:
        thefilter.filter_bookmarks()
    if args.votes:
        thefilter.filter_votes()

    thefilter.vacuum()
    thefilter.close()

    end_time = time.time()
    print(f"Done in {end_time}")


if __name__ == "__main__":
    main()

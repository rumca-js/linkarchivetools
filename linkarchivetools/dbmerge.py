import shutil
import os
from pathlib import Path
from sqlalchemy import create_engine

from .utils.reflected import *


class DbMerge(object):
    """
    Converter DB -> feeds.
    """

    def __init__(
        self,
        input_dbs=None,
        output_db=None,
        verbose=True,
    ):
        """
        Constructor
        @param read_internet_links Read links to find RSS feeds
        @param update_feed Many things are copied from original entry.
                          If this setting is true, feed entry fetches title, and other properties
        """
        self.input_dbs = input_dbs
        self.output_db = output_db
        self.verbose = verbose

    def convert(self):
        """
        API
        """
        input_dbs = self.input_dbs
        if len(input_dbs) < 2:
            return False

        size_zero = os.path.getsize(input_dbs[0])
        size_one = os.path.getsize(input_dbs[1])

        if size_zero > size_one:
            bigger_db = input_dbs[0]
            smaller_db = input_dbs[1]
        else:
            bigger_db = input_dbs[1]
            smaller_db = input_dbs[0]

        dst = Path(self.output_db)

        if dst.exists():
            dst.unlink()

        shutil.copy(bigger_db, self.output_db)

        self.src_engine = create_engine(f"sqlite:///{smaller_db}")
        self.dst_engine = create_engine(f"sqlite:///{self.output_db}")

        with self.src_engine.connect() as connection:
            self.src_connection = connection
            with self.dst_engine.connect() as dst_connection:
                self.dst_connection = dst_connection
                self.convert_entries()

    def convert_entries(self):
        src_table = ReflectedEntryTable(self.src_engine, self.src_connection)
        for entry in src_table.get_entries_good():
            dst_table = ReflectedEntryTable(self.dst_engine, self.dst_connection)
            if not dst_table.is_entry_link(entry.link):
                self.convert_entry(entry)
            elif self.verbose:
                print(f"Entry {entry.link} is already present")

    def convert_entry(self, entry):
        if self.verbose:
            print(f"Converting entry {entry.link}")

        copier = EntryCopier(
                             src_engine=self.src_engine,
                             src_connection=self.src_connection,
                             dst_engine = self.dst_engine,
                             dst_connection=self.dst_connection) 
        copier.copy_entry(entry)

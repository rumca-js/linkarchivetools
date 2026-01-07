"""
@brief Converts JSON files to SQLite DB

SQLite can easily be imported and used by other projects.
"""

import os
import sqlite3
import json
import argparse
import time
from pathlib import Path
from sqlalchemy import create_engine
from dateutil import parser

from .utils.reflected import *


class DirReader(object):
    def __init__(self, source_files_directory, accepted_extensions=None):
        self.dir = source_files_directory
        if accepted_extensions is None:
            self.accepted_extensions = [".json"]

    def get_files(self):
        file_list = []
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                file_split = os.path.splitext(file)
                if file_split[1] in self.accepted_extensions:
                    file_list.append(os.path.join(root, file))

        file_list = sorted(file_list)
        return file_list


class JSON2Db(object):
    """
    Performs actual conversion between from JSON to DB
    """

    def __init__(self, input_file=None, input_dir=None, output_db=None, preserve_id=False, vote_threshold=None, verbose=False):
        self.input_file = input_file
        self.input_dir = input_dir
        self.output_db = output_db
        self.preserve_id = preserve_id
        self.vote_threshold = vote_threshold
        self.verbose = verbose

        if self.input_dir:
            self.file_reader = DirReader(source_files_directory=self.input_dir)
            self.files = self.file_reader.get_files()
        elif self.input_file:
            self.file_reader = None
            self.files = [self.input_file]
        else:
            self.file_reader = None
            self.files = []

    def convert(self):
        #path = Path(self.output_db)
        #if path.exists():
        #    path.unlink()

        self.engine = create_engine(f"sqlite:///{self.output_db}")
        with self.engine.connect() as connection:
            self.connection = connection

            total_num_files = len(self.files)

            for row, afile in enumerate(self.files):
                print("[{}/{}]: file:{}".format(row, total_num_files, afile))
                self.convert_file(afile)

    def convert_file(self, file_name):
        data = self.read_file(file_name)
        if not data:
            return

        total_rows = len(data)

        for row, entry in enumerate(data):
            entry = self.prepare_entry(entry)
            if "link" in entry:
                if self.preserve_id:
                    if "id" not in entry:
                        print("Entry {} is missing ID".format(entry["link"]))
                        continue
                else:
                    entry["id"] = row

                if self.is_entry_to_be_added(entry):
                    table = ReflectedEntryTable(engine=self.engine, connection=self.connection)
                    if table.insert_entry_json(entry) is not None:
                        if self.verbose:
                            print(
                                " -> [{}/{}] Link:{} Added".format(
                                    row, total_rows, entry["link"]
                                )
                            )
                    else:
                        print(
                            " -> [{}/{}] Link:{} NOT Added".format(
                                row, total_rows, entry["link"]
                            )
                        )
                else:
                    if self.verbose:
                        print(
                            " -> [{}/{}] Link:{} Skipped".format(
                                row, total_rows, entry["link"]
                            )
                        )

    def prepare_entry(self, entry):
        """
        Drops any unwelcome keys
        """
        table = ReflectedEntryTable(engine=self.engine, connection=self.connection)
        columns = table.get_column_names()
        keys = list(entry.keys())

        diff = list(set(keys) - set(columns))
        for item in diff:
            del entry[item]

        for key in entry:
            if key.startswith("date"):
                if entry[key]:
                    entry[key] = parser.parse(entry[key])

        return entry

    def is_entry_to_be_added(self, entry):
        # entry already exists
        table = ReflectedEntryTable(engine=self.engine, connection=self.connection)
        if "id" in entry and table.is_entry_id(entry["id"]):
            return False
        if "link" in entry and table.is_entry_link(entry["link"]):
            return False

        if self.vote_threshold:
            if "page_rating_votes" in entry:
                if entry["page_rating_votes"]:
                    if int(entry["page_rating_votes"]) < self.vote_threshold:
                        return False
                    else:
                        return True
                return False
            return False

        return True

    def read_file_contents(self, file_name):
        with open(file_name, "r") as f:
            return f.read()

    def read_file(self, file_name):
        text = self.read_file_contents(file_name)

        try:
            j = json.loads(text)

            if "links" in j:
                return j["links"]
            if "sources" in j:
                return j["sources"]

            return j
        except Exception as e:
            print("Could not read file: {}".format(afile))


class Parser(object):
    def parse(self):
        self.parser = argparse.ArgumentParser(description="Data converter program")
        self.parser.add_argument("--input-file", help="File to be scanned")
        self.parser.add_argument("--input-dir", help="Directory to be scanned")
        self.parser.add_argument(
            "--output-db", default="converted.sqlite", help="Output db name"
        )
        self.parser.add_argument(
            "--preserve-id", action="store_true", help="Preserves ID of objects"
        )
        self.parser.add_argument("--vote-min", help="Minimum amount of entry vote")
        self.parser.add_argument("--language", help="Accept language")  # TODO implement
        self.parser.add_argument("--entries", help="Convert entries")  # TODO implement
        self.parser.add_argument("--sources", help="Convert sources")  # TODO implement
        self.parser.add_argument(
            "--verbose", action="store_true", help="Shows more info"
        )

        self.args = self.parser.parse_args()

        if self.args.dir:
            self.dir = self.args.dir
        else:
            self.dir = None

        if self.args.preserve_id:
            self.preserve_id = self.args.preserve_id
        else:
            self.preserve_id = None

        if self.args.vote_min:
            self.vote_min = int(self.args.vote_min)
        else:
            self.vote_min = None


def main():
    print("Starting processing")
    parser = Parser()
    parser.parse()

    try:
        start_time = time.time()

        c = JSON2Db(input_file = parser.args.input_file, input_dir=parser.args.input_dir, output_db = parser.args.output_db)
        c.convert()

        elapsed_time_seconds = time.time() - start_time
        elapsed_minutes = int(elapsed_time_seconds // 60)
        elapsed_seconds = int(elapsed_time_seconds % 60)
        print(f"Time: {elapsed_minutes}:{elapsed_seconds}")

    except Exception as e:
        print("Exception: {}".format(e))
    except KeyboardInterrupt as e:
        print("Exception: {}".format(e))

    db.close()
    print("Processing DONE")


if __name__ == "__main__":
    main()

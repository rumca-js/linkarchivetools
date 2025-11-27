"""
Converts database to JSON.
"""

import os
import sys
import json
import shutil
from pathlib import Path
import argparse

from sqlalchemy import create_engine
from .utils.reflected import *


class Db2JSON(object):

    def __init__(self, input_db, output_dir, format=None, rows_max=1000):
        self.input_db = input_db
        self.output_dir = output_dir

        self.format = format
        self.rows_max = rows_max

        self.file_index = 0
        self.entry_index = 0
        self.handle = None

        self.rows = []

        self.processed = 0
        self.all = 0

        self.setup()

    def setup(self):
        path = Path(self.input_db)
        if not path.exists():
            print("File {} does not exist".format(path))
            return

        if self.output_dir and self.output_dir != ".":
            new_path = Path(self.output_dir)
            if new_path.exists():
                shutil.rmtree(new_path)
            new_path.mkdir()

        self.engine = create_engine(f"sqlite:///{self.input_db}")

    def write(self, entry):
        """Write entries to the specified directory, 1000 per file."""
        if self.handle == None:
            file_path = str(self.get_file_path())
            self.handle = open(file_path, "w")

        row = self.get_entry_json_data(entry)

        self.rows.append(row)

        self.entry_index += 1

        sys.stdout.write(f"{self.file_index}/{self.entry_index:04d}\r")

        if self.entry_index == self.rows_max:
            self.file_index += 1
            self.entry_index = 0
            self.finish_stream()

            file_path = str(self.get_file_path())
            self.handle = open(file_path, "w")

    def get_entry_json_data(self, entry):
        date_published = entry.date_published
        if date_published:
            date_published = date_published.isoformat()

        date_dead_since = entry.date_dead_since
        if date_dead_since:
            date_dead_since = date_dead_since.isoformat()

        row = {
            "link": entry.link,
            "description": entry.description,
            "author": entry.author,
            "album": entry.album,
            "bookmarked": entry.bookmarked,
            "date_dead_since": date_dead_since,
            "date_published": date_published,
            "language": entry.language,
            "manual_status_code": entry.manual_status_code,
            "page_rating": entry.page_rating,
            "page_rating_contents": entry.page_rating_contents,
            "page_rating_votes": entry.page_rating_votes,
            "page_rating_visits": entry.page_rating_visits,
            "permanent": entry.permanent,
            "source_url": entry.source_url,
            "status_code": entry.status_code,
            "thumbnail": entry.thumbnail,
            "title": entry.title,
            "age": entry.age,
            "id": entry.id,
        }

        social_table = ReflectedSocialData(self.engine, self.connection)
        social_data = social_table.get(entry.id)
        if social_data:
            row.setdefault("thumbs_up", social_data.thumbs_up)
            row.setdefault("thumbs_down", social_data.thumbs_down)
            row.setdefault("view_count", social_data.view_count)
            row.setdefault("rating", social_data.rating)
            row.setdefault("upvote_ratio", social_data.upvote_ratio)
            row.setdefault("upvote_diff", social_data.upvote_diff)
            row.setdefault("upvote_view_ratio", social_data.upvote_view_ratio)
            row.setdefault("stars", social_data.stars)
            row.setdefault("followers_count", social_data.followers_count)

        tags_table = ReflectedUserTags(self.engine, self.connection)
        tags = tags_table.get_tags(entry.id)
        row["tags"] = tags

        return row

    def get_file_path(self):
        filename = "{}_{}.json".format(self.format, str(self.file_index))
        if self.output_dir and self.output_dir != ".":
            return Path(self.output_dir) / filename
        else:
            return Path(filename)

    def close(self):
        if self.handle:
            self.finish_stream()
        self.handle = None

    def finish_stream(self):
        if not self.handle:
            return

        try:
            string = json.dumps(self.rows, indent=4)
            self.handle.write(string)
        except ValueError as e:
            print(f"Error writing file {file_path}: {e}")
        self.handle.close()
        self.rows = []

    def convert(self):
        with self.engine.connect() as connection:
            self.connection = connection
            table = ReflectedEntryTable(self.engine, connection)

            for entry in table.get_entries():
                # print(entry)
                self.write(entry)


def parse():
    parser = argparse.ArgumentParser(description="Data analyzer program")
    parser.add_argument("--db", default="places.db", help="DB to be scanned")
    parser.add_argument("--output-dir", default="json", help="Output directory")
    parser.add_argument(
        "--rows-max", default=1000, action="store_true", help="Number of rows per file"
    )
    parser.add_argument("-f", "--format", default="entries", help="file name format")
    parser.add_argument("-v", "--verbosity", help="Verbosity level")

    args = parser.parse_args()

    return parser, args


def main():
    parser, args = parse()

    f = Db2JSON(
        input_db=args.db,
        output_dir=args.output_dir,
        format=args.format,
        rows_max=args.rows_max,
    )
    f.convert()
    f.close()


if __name__ == "__main__":
    main()

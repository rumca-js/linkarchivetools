"""
Provides information about archive

Examples:
 - What was said about Musk
  $ --search "title=*Musk*"
 - What was said about Musk (title, link, description, etc)
  $ --search "Musk"

TODO
 - Output formats? (md)?
 - Maybe it could produce a chart?

"""

import argparse
import time
import os
import json
from sqlalchemy import create_engine

from .utils.omnisearch import SingleSymbolEvaluator, EquationEvaluator, OmniSearch
from .utils.alchemysearch import (
    AlchemySymbolEvaluator,
    AlchemyEquationEvaluator,
    AlchemySearch,
)
from .utils.reflected import (
    ReflectedEntryTable,
    ReflectedUserTags,
    ReflectedSocialData,
)


def print_time_diff(start_time):
    elapsed_time_seconds = time.time() - start_time
    elapsed_minutes = int(elapsed_time_seconds // 60)
    elapsed_seconds = int(elapsed_time_seconds % 60)
    print(f"Time: {elapsed_minutes}:{elapsed_seconds}")


class RowHandler(object):

    def __init__(self, args=None, engine=None, connection=None):
        self.args = args
        self.start_time = time.time()
        self.engine = engine
        self.connection = connection

        self.files = []

        self.total_entries = 0
        self.good_entries = 0
        self.dead_entries = 0

    def print_entry(self, entry):
        level = self.args.verbosity
        if level is None or level == 0:
            return

        text = ""

        if self.args.description:
            print("---------------------")

        text = "[{:03d}] {}".format(entry.page_rating_votes, entry.link)

        if self.args.title:
            if entry.title:
                text += " " + entry.title

        if self.args.source:
            source_id = entry.source
            if source_id:
                r = ReflectedEntryTable(self.engine, self.connection)
                source = r.get_source(source_id)
                text += " [{}]".format(source.title)

        print(text)

        if self.args.date_published:
            date_published = entry.date_published
            if date_published:
                print(date_published)

        if self.args.description:
            description = entry.description
            if description:
                print(description)

        if self.args.tags:
            tags_table = ReflectedUserTags(self.engine, self.connection)
            tags = tags_table.get_tags_string(entry.id)
            if tags and tags != "":
                self.print_tags(tags)

        if self.args.social:
            social_table = ReflectedSocialData(self.engine, self.connection)
            social = social_table.get(entry.id)
            if social is not None:
                self.print_social(social)

        if self.args.status:
            print(entry.status_code)

    def print_tags(self, tags):
        print(tags)

    def print_social(self, social):
        if (
            social.view_count is not None
            and social.thumbs_up is not None
            and social.thumbs_down is not None
        ):
            print(
                f"V:{social.view_count} TU:{social.thumbs_up} TD:{social.thumbs_down}"
            )
        else:
            if social.view_count:
                print(f"F:{social.view_count}")

            if social.thumbs_up:
                print(f"F:{social.thumbs_up}")

            if social.thumbs_down:
                print(f"F:{social.thumbs_down}")

            if social.upvote_diff:
                print(f"S:{social.upvote_diff}")

            if social.upvote_ratio:
                print(f"S:{social.upvote_ratio}")

            if social.followers_count:
                print(f"F:{social.followers_count}")

            if social.stars:
                print(f"S:{social.stars}")

    def get_time_diff(self):
        return time.time() - self.start_time

    def handle_row(self, row):
        """
        Row is to be expected a 'dict', eg. row["link"]
        """
        link = row.link

        level = self.args.verbosity

        self.print_entry(row)

        self.total_entries += 1

    def summary(self):
        if self.args.summary:
            if self.args.verify:
                print(
                    "total:{} good:{} dead:{}".format(
                        self.total_entries, self.good_entries, self.dead_entries
                    )
                )
            else:
                print("total:{}".format(self.total_entries))


class DbAnalyzer(object):
    def __init__(self, input_db, args=None):
        self.args = args
        self.result = None
        self.engine = None
        self.input_db = input_db

    def print_summary(self, print_columns=False):
        db = self.input_db

        level = self.args.verbosity
        if level is None or level == 0:
            return

        if not os.path.isfile(db):
            print("File does not exist:{}".format(db))
            return

        self.engine = create_engine("sqlite:///" + db)
        with self.engine.connect() as connection:
            r = ReflectedEntryTable(self.engine, connection)
            r.print_summary(print_columns)

    def search(self):
        if self.is_db_scan():
            file = self.input_db
            if not os.path.isfile(file):
                print("File does not exist:{}".format(file))
                return

            print("Creating engine")
            self.engine = create_engine("sqlite:///" + self.input_db)
            print("Creating engine DONE")

            with self.engine.connect() as connection:
                self.connection = connection

                row_handler = RowHandler(args=self.args, engine=self.engine, connection=self.connection)

                search = None
                if self.args:
                    search = self.args.search

                print("Starting alchemy")
                searcher = AlchemySearch(
                    self.engine,
                    search,
                    row_handler=row_handler,
                    args=self.args,
                    connection=self.connection,
                )
                print("Starting alchemy DONE")

                print("Searching...")
                searcher.search()

    def is_db_scan(self):
        if self.input_db:
            return True

        return False


class Parser(object):

    def parse(self):
        self.parser = argparse.ArgumentParser(description="Data analyzer program")
        self.parser.add_argument("--db", help="DB to be scanned")

        self.parser.add_argument(
            "--search", help="Search, with syntax same as the main program / site."
        )
        self.parser.add_argument(
            "--order-by", default="page_rating_votes", help="order by column."
        )
        self.parser.add_argument("--asc", action="store_true", help="order ascending")
        self.parser.add_argument("--desc", action="store_true", help="order descending")
        self.parser.add_argument("--table", default="linkdatamodel", help="Table name")

        self.parser.add_argument("--title", action="store_true", help="displays title")
        self.parser.add_argument(
            "--description", action="store_true", help="displays description"
        )
        self.parser.add_argument(
            "--status", action="store_true", help="displays status"
        )
        self.parser.add_argument("--tags", action="store_true", help="displays tags")
        self.parser.add_argument(
            "--social", action="store_true", help="displays social data"
        )
        self.parser.add_argument(
            "--date-published", action="store_true", help="displays date-published"
        )
        self.parser.add_argument(
            "--source", action="store_true", help="displays source"
        )

        self.parser.add_argument(
            "--summary", action="store_true", help="displays summary of tables"
        )
        self.parser.add_argument(
            "--columns",
            action="store_true",
            help="displays summary of tables column nmaes",
        )

        self.parser.add_argument(
            "-i", "--ignore-case", action="store_true", help="Ignores case"
        )
        self.parser.add_argument("-v", "--verbosity",  type=int, default = 1, help="Verbosity level")

        self.args = self.parser.parse_args()

        return True


def main():
    p = Parser()
    if not p.parse():
        print("Could not parse options")
        return

    start_time = time.time()

    m = DbAnalyzer(input_db=p.args.db, args=p.args)
    if p.args.summary:
        m.print_summary(p.args.columns)
    else:
        m.search()

    print_time_diff(start_time)


if __name__ == "__main__":
    main()

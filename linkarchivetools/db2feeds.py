"""
Converts Database to information about RSS feeds.

TODO - copy tags from origin to RSS feeds
"""
import shutil
import argparse
from pathlib import Path
from sqlalchemy import create_engine

from webtoolkit import RemoteUrl, BaseUrl
from .utils.reflected import *


class Db2Feeds(object):
    """
    Converter DB -> feeds.
    """
    def __init__(self,input_db=None, verbose = True, remote_server="", output_db=None, output_format=None):
        self.input_db = input_db
        self.verbose = verbose
        self.remote_server = remote_server

        self.output_db = output_file
        self.output_format = output_format

        if self.output_db:
            self.output_format = "SQLITE"
        self.make_output_db()

    def process(self):
        self.engine = create_engine(f"sqlite:///{self.input_db}")
        with self.engine.connect() as connection:
            self.connection = connection
            if self.new_engine:
                with self.new_engine.connect() as new_connection:
                    self.new_connection = new_connection
                    self.read()
            else:
                self.read()

    def make_output_db(self):
        if self.output_format != "SQLITE":
            self.new_engine = None
            self.new_connection = None
            return

        new_path = Path(self.output_db)
        if new_path.exists():
            new_path.unlink()

        shutil.copy(self.input_db, self.output_db)

        self.new_engine = create_engine(f"sqlite:///{self.output_db}")

    def read(self):
        self.truncate_tables()

        table = ReflectedEntryTable(self.engine, self.connection)

        new_table = None
        if self.new_engine:
            new_table = ReflectedTable(self.new_engine, self.new_connection)
            new_table.vacuum()

        for entry in table.get_entries_good():
            if self.remote_server:
                url = RemoteUrl(remote_server=remote_server, url=entry.link)
                feeds = url.get_feeds()
                if len(feeds) == 0:
                    url.get_response()
            else:
                url = BaseUrl(entry.link)

            feeds = url.get_feeds()

            for feed in feeds:
                data = {}
                data["link"] = feed
                data["title"] = entry.title
                data["page_rating_votes"] = entry.page_rating_votes

                # not null requirement
                data["source_url"] = ""
                data["permanent"] = False
                data["bookmarked"] = False
                data["status_code"] = 0
                data["contents_type"] = 0
                data["page_rating_contents"] = 0
                data["page_rating_visits"] = 0
                data["page_rating"] = 0

                self.print_data(data)

                if new_table:
                    self.copy_entry(new_table, data)

    def copy_entry(self, table, data):
        """
        TODO copy from origin table tags
        """
        table.insert_json_data("linkdatamodel", data)

    def truncate_tables(self):
        if not self.new_engine:
            return

        table_names = self.get_table_names()
        for table_name in table_names:
            table = ReflectedTable(self.new_engine, self.new_connection)
            table.truncate_table(table_name)

    def get_table_names(self):
        table_names = [
          "credentials",
          "sourcecategories",
          "sourcesubcategories",
          "sourcedatamodel",
          "userconfig",
          "configurationentry",
          "linkdatamodel",
          "domains",
          "usertags",
          "compactedtags",
          "usercompactedtags",
          "entrycompactedtags",
          "uservotes",
          "browser",
          "entryrules",
          "dataexport",
          "gateway",
          "modelfiles",
          "readlater",
          "searchview",
          "socialdata",
          #"blockentry",
          "blockentrylist",
          "usercomments",
          "userbookmarks",
          "usersearchhistory",
          "userentrytransitionhistory",
          "userentryvisithistory",
        ]
        return table_names

    def print_data(self, data):
        """
        If we print to SQLITE we want to see progress so we display it anyway
        """
        link = data["link"]
        title = data["title"]
        page_rating_votes = data["page_rating_votes"]

        if self.output_format == "LINES" or self.output_format == "SQLITE":
            print(f"[{page_rating_votes}] {link} - {title}")
        elif self.output_format == "JSON":
            print(f'''
            \{ "title" : "{title}",
              "link" : "{link}",
              "page_rating_votes : {page_rating_votes}
            \}''')
        else:
            print("Unsupported output format")


def parse():
    parser = argparse.ArgumentParser(description="Data analyzer program")
    parser.add_argument("--db", default="catalog.db", help="DB to be scanned")
    parser.add_argument("--output-db", help="File to be created")
    parser.add_argument("--output-format", default="LINES", help="format of display. LINES, JSON, SQLITE")
    parser.add_argument("--crawling-server", default="", help="Remote crawling server")
    
    args = parser.parse_args()

    return parser, args


def main():
    parser, args = parse()

    path = Path(args.db)
    if not path.exists():
        print("File {} does not exist".format(path))
        return

    reader = Db2Feeds(input_db = args.db, remote_server=args.crawling_server, output_db=args.output_db, output_format=args.output_format)
    reader.process()


if __name__ == "__main__":
    main()

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

    def __init__(
        self,
        input_db=None,
        verbose=True,
        remote_server="",
        output_db=None,
        output_format=None,
        read_internet_links=False,
        update_rss=False,
    ):
        self.input_db = input_db
        self.verbose = verbose
        self.remote_server = remote_server
        self.update_rss = update_rss
        self.read_internet_links = read_internet_links

        self.output_db = output_db
        self.output_format = output_format

        if self.output_db:
            self.output_format = "SQLITE"
        self.make_output_db()

    def convert(self):
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
            if self.read_internet_links and self.remote_server:
                url = RemoteUrl(remote_server=self.remote_server, url=entry.link)
                feeds = url.get_feeds()
                if len(feeds) == 0:
                    url.get_response()
            else:
                url = BaseUrl(entry.link)

            feeds = url.get_feeds()

            for feed in feeds:
                data = self.prepare_data(entry, feed)

                self.print_data(entry, data)

                if new_table:
                    self.copy_entry(entry, new_table, data)

    def prepare_data(self, entry, feed):
        data = {}
        data["link"] = feed
        data["title"] = entry.title
        data["page_rating_votes"] = entry.page_rating_votes
        data["manual_status_code"] = entry.manual_status_code
        data["thumbnail"] = entry.thumbnail
        data["language"] = entry.language

        # not null requirement
        data["source_url"] = ""
        data["permanent"] = False
        data["bookmarked"] = False
        data["status_code"] = entry.status_code
        data["contents_type"] = 0
        data["page_rating_contents"] = 0
        data["page_rating_visits"] = 0
        data["page_rating"] = 0

        if self.update_rss and self.remote_server:
            url_feed = RemoteUrl(remote_server=self.remote_server, url=feed)
            url_feed.get_response()

            data["title"] = url_feed.get_title()
            data["description"] = url_feed.get_description()
            data["status_code"] = url_feed.get_status_code()
            data["thumbnail"] = url_feed.get_thumbnail()
        return data

    def copy_entry(self, entry, table, data):
        """
        TODO copy from origin table tags
        """
        new_entry_id = table.insert_json_data("linkdatamodel", data)

        source_entry_compacted_tags = ReflectedEntryCompactedTags(self.engine, self.connection)
        tags = source_entry_compacted_tags.get_tags(entry.id)

        entry_tag_data = {}
        for tag in tags:
            entry_tag_data["tag"] = tag
            entry_tag_data["entry_id"] = new_entry_id
            destination_entry_compacted_tags = ReflectedEntryCompactedTags(self.new_engine, self.new_connection)
            destination_entry_compacted_tags.insert_json_data("entrycompactedtags", entry_tag_data)

        source_entry_social_data = ReflectedSocialData(self.engine, self.connection)
        social_data = source_entry_social_data.get_json(entry.id)
        if social_data:
            if "id" in social_data:
                del social_data["id"]
            social_data["entry_id"] = new_entry_id

            destination_entry_social_data = ReflectedSocialData(self.new_engine, self.new_connection)
            destination_entry_social_data.insert_json_data("socialdata", social_data)

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
            # "blockentry",
            "blockentrylist",
            "usercomments",
            "userbookmarks",
            "usersearchhistory",
            "userentrytransitionhistory",
            "userentryvisithistory",
            "user",
        ]
        return table_names

    def print_data(self, entry, data):
        """
        If we print to SQLITE we want to see progress so we display it anyway
        """
        if not self.verbose:
            return

        link = data["link"]
        title = data["title"]
        page_rating_votes = data["page_rating_votes"]

        if self.output_format == "LINES" or self.output_format == "SQLITE":
            print(f"[{page_rating_votes}] {link} - {title}")
            user_tags = ReflectedEntryCompactedTags(self.engine, self.connection)
            tags = user_tags.get_tags_string(entry.id)
            if tags:
                print(f"{tags}")
        elif self.output_format == "JSON":
            user_tags = ReflectedEntryCompactedTags(self.engine, self.connection)
            tags = user_tags.get_tags(entry.id)
            print(
                f"""
            \{ "title" : "{title}",
              "link" : "{link}",
              "page_rating_votes : {page_rating_votes},
              "tags" : {tags}
            \}"""
            )
        else:
            print("Unsupported output format")


def parse():
    parser = argparse.ArgumentParser(description="Data analyzer program")
    parser.add_argument("--db", default="catalog.db", help="DB to be scanned")
    parser.add_argument("--output-db", help="File to be created")
    parser.add_argument("--update-rss",action="store_true", help="Reads RSS to check it's title and properties")
    parser.add_argument("--read-internet-links",action="store_true", help="Reads entries to check if contains RSS. Without it only calculated RSS are returned")
    parser.add_argument(
        "--output-format",
        default="LINES",
        help="format of display. LINES, JSON, SQLITE",
    )
    parser.add_argument("--crawling-server", default="", help="Remote crawling server")

    args = parser.parse_args()

    return parser, args


def main():
    parser, args = parse()

    path = Path(args.db)
    if not path.exists():
        print("File {} does not exist".format(path))
        return

    reader = Db2Feeds(
        input_db=args.db,
        remote_server=args.crawling_server,
        output_db=args.output_db,
        output_format=args.output_format,
    )
    reader.convert()


if __name__ == "__main__":
    main()

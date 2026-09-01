from pathlib import Path
from .sourcedata import SourceData
from .entries import Entries
from .basetable import BaseTable


class Sources(BaseTable):
    SOURCE_TYPE_RSS = "RSS"
    SOURCE_TYPE_PARSE = "Parse"
    SOURCE_TYPE_EMAIL = "Email"

    def __init__(self, connection):
        self.connection = connection
        self.set_table("sources_table")

    def add(self, source_url, source_type=""):
        if self.exists(source_url):
            return

        properties = {}
        properties["url"] = source_url
        properties["source_type"] = source_type

        return self.connection.sources_table.insert_json(properties)

    def set(self, source_url, source_properties=None, source_type=""):
        link = source_url

        title = ""
        language = ""
        favicon = ""

        if source_properties:
            title = source_properties.get("title", "")
            language = source_properties.get("language", "")
            favicon = source_properties.get("thumbnail", "")

        source = self.get_with_url(link)
        if source:
            """
            """
            data = {}

            data["title"] = title
            data["favicon"] = favicon
            data["language"] = language
            data["source_type"] = source_type

            return self.connection.sources_table.update_json_data(source.id, data)

        properties = {}
        properties["url"] = link
        properties["source_type"] = source_type
        properties["title"] = title
        properties["language"] = language
        properties["favicon"] = favicon

        return self.connection.sources_table.insert_json(properties)

    def delete_entries(self, source):
        """
        TODO Remove all entries with source_url = source
        """
        entries = Entries(self.connection)
        entries.delete_where({"source_url" : source.url})

    def delete(self, id):
        source = self.get(id)

        self.delete_entries(source)

        sources_data = SourceData(connection=self.connection)
        sources_data.delete(source)

        self.connection.sources_table.delete(id=id)

    def get(self,id):
        return self.connection.sources_table.get(id=id)

    def get_with_url(self,source_url):
        for source in self.connection.sources_table.get_where({"url":source_url}):
            return source

    def exists(self, source_url):
        link = source_url

        for source in self.connection.sources_table.get_where({"url":link}):
            return True

        return False

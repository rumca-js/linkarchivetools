from pathlib import Path
from .sourcedata import SourceData
from .entries import Entries


class Sources(object):
    def __init__(self, connection):
        self.connection = connection

    def set(self, source_url, source_properties=None):
        link = source_url

        title = ""
        language = ""
        favicon = ""

        if source_properties:
            title = source_properties.get("title", "")
            language = source_properties.get("language", "")
            favicon = source_properties.get("thumbnail", "")

        if not title:
            title = ""
        if not language:
            language = ""
        if not favicon:
            favicon = ""

        source_iter = self.connection.sources_table.get_where({"url":link})
        source = next(source_iter, None)
        if source:
            """
            TODO update source
            """
            data = {}
            data["title"] = title
            data["favicon"] = favicon
            data["language"] = favicon

            return self.connection.sources_table.update_json_data(source.id, data)

        properties = {
               "url": link,
               "enabled" : True,
               "source_type" : "",
               "title" : title,
               "category_name": "",
               "subcategory_name": "",
               "export_to_cms": False,
               "remove_after_days": 5,
               "language": language,
               "age": 0,
               "fetch_period": 3600,
               "auto_tag": "",
               "entries_backgroundcolor_alpha": 1.0,
               "entries_backgroundcolor": "",
               "entries_alpha": 1.0,
               "proxy_location": "",
               "auto_update_favicon":False,
               "xpath": "",
               "favicon": favicon,
       }

        return self.connection.sources_table.insert_json(properties)

    def count(self):
        return self.connection.sources_table.count()

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
        sources_data.remove(source)

        self.remove_static_files(source)

        self.connection.sources_table.delete(id=id)

    def get(self,id):
        return self.connection.sources_table.get(id=id)

    def exists(self, source_url):
        link = source_url

        source_iter = self.connection.sources_table.get_where({"url":link})
        source = next(source_iter, None)
        if source:
            return True

        return False

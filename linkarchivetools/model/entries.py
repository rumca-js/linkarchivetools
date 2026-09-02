from datetime import datetime
from webtoolkit import BaseUrl

from .socialdata import SocialData
from .basetable import BaseTable


class Entries(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("entries_table")

    def add(self, entry_json, source=None):
        if self.connection.entries_table.exists(link=entry_json["link"]):
            return

        if source:
            entry_json["source_url"] = source.url
            entry_json["source_id"] = source.id

        if "source" in entry_json:
            del entry_json["source"]
        if "feed_entry" in entry_json:
            del entry_json["feed_entry"]
        if "link_canonical" in entry_json:
            del entry_json["link_canonical"]
        if "tags" in entry_json:
            del entry_json["tags"]

        entry_json["date_created"] = datetime.now()

        try:
            entry_id = self.connection.entries_table.insert_json(entry_json=entry_json)
            return entry_id
        except Exception as E:
            print(E)
            print(entry_json)
            raise

    def update_all(self):
        for entry in self.get_table().get_where():
            self.update(entry)

    def update(self, entry, url_obj=None):
        if url_obj is None:
            url_obj = BaseUrl(url = entry.link)

        url_obj.get_response()

        url_properties = url_obj.get_properties()
        if url_properties:
            properties = {}
            properties["title"] = url_properties["title"]
            properties["description"] = url_properties["description"]
            properties["language"] = url_properties["language"]
            properties["author"] = url_properties["author"]
            properties["album"] = url_properties["album"]
            properties["date_published"] = url_properties["date_published"]
            properties["date_update_last"] = datetime.now()

            response = url_obj.get_response()
            if response:
                properties["status_code"] = response.get_status_code()
                properties["contents_hash"] = url_obj.get_hash()
                properties["body_hash"] = url_obj.get_body_hash()
                properties["meta_hash"] = url_obj.get_meta_hash()
            self.update_properties(entry, properties)

    def update_properties(self, entry, properties):
        try:
            self.connection.entries_table.update_json_data(id=entry.id, json_data=properties)
            return True
        except Exception as E:
            print(E)
            print(properties)
            raise

    def delete(self, id):
        socialdata = SocialData(self.connection)
        socialdata.delete(entry_id = id)
        self.connection.entries_table.delete(id=id)

    def get(self,id):
        return self.connection.entries_table.get(id=id)

    def exists(self,link=None):
        return self.connection.entries_table.exists(link=link)

    def delete_where(self, conditions):
        entries = self.connection.entries_table.get_where(conditions)
        for entry in entries:
            socialdata = SocialData(self.connection)
            socialdata.delete(entry_id = entry.id)

        self.connection.entries_table.delete_where(conditions)

    def cleanup(self):
        ids_to_remove = set()
        for entry in self.connection.entries_table.get_where():
            if entry.source_id is not None:
                if not self.connection.sources_table.get(id=entry.source_id):
                    ids_to_remove.add(entry.id)

        for id in ids_to_remove:
            self.connection.entries_table.delete(id=id)


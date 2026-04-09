from datetime import datetime
from .socialdata import SocialData


class Entries(object):
    def __init__(self, connection):
        self.connection = connection

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
            entry_id = self.connection.entries_table.insert_json(entry_json)
            return entry_id
        except Exception as E:
            print(E)
            print(entry_json)
            raise

    def count(self):
        return self.connection.entries_table.count()

    def delete(self, id):
        socialdata = SocialData(self.connection)
        socialdata.delete(entry_id = id)
        self.connection.entries_table.delete(id=id)

    def get(self,id):
        return self.connection.entries_table.get(id=id)

    def exists(self,link=None):
        return self.connection.entries_table.exists(link=link)

    def cleanup(self):
        ids_to_remove = set()
        for entry in self.connection.entries_table.get_where():
            if entry.source_id is not None:
                if not self.connection.sources_table.get(id=entry.source_id):
                    ids_to_remove.add(entry.id)

        for id in ids_to_remove:
            self.connection.entries_table.delete(id=id)

    def delete_where(self, conditions):
        entries = self.connection.entries_table.get_where(conditions)
        for entry in entries:
            socialdata = SocialData(self.connection)
            socialdata.delete(entry_id = entry.id)

        self.connection.entries_table.delete_where(conditions)

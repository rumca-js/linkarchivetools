from .basetable import BaseTable
from .entries import Entries


class CheckLater(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("readlater")

    def get(self, entry_id):
        for row in self.get_table().get_where({"entry_id" : entry_id}):
            tags = row.tag
            if tags and tags.endswith(","):
                tags = tags[:-1]
            return tags

        return ""

    def get_all_entry_ids(self):
        result = []
        for row in self.get_table().get_where({}):
            result.append(row.entry_id)

        return result

    def check_later(self, entry):
        rows = self.get_table().get_where({"entry_id" : entry.id})
        for row in rows:
            if row:
                return

        json_data = {}
        json_data["entry_id"] = entry.id
        json_data["user_id"] = None

        return self.get_table().insert_json_data(json_data)

    def not_check_later(self, entry):
        rows = self.get_table().get_where({"entry_id" : entry.id})
        for row in rows:
            if row:
                self.get_table().delete(id=row.id)

    def get_entries(self):
        result = []
        entries = Entries(connection=self.connection)

        entry_ids = self.get_all_entry_ids()
        for entry_id in entry_ids:
            entry = entries.get(entry_id)
            result.append(entry)

        return result

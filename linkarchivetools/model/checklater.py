from .basetable import BaseTable
from .entries import Entries


class CheckLater(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("readlater")

    def get(self, entry_id):
        for row in self.get_table().get_where({"entry_id" : entry_id}):
            return row

    def get_all_entry_ids(self):
        result = []
        for row in self.get_table().get_where({}):
            result.append(row.entry_id)

        return result

    def is_checked(self, entry):
        rows = self.get_table().get_where({"entry_id" : entry.id})
        for row in rows:
            if row:
                return True

        return False

    def check_later(self, entry):
        rows = self.get_table().get_where({"entry_id" : entry.id})
        for row in rows:
            if row:
                return

        json_data = {}
        json_data["entry_id"] = entry.id
        json_data["user_id"] = None

        id = self.get_table().insert_json_data(json_data)
        if id is None:
            return False

        return True

    def not_check_later(self, entry):
        rows = self.get_table().get_where({"entry_id" : entry.id})
        for row in rows:
            if row:
                self.get_table().delete(id=row.id)
                return True
        return False

    def get_entries(self):
        result = []
        entries = Entries(connection=self.connection)

        entry_ids = self.get_all_entry_ids()
        for entry_id in entry_ids:
            entry = entries.get(entry_id)
            result.append(entry)

        return result

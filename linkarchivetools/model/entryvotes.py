from .serializers import entry_to_json

from .basetable import BaseTable


class EntryVotes(object):
    def __init__(self, connection):
        self.connection = connection

    def get(self, entry_id):
        for row in self.connection.entries_table.get_where({"id" : entry_id}):
            return row.page_rating_votes

    def set(self, entry_id, vote):
        entry_json = {}
        entry_json["page_rating_votes"] = vote

        return self.connection.entries_table.update_json_data(id=entry_id, json_data=entry_json)

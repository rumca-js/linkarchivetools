
class EntryTags(object):
    def __init__(self, connection):
        self.connection = connection

    def get(self, entry_id):
        for row in self.connection.entrycompactedtags.get_where({"entry_id" : entry_id}):
            tags = row.tag
            if tags and tags.endswith(","):
                tags = tags[:-1]
            return tags

        return ""

    def get_map(self, entry_id):
        tags = self.get(entry_id=entry_id)
        if tags:
            return tags.split(",")

    def set(self, entry_id, tags):
        if tags and not tags.endswith(","):
            tags = tags + ","

        json_data = {}
        json_data["tag"] = tags
        json_data["entry_id"] = entry_id

        updated = False
        compacted_tags = self.connection.entrycompactedtags.get_where({"entry_id" : entry_id})
        for compacted_tag in compacted_tags:
            if updated:
                self.connection.entrycompactedtags.delete(compacted_tag.id)
            else:
                self.connection.entrycompactedtags.update_json_data(compacted_tag.id, json_data)
            updated = True

        if not updated:
            self.connection.entrycompactedtags.insert_json_data(json_data)

    def cleanup(self):
        compacted_tags = self.connection.entrycompactedtags.get_where({})
        for compacted_tag in compacted_tags:
            if self.connection.entries_table.get(compacted_tag.entry_id) is None:
                self.connection.entrycompactedtags.delete(compacted_tag.id)

from .basetable import BaseTable

class EntryTagsService(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("entrycompactedtags")

    def get(self, entry_id):
        """
        Return tag string
        """
        for row in self.get_table().get_where({"entry_id" : entry_id}):
            tags = row.tag
            if tags and tags.endswith(","):
                tags = tags[:-1]
            return tags

        return ""

    def get_map(self, entry_id):
        tags = self.get(entry_id=entry_id)
        if tags:
            result = []
            split = tags.split(",")
            for tag in split:
                result.append(tag.strip())

            return result

    def set(self, entry_id, tags):
        """
        Tags is string
        """
        if tags and not tags.endswith(","):
            tags = tags + ","

        json_data = {}
        json_data["tag"] = tags
        json_data["entry_id"] = entry_id

        table = self.get_table()

        updated = False
        compacted_tags = table.get_where({"entry_id" : entry_id})
        for compacted_tag in compacted_tags:
            if updated:
                table.delete(compacted_tag.id)
            else:
                table.update_json_data(compacted_tag.id, json_data)
            updated = True

        if not updated:
            table.insert_json_data(json_data)

    def cleanup(self):
        table = self.get_table()
        compacted_tags = table.get_where({})
        for compacted_tag in compacted_tags:
            if self.connection.entries_table.get(compacted_tag.entry_id) is None:
                table.delete(compacted_tag.id)

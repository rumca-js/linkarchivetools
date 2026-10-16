from .basetable import BaseTable


class BlockEntryService(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("blockentry")
        self.table = self.get_reflected_table("blockentry")

    def is_blocked(self, domain_only_url):
        return self.get_entry(domain_only_url)

    def get_entry(self, domain_only_url):
        blocks = self.table.get_where({"url" : domain_only_url})
        for block in blocks:
            return block

    def add(self, url):
        if not self.get_entry(url):
            json_data = {}
            json_data["url"] = url
            return self.table.insert_json_data(json_data = json_data)

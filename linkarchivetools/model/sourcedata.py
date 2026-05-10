import json
from pathlib import Path
from datetime import datetime, timedelta
from .basetable import BaseTable


class SourceData(BaseTable):
    def __init__(self, connection, default_fetch_period_s=3600):
        self.connection = connection
        self.set_table("sourceoperationaldata")
        self.default_fetch_period_s = default_fetch_period_s

    def get_source_data(self, source):
        op_datas = self.connection.sourceoperationaldata.get_where({"source_obj_id" : source.id})
        for op_data in op_datas:
            return op_data

    def mark_read(self, source, url = None):
        op_data = self.get_source_data(source)

        new_data = {}
        new_data["date_fetched"] = datetime.now()
        new_data["source_obj_id"] = source.id

        # TODO fill correctly
        new_data["consecutive_errors"] = 0
        new_data["import_seconds"] = 0
        new_data["number_of_entries"] = 0

        if url:
            new_data["page_hash"] = url.get_hash()
            new_data["body_hash"] = url.get_body_hash()

        try:
            if op_data:
                return self.connection.sourceoperationaldata.update_json_data(id=op_data.id, json_data=new_data)
            else:
                return self.connection.sourceoperationaldata.insert_json_data(json_data=new_data)
        except Exception as E:
            E_str = str(E)
            print(f"Error for data {new_data} {E_str}")

    def is_update_needed(self, source):
        this_source_data = self.get_source_data(source)
        if this_source_data:
            date_fetched = this_source_data.date_fetched

            fetch_period_s = self.default_fetch_period_s
            if source.fetch_period > 0:
                fetch_period_s = source.fetch_period

            if datetime.now() - date_fetched < timedelta(seconds=fetch_period_s):
                return False

        return True

    def get_update_seconds(self, source):
        this_source_data = self.get_source_data(source)
        if this_source_data:
            date_fetched = this_source_data.date_fetched
            diff = datetime.now() - date_fetched
            return diff.total_seconds()

        return 0

    def delete(self, source):
        self.connection.sourceoperationaldata.delete_where({"source_obj_id" : source.id})

    def cleanup(self):
        ids_to_remove = []
        op_datas = self.connection.sourceoperationaldata.get_where()
        for op_data in op_datas:
            source = self.connection.sources_table.get(op_data.source_obj_id)
            if not source:
                ids_to_remove.append(op_data.id)

        for id in ids_to_remove:
            self.connection.sourceoperationaldata.delete(op_data.id)

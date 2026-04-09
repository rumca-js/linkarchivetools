import json
from pathlib import Path
from datetime import datetime, timedelta


class SocialData(object):
    def __init__(self, connection):
        self.connection = connection

    def get(self, entry_id):
        social_datas = self.connection.socialdata.get_where({"entry_id" : entry_id})
        for social_data in social_datas:
            return social_data

    def add(self, entry_id, social_data):
        existing_social_data = self.get(entry_id)

        if existing_social_data:
            social_data["id"] = existing_social_data.id

        social_data["entry_id"] = entry_id
        social_data["date_updated"] = datetime.now()

        valid = self.is_valid(social_data)
        if not valid:
            return

        if existing_social_data:
            self.connection.socialdata.update_json_data(id=existing_social_data.id, json_data=social_data)
        else:
            self.connection.socialdata.insert_json_data(json_data=social_data)

    def is_valid(self, social_data_json):
        valid = False
        for key, value in social_data_json.items():
            if key is not None and value is not None:
                valid = True
        return valid

    def delete(self, entry_id):
        self.connection.socialdata.delete_where({"entry_id" : entry_id})

    def cleanup(self):
        social_data_container = self.connection.socialdata.get_where({})
        # TODO  cannot import entries
        #for social_data in social_data_container:
        #    entry = Entries.get(id=social_data.entry_id)
        #    if not entry:
        #        self.connection.socialdata.delete(id=social_data.id)

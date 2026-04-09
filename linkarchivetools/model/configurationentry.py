
class ConfigurationEntry(object):
    def __init__(self, connection):
        self.connection = connection

    def get(self):
        return self.connection.configurationentry.get()

    def reset(self):
        config_entry = self.get()

        update_data = {}
        #update_data["enable_social_data"] = True
        update_data["new_entries_fetch_social_data"] = True
        update_data["entry_update_fetches_social_data"] = True

        self.connection.configurationentry.update_json_data(id=config_entry.id, json_data=update_data)

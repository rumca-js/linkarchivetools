
class ConfigurationEntry(object):
    def __init__(self, connection):
        self.connection = connection

    def get(self):
        return self.connection.configurationentry.get()

    def truncate(self):
        self.connection.entry_rules.truncate()

    def count(self):
        return self.connection.entries_table.count()

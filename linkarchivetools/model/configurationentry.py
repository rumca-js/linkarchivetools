
class ConfigurationEntry(object):
    CONFIGURATION_NEWS = "News"
    CONFIGURATION_GALLERY = "Gallery"
    CONFIGURATION_SEARCH_ENGINE = "Search Engine"

    def __init__(self, connection):
        self.connection = connection

    def get(self):
        return self.connection.configurationentry.get()

    def truncate(self):
        self.connection.configurationentry.truncate()

    def count(self):
        return self.connection.configurationentry.count()

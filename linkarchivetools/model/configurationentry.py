
class ConfigurationEntry(object):
    DISPLAY_STYLE_LIGHT = "style-light"
    DISPLAY_STYLE_DARK = "style-dark"

    ACCESS_TYPE_ALL = "access-type-all"
    ACCESS_TYPE_LOGGED = "access-type-logged"
    ACCESS_TYPE_OWNER = "access-type-owner"
    ACCESS_TYPE_STAFF = "access-type-staff"

    DISPLAY_TYPE_STANDARD = "standard"
    DISPLAY_TYPE_GALLERY = "gallery"
    DISPLAY_TYPE_SEARCH_ENGINE = "search-engine"
    DISPLAY_TYPE_CONTENT_CENTRIC = "content-centric"
    DISPLAY_TYPE_ACCORDION = "accordion"
    DISPLAY_TYPE_LINKS_ONLY = "links-only"

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

    def update(self, json_data):
        config_entry = self.get()
        return self.connection.configurationentry.update_json_data(id=config_entry.id, json_data=json_data)

from .basetable import BaseTable

class ConfigurationEntryService(BaseTable):
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
    DISPLAY_TYPE_COMPACT = "compact"

    CONFIGURATION_NEWS = "News"
    CONFIGURATION_GALLERY = "Gallery"
    CONFIGURATION_SEARCH_ENGINE = "Search Engine"

    def __init__(self, connection):
        self.connection = connection
        self.set_table("configurationentry")

    def get(self):
        table = self.get_table()
        for row in table.get_where():
            return row

        json_data = {}
        table.insert_json_data(json_data)

        for row in table.get_where():
            return row

    def truncate(self):
        self.get_table().truncate()

    def count(self):
        return self.get_table().count()

    def update(self, json_data):
        config_entry = self.get()
        return self.get_table().update_json_data(id=config_entry.id, json_data=json_data)


# Module-level definitions for DISPLAY_STYLE, ACCESS_TYPE, DISPLAY_TYPE, and CONFIGURATION presets
DISPLAY_STYLE_LIGHT = ConfigurationEntryService.DISPLAY_STYLE_LIGHT
DISPLAY_STYLE_DARK = ConfigurationEntryService.DISPLAY_STYLE_DARK

ACCESS_TYPE_ALL = ConfigurationEntryService.ACCESS_TYPE_ALL
ACCESS_TYPE_LOGGED = ConfigurationEntryService.ACCESS_TYPE_LOGGED
ACCESS_TYPE_OWNER = ConfigurationEntryService.ACCESS_TYPE_OWNER
ACCESS_TYPE_STAFF = ConfigurationEntryService.ACCESS_TYPE_STAFF

DISPLAY_TYPE_STANDARD = ConfigurationEntryService.DISPLAY_TYPE_STANDARD
DISPLAY_TYPE_GALLERY = ConfigurationEntryService.DISPLAY_TYPE_GALLERY
DISPLAY_TYPE_SEARCH_ENGINE = ConfigurationEntryService.DISPLAY_TYPE_SEARCH_ENGINE
DISPLAY_TYPE_CONTENT_CENTRIC = ConfigurationEntryService.DISPLAY_TYPE_CONTENT_CENTRIC
DISPLAY_TYPE_ACCORDION = ConfigurationEntryService.DISPLAY_TYPE_ACCORDION
DISPLAY_TYPE_LINKS_ONLY = ConfigurationEntryService.DISPLAY_TYPE_LINKS_ONLY
DISPLAY_TYPE_COMPACT = ConfigurationEntryService.DISPLAY_TYPE_COMPACT

CONFIGURATION_NEWS = ConfigurationEntryService.CONFIGURATION_NEWS
CONFIGURATION_GALLERY = ConfigurationEntryService.CONFIGURATION_GALLERY
CONFIGURATION_SEARCH_ENGINE = ConfigurationEntryService.CONFIGURATION_SEARCH_ENGINE


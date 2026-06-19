def get_tables():
    tables = [
        "apikeys",                      # table containing API keys for server, access
        "applogging",                   # logger table
        "backgroundjob",                # jobs queue
        "backgroundjobhistory",         # jobs queue history
        "keywords",                     # keywords parsed from incoming links, entries, etc.
        "credentials",                  # credentials used by the system for access
        "sourcecategories",             # source categories
        "sourcesubcategories",          # sources subcategories
        "sourcedatamodel",              # source data model (sources)
        "sourceoperationaldata",        # operational data for source. When was last time fetched. etc.
        "configurationentry",           # main configuration entry record
        "linkdatamodel",                # entries
        "domains",                      # domains
        "compactedtags",                # tags compacted, to easily obtain how many tags we have
        "entrycompactedtags",           # tags compacted for entry
        "browser",                      # browsers configured for the system
        "entryrules",                   # entry rules
        "dataexport",                   # data export
        "gateway",                      # gateway
        "modelfiles",                   # model files, stored files
        "searchview",                   # entry search views (to filter bookmarks etc)
        "socialdata",                   # entry social data
        "blockentry",                   # block entry row
        "blockentrylist",               # block entry list, contains block entry rows

        "readlater",                    # user read later entries
        "userconfig",                   # configuration of the user
        "usertags",                     # tags added by the user
        "usercompactedtags",            # tags added by the user (compacted for user, with ',' delim)
        "uservotes",                    # user votes
        "usercomments",                 # user comments
        "userbookmarks",                # user bookmarks
        "usersearchhistory",            # user search history
        "userentrytransitionhistory",   # user transition history
        "userentryvisithistory",        # user entry visit history
    ]
    return tables


def get_backup_tables():
    """
    Not all tables need to be backupped
    """
    tables = [
        "apikeys",
        #"applogging",
        #"backgroundjob",
        #"backgroundjobhistory",
        #"keywords",
        "credentials",
        "sourcecategories",
        "sourcesubcategories",
        "sourcedatamodel",
        #"sourceoperationaldata",
        "configurationentry",
        "linkdatamodel",
        "domains",
        "compactedtags",
        "entrycompactedtags",
        "browser",
        "entryrules",
        "dataexport",
        "gateway",
        "modelfiles",
        "searchview",
        "socialdata",
        # "blockentry", # do not backup it, the list has to be reinitialized each time
        "blockentrylist",

        "readlater",
        "userconfig",
        "usertags",
        "usercompactedtags",
        "uservotes",
        "usercomments",
        "userbookmarks",
        "usersearchhistory",
        "userentrytransitionhistory",
        "userentryvisithistory",
    ]
    return tables


def get_truncate_tables():
    """
    When producing for public
    """
    tables = [
        "apikeys",
        "applogging",
        "backgroundjob",
        "backgroundjobhistory",
        "keywords",
        "credentials",
        "sourcecategories",
        "sourcesubcategories",
        "sourcedatamodel",
        "sourceoperationaldata",
        #"configurationentry",
        #"linkdatamodel",
        "domains",
        #"compactedtags",
        #"entrycompactedtags",
        "browser",
        "entryrules",
        "dataexport",
        "gateway",
        "modelfiles",
        #"searchview",
        #"socialdata",
        "blockentry",
        "blockentrylist",

        "user",
        "readlater",
        "userconfig",
        "usertags",
        "usercompactedtags",
        "uservotes",
        "usercomments",
        "userbookmarks",
        "usersearchhistory",
        "userentrytransitionhistory",
        "userentryvisithistory",
    ]
    return tables

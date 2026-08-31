# Link Database Tools

Package provides tools that allow to filter databases produced by https://github.com/rumca-js/Django-link-archive.

Can filter or analyze entries from https://github.com/rumca-js/Internet-Places-Database.

# Tools

 - DbAnalyzer - provides analysis of the DB contents
 - DbUpdate - modifies database. Can create missing tables, truncate tables.
 - Db2Feeds - converts database to DB of feeds
 - Db2JSON - converts database to JSON
 - JSON2Db - Converts JSON into datbase
 - DbMerge - Merges database with other databse
 - backup.sh - create backup of Postgres tables

# DbAnalyzer

```
usage: dbanalyzer.py [-h] [--db DB] [--search SEARCH] [--order-by ORDER_BY] [--asc] [--desc]
                     [--table TABLE] [--title] [--votes] [--description] [--status] [--tags]
                     [--social] [--date-published] [--source] [--summary] [--columns] [--rss]
                     [--channel] [--json] [-i] [-v VERBOSITY]

Data analyzer program

options:
  -h, --help            show this help message and exit
  --db DB               DB to be scanned
  --search SEARCH       Search, with syntax same as the main program / site.
  --order-by ORDER_BY   order by column.
  --asc                 order ascending
  --desc                order descending
  --table TABLE         Table name
  --title               displays title
  --votes               displays votes
  --description         displays description
  --status              displays status
  --tags                displays tags
  --social              displays social data
  --date-published      displays date-published
  --source              displays source
  --summary             displays summary of tables
  --columns             displays summary of tables column names
  --rss                 displays RSS sources
  --channel             displays channels
  --json                JSON format
  -i, --ignore-case     Ignores case
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```

# DbUpdate

```
usage: dbupdate.py [-h] [--db DB] [--create-tables] [--truncate-tables TRUNCATE_TABLES]
                   [--trunc-dynamic-data] [--trunc-configuration] [--trunc-search-data]
                   [--trunc-visits-data] [--delete-non-bookmarked] [--delete-no-votes]
                   [--delete-redundant] [--no-users] [--obfuscate] [-v VERBOSITY]

DB manipulation program

options:
  -h, --help            show this help message and exit
  --db DB               DB to be filtered
  --create-tables       Creates tables. Even missing ones
  --truncate-tables TRUNCATE_TABLES
                        Truncate table(s). Pass table names
  --trunc-dynamic-data  Truncates dynamic tables
  --trunc-configuration
                        Removes uneceesary configuration
  --trunc-search-data   Removes all search data
  --trunc-visits-data   Removes all visit data
  --delete-non-bookmarked
                        Removes non bookmarked
  --delete-no-votes     Removes entries without a vote
  --delete-redundant    Removes entries that are redundant - not bookmarked, no votes
  --no-users            Prepares for setup with no users
  --obfuscate           Obfuscates private data
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level

```

# Db2Feeds

```
usage: db2feeds.py [-h] [--db DB] [--output-db OUTPUT_DB] [--update-rss] [--clean]
                   [--read-internet-links] [--output-format OUTPUT_FORMAT]
                   [--crawling-server CRAWLING_SERVER]

Data analyzer program

options:
  -h, --help            show this help message and exit
  --db DB               DB to be scanned
  --output-db OUTPUT_DB
                        File to be created
  --update-rss          Reads RSS to check it's title and properties
  --clean               If output db exists, then it is removed at start
  --read-internet-links
                        Reads entries to check if contains RSS. Without it only calculated RSS are
                        returned
  --output-format OUTPUT_FORMAT
                        format of display. LINES, JSON, SQLITE
  --crawling-server CRAWLING_SERVER
                        Remote crawling server
```

# Db2JSON

```
usage: db2json.py [-h] [--db DB] [--output-dir OUTPUT_DIR] [--rows-max] [-f FORMAT] [-v VERBOSITY]

Data analyzer program

options:
  -h, --help            show this help message and exit
  --db DB               DB to be scanned
  --output-dir OUTPUT_DIR
                        Output directory
  --rows-max            Number of rows per file
  -f FORMAT, --format FORMAT
                        file name format
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```


# DbMerge

```
usage: dbmerge.py [-h] [--input-dbs INPUT_DBS] [--output OUTPUT]

Data analyzer program

options:
  -h, --help            show this help message and exit
  --input-dbs INPUT_DBS
                        DBs to be scanned. Delim ,
  --output OUTPUT       DB to be produced
```

# Utils

Reflected tools - provides access table definitions.
Model - model data. Classes that allow you to modify, read tables

# Installation

pip install linkarchivetools

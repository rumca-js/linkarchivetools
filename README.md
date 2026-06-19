# Link Database Tools

Package provides tools that allow to filter databases produced by https://github.com/rumca-js/Django-link-archive.

Can filter or analyze entries from https://github.com/rumca-js/Internet-Places-Database.

# Tools

 - DbAnalyzer - provides analysis of the DB contents
 - Db2Feeds - converts database to DB of feeds
 - Db2JSON - converts database to JSON
 - DbFilter - filters database (only bookmarks? only votes?)
 - DbMerge - Merges database with other databse
 - JSON2Db - Converts JSON into datbase
 - Backup - makes backup of postgres tables

# DbAnalyzer

```
usage: dbanalyzer.py [-h] [--db DB] [--search SEARCH] [--order-by ORDER_BY] [--asc] [--desc]
                     [--table TABLE] [--title] [--description] [--status] [--tags] [--social]
                     [--date-published] [--source] [--summary] [--columns] [--rss] [--channels]
                     [--json] [-i] [-v VERBOSITY]

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
  --description         displays description
  --status              displays status
  --tags                displays tags
  --social              displays social data
  --date-published      displays date-published
  --source              displays source
  --summary             displays summary of tables
  --columns             displays summary of tables column names
  --rss                 displays RSS sources
  --channels            displays channels
  --json                JSON format
  -i, --ignore-case     Ignores case
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

# DbFilter

```
usage: dbfilter.py [-h] [--db DB] [--output-db OUTPUT_DB] [--bookmarked] [--votes] [--truncate]
                   [-v VERBOSITY]

Data analyzer program

options:
  -h, --help            show this help message and exit
  --db DB               DB to be scanned
  --output-db OUTPUT_DB
                        DB to be created
  --bookmarked          export bookmarks
  --votes               export if votes is > 0
  --truncate            Truncates tables for public
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

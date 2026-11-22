# CLI Interfaces and Endpoints

## Architecture

linkarchivetools does not expose hosted HTTP REST or RPC server endpoints. All user interactions occur through CLI commands or direct Python module imports.

## CLI Commands

### dbanalyzer
- Source: [dbanalyzer.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/dbanalyzer.py)
- CLI invocation: `poetry run python -m linkarchivetools.dbanalyzer [options]`
- Options:
  - `--db`: path to SQLite database file
  - `--search`: search expression using query grammar
  - `--order-by`: column name to sort results by
  - `--asc`: sort in ascending order
  - `--desc`: sort in descending order
  - `--table`: target table name (default: linkdatamodel)
  - `--title`: display entry titles
  - `--votes`: display entry votes
  - `--description`: display entry descriptions
  - `--status`: display HTTP response status codes
  - `--tags`: display entry tags
  - `--social`: display social metrics
  - `--date-published`: display publication dates
  - `--source`: display source identifiers
  - `--summary`: print summary of table names and row counts
  - `--columns`: print table columns
  - `--rss`: print detected RSS source URLs
  - `--channel`: print channel names
  - `--json`: format output as JSON
  - `-i, --ignore-case`: ignore case in search terms
  - `-v, --verbosity`: verbosity level

### dbupdate
- Source: [dbupdate.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/dbupdate.py)
- CLI invocation: `poetry run python -m linkarchivetools.dbupdate [options]`
- Options:
  - `--db`: path to SQLite database file
  - `--create-tables`: create missing tables defined in schema
  - `--truncate-tables`: comma-delimited list of table names to truncate
  - `--trunc-dynamic-data`: truncate dynamic runtime tables
  - `--trunc-configuration`: truncate configuration tables
  - `--trunc-search-data`: truncate search history tables
  - `--trunc-visits-data`: truncate visit and transition tables
  - `--delete-non-bookmarked`: delete links that are not bookmarked
  - `--delete-no-votes`: delete links without votes
  - `--delete-redundant`: delete unvoted and unbookmarked entries
  - `--no-users`: strip user records and personal tables
  - `--obfuscate`: obfuscate sensitive and private data
  - `-v, --verbosity`: verbosity level

### db2feeds
- Source: [db2feeds.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/db2feeds.py)
- CLI invocation: `poetry run python -m linkarchivetools.db2feeds [options]`
- Options:
  - `--db`: input database to scan
  - `--output-db`: output database file path for generated feeds
  - `--update-rss`: fetch RSS endpoints to inspect feed titles and metadata
  - `--clean`: remove output database before processing if it exists
  - `--read-internet-links`: verify links over HTTP to detect RSS endpoints
  - `--output-format`: output format (LINES, JSON, SQLITE)
  - `--crawling-server`: remote crawling service address

### dbmerge
- Source: [dbmerge.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/dbmerge.py)
- CLI invocation: `poetry run python -m linkarchivetools.dbmerge [options]`
- Options:
  - `--input-dbs`: comma-delimited list of SQLite database files
  - `--output`: target merged SQLite database path

### db2json
- Source: [db2json.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/db2json.py)
- CLI invocation: `poetry run python -m linkarchivetools.db2json [options]`
- Options:
  - `--db`: path to database file
  - `--output-dir`: destination directory for exported JSON files
  - `--rows-max`: maximum number of rows per output JSON file
  - `-f, --format`: output file name pattern
  - `-v, --verbosity`: verbosity level

### json2db
- Source: [json2db.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/json2db.py)
- CLI invocation: `poetry run python -m linkarchivetools.json2db [options]`
- Options:
  - `--input-file`: single JSON file to import
  - `--input-dir`: directory of JSON files to import
  - `--output-db`: destination SQLite database path
  - `--preserve-id`: preserve original row primary key IDs
  - `--vote-min`: minimum vote threshold for imported entries
  - `--verbose`: verbose output

### backup
- Source: [backup.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/backup.py)
- CLI invocation: `poetry run python -m linkarchivetools.backup [options]`
- Options:
  - `--backup`: execute backup from PostgreSQL instance
  - `--restore`: restore database from backup files
  - `--vacuum`: run VACUUM against PostgreSQL tables
  - `--analyze`: run ANALYZE against PostgreSQL tables
  - `--reindex`: run REINDEX against PostgreSQL tables
  - `--export-type`: backup type (custom or sqlite)
  - `--database`: PostgreSQL database name
  - `--user`: PostgreSQL user
  - `--host`: PostgreSQL host

## External URL Contracts

- Remote Crawling Server: optional HTTP crawler client used by db2feeds
- Web Toolkit Integration: URL canonicalization via webtoolkit (BaseUrl, UrlLocation, PageResponseObject)
- RSS Feed URLs: remote XML feed URLs fetched and validated via requests

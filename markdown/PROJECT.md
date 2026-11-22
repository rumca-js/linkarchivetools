# Project Specification

Provides classes and functions for link management programs.

## Tech Stack

- Language: Python 3.10+
- Build system: Poetry (poetry-core)
- Core dependencies:
  - sqlalchemy (2.0 declarative mappings and reflection)
  - psycopg2-binary (PostgreSQL dialect driver)
  - webtoolkit (BaseUrl, UrlLocation, PageResponseObject utilities)
  - sympy (expression parsing helper)
  - python-dateutil (timestamp formatting and manipulation)
  - requests (crawling and remote feed verification)
- Development dependencies:
  - black (code formatting)
  - unittest (test suite execution)

## Repository Layout

- linkarchivetools/ - core package
  - model/ - SQLAlchemy declarative models and table controllers
    - definitions.py - declarative database schema mapping
    - basetable.py - base controller class for table interactions
    - dbconnection.py - engine, connection, and session lifecycle manager
    - serializers.py - JSON and RSS channel/atom XML serialization
    - entries.py - link data query and persistence controller
    - sources.py - source repository controller
    - applogging.py - system log event controller
    - backgroundjobs.py - asynchronous task queue controller
    - configurationentry.py - system configuration record controller
    - entryrules.py - rule matching and tagging controller
    - entrytags.py - tag compaction and association controllers
    - entryvisits.py - transition and visit tracking controller
    - entryvotes.py - user rating and vote controller
    - searchview.py - search view filter controller
    - socialdata.py - external social metadata controller
    - sourcedata.py - source metadata controller
    - checklater.py - read-later queue controller
    - blocklist.py - domain and link blocklist controller
    - userconfig.py - user account configuration controller
  - utils/ - query engines and reflection utilities
    - alchemysearch.py - structured query builder translating ASTs to SQLAlchemy filters
    - omnisearch.py - grammar and AST token parser for search syntax
    - reflected.py - dynamic table reflection, bulk copying, and schema generation
  - tableconfig.py - grouping definitions for backup, personal, dynamic, and configuration tables
  - backup.py - PostgreSQL dump, restore, analyze, vacuum, and reindex manager
  - db2feeds.py - RSS extraction and feed database generator
  - db2json.py - SQLite table exporter to chunked JSON records
  - dbanalyzer.py - CLI analysis, inspection, and multi-field search engine
  - dbmerge.py - entry deduplication and multi-database merger
  - dbupdate.py - table creation, truncation, user stripping, and privacy obfuscation
  - json2db.py - JSON record importer into SQLite databases
- tests/ - unittest test suite
- markdown/ - project reference documentation and active work tracking

## Command Reference

- Run full test suite:
```bash
poetry run python -u -m unittest discover -v
```

- Code formatting:
```bash
poetry run black linkarchivetools
```

- Build distribution wheel and tarball:
```bash
poetry build
```

- Analyze database contents:
```bash
poetry run python -m linkarchivetools.dbanalyzer --db path/to/archive.db --summary
```

- Filter and clean database:
```bash
poetry run python -m linkarchivetools.dbupdate --db path/to/archive.db --create-tables
```

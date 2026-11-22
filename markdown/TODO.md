# Project Backlog and Architectural TODOs

## Architectural Refactoring

- Provide entry to JSON and JSON to entry. there might be different needs: only entry information, entry with tags, entry with social data.

- verify if definitions.py is missing fields, or if any is redundant

- perform code analysis of each conversion classes

- Consolidate business logic:
  - Resolve division between linkarchivetools/model/ controllers and linkarchivetools/utils/reflected.py
  - Refactored model operations should utilize consistent declarative mappings rather than mixed reflection

- Modernize database session management:
  - Replace DBConnection wrapper (which combines raw engine and connection instances) with standard SQLAlchemy session factory pattern

- CLI entrypoint consolidation:
  - Migrate root-level wrapper scripts (backup.py, db2feeds.py, db2json.py, dbanalyzer.py, dbmerge.py, dbupdate.py, json2db.py) to pyproject.toml CLI console_scripts

- Table grouping unification:
  - Reconcile table categories in tableconfig.py to align backup sets, dynamic sets, and truncation routines

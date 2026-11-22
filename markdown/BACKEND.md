# Backend Architecture

## Overview

The backend layer comprises database connections, model controllers, dynamic table reflection, query compilers, and serialization utilities.

## Core Modules

### Connection Management
- Location: [dbconnection.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/dbconnection.py)
- Class: DBConnection
- Responsibilities: creates SQLAlchemy engines, manages connection instances, and builds sessionmaker instances for SQLite and PostgreSQL databases.

### Table Classification Policies
- Location: [tableconfig.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/tableconfig.py)
- Responsibilities: categorizes tables into functional groups:
  - all tables: complete schema table set
  - backup tables: tables eligible for backup operations
  - dynamic tables: runtime operational tables eligible for clearing (applogging, backgroundjob, keywords)
  - user tables: user-owned data (user, userbookmarks, usertags, uservotes)
  - configuration tables: system and browser configuration records
  - truncate tables: predefined sets for headless or public distribution cleanups

### Model Controllers (linkarchivetools/model/)
- BaseTable in [basetable.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/basetable.py): base controller providing session lifecycle and CRUD primitives
- EntriesController in [entries.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/entries.py): query, insert, and update operations on linkdatamodel
- SourcesController in [sources.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/sources.py): source registry and crawl status management
- BackgroundJobsController in [backgroundjobs.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/backgroundjobs.py): job scheduling, status transitions, and error tracking
- ConfigurationEntryController in [configurationentry.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/configurationentry.py): global runtime parameter storage
- EntryRulesController in [entryrules.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/entryrules.py): pattern evaluation and rule automation
- Tag Controllers in [entrytags.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/entrytags.py): compacted tag dictionaries and relational tag mappings
- EntryVisitsController in [entryvisits.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/entryvisits.py): visit metrics and referrer transition logging
- EntryVotesController in [entryvotes.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/entryvotes.py): aggregate and individual vote management
- SearchView in [searchview.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/searchview.py): dynamic filter views and query persistence
- SocialData in [socialdata.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/socialdata.py): external platform metrics and raw response storage
- SourceData in [sourcedata.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/sourcedata.py): source operational records and fetch histories
- ReadLater in [checklater.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/checklater.py): user reading list state
- BlockList in [blocklist.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/blocklist.py): domain and URL exclusion filtering
- UserConfig in [userconfig.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/userconfig.py): user preferences key-value store
- AppLogging in [applogging.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/applogging.py): database-backed system log writer
- Serializers in [serializers.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/model/serializers.py): RSS 2.0 XML templates, Atom item formatting, and JSON encoders

### Query Engine (linkarchivetools/utils/)
- Omnisearch in [omnisearch.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/utils/omnisearch.py): recursive descent parser tokenizing search grammar into query AST nodes
- AlchemySearch in [alchemysearch.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/utils/alchemysearch.py): translates Omnisearch AST nodes into SQLAlchemy binary expressions and filter clauses

### Reflection and Bulk Operations (linkarchivetools/utils/)
- ReflectedTable in [reflected.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/utils/reflected.py): inspects arbitrary database tables via SQLAlchemy metadata reflection
- ReflectedEntryTable in [reflected.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/utils/reflected.py): handles schema migrations, table creation, and bulk record insertions
- EntryCopier in [reflected.py](file:///home/hunter/WorkDir/git/linkarchivetools/linkarchivetools/utils/reflected.py): streaming cross-database record copier with deduplication

# PROJECT

This project provide link archive tools.

This project uses:
 - webtoolkit dependency for BaseUrl, UrlLocation, PageResponseObject, and other classes

Project:
 - Provides database scheme for link storage
 - Provides scripts that can be used to modify databases: search, update, etc.

Scripts:
 - db2json.py - used to convert SQLite to JSON
 - json2db.py - used to convert JSON to SQLite
 - dbanalyzer.py - used to search database
 - dbupdate.py - used to truncate table, or change values
 - db2feeds.py - converts database of links to database of feeds
 - backupy.py - performs backup from postgres table

# Table scheme
 - model/definitions.py - provide table definitions
 - tableconfig.py - provides table names with their meaning

# Business logic
Tried to implement some business logic in model/ directory, but I don't like it

# Notes
 - this project uses dbconnection that contains engine and connection (I don't like it). I think projects use sessions
 - backup performs from table where instance preceeds table name. It uses django approach, so it does look like a 'custom' script
 - functionality is scattered between scripts. maybe consolidation is needed?
 - I don't like that part of things are using utils/reflected.py and some are in model/ directory

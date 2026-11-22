# Known Bugs and Issues

## Test Suite Regressions

### ConfigurationEntry Controller CompileError
- File: tests/test_model_configurationentry.py
- Method: test_insert_json
- Symptom: CompileError raised by SQLAlchemy during insert execution
- Root cause: unconsumed column names in insert statement parameters:
  - log_remove_entries
  - entry_update_via_internet
- Status: open

### DbUpdate Truncation Assertions Failure
- File: tests/test_dbupdate.py
- Methods:
  - test_truncate_configuration_tables
  - test_truncate_dynamic_data
  - test_truncate_user_tables
- Symptom: AssertionError: 0 not greater than 0 on input_compactedtags_count check
- Root cause: test fixture initialization does not populate compactedtags prior to executing truncation assertions
- Status: open

## Runtime Warnings

### Missing SQLite Tables in db2feeds
- Module: linkarchivetools/db2feeds.py
- Symptom: SQLite table does not exist logged for:
  - usercomments
  - usercompactedtags
  - sourcesubcategories
  - sourcecategories
- Impact: non-fatal warning during feed generation on minimal databases
- Status: open

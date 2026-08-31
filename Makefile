.PHONY: test build publish config reformat example summary

test:
	poetry run python -u -m unittest discover -v 2>&1 | tee test_output.txt

build:
	poetry build

publish:
	poetry publish

config:
	poetry config pypi-token.pypi your-token-here

reformat:
	poetry run black linkarchivetools

example:
	poetry run python3 -m linkarchivetools.dbanalyzer --db linkarchivetools/internet.db --search "*warhammer*" --title

summary:
	@echo \# DbAnalyzer
	@echo '```'
	@poetry run python dbanalyzer.py --help
	@echo '```'
	@echo \# DbUpdate
	@echo '```'
	@poetry run python dbupdate.py --help
	@echo '```'
	@echo \# Db2Feeds
	@echo '```'
	@poetry run python db2feeds.py --help
	@echo '```'
	@echo \# DbMerge
	@echo '```'
	@poetry run python dbmerge.py --help
	@echo '```'
	@echo \# Db2JSON
	@echo '```'
	@@poetry run python db2json.py --help
	@echo '```'
	@echo \# JSON2Db
	@echo '```'
	@poetry run python json2db.py --help
	@echo '```'

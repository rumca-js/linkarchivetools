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

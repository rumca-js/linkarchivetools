#rm test.db

#poetry run python dbupdate.py --create-tables --db test.db
#poetry run python dbanalyzer.py --summary --db test.db

#poetry run python dbupdate.py --db test.db --insert-source-url "https://www.youtube.com/feeds/videos.xml?channel_id=UC0Wju2yvRlfwqraLlz5152Q"
#poetry run python dbupdate.py --db test.db --insert-link "https://google.com"
#poetry run python dbanalyzer.py --summary --db test.db

#poetry run python dbupdate.py --db test.db --update-entries
#poetry run python dbupdate.py --db test.db --update-sources

#poetry run python dbanalyzer.py --db test.db --search "*" --title --tags --social --status --description

poetry run python dbupdate.py --db test.db --process-sources
poetry run python dbanalyzer.py --db test.db --print-sources

#poetry run python dbanalyzer.py --summary --db test.db
#poetry run python dbanalyzer.py --db test.db --search "*" --title --tags --social --status --description

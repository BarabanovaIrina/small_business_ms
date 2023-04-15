.DEFAULT_GOAL := run

install:
	pip install -r requirements.txt

pre-commit-check:
	pre-commit run --all-files

run-tests:
	coverage run --source "warehouse" warehouse/manage.py test warehouse
	coverage xml -o warehouse/coverage.xml
	coverage run --source "sales" sales/manage.py test sales
	coverage xml -o sale/coverage.xml
	coverage run --source "accounting" accounting/manage.py test accounting
	coverage xml -o accounting/coverage.xml

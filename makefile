.DEFAULT_GOAL := run

install:
	pip install -r requirements.txt

pre-commit-check:
	pre-commit run --all-files

run-wh-tests:
	python warehouse/manage.py test warehouse

run-sales-tests:
	python sales/manage.py test sales

test-coverage:
	pytest --cov=rates --cov-report xml

.DEFAULT_GOAL := run

install:
	pip install -r requirements.txt

pre-commit-check:
	pre-commit run --all-files

run-tests:
	python warehouse/manage.py test warehouse

test-coverage:
	pytest --cov=rates --cov-report xml

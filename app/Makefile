.PHONY: help deps migrate test lint

help:
		@echo Makefile Commands
		@echo make test							Runs Django Tests


deps:
		pip install --upgrade pip && pip install -r requirements.txt


migrate:
		python manage.py makemigrations && python manage.py migrate

lint:
		flake8 . && pylint .


test:
		python manage.py test

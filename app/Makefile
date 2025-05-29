.PHONY: help deps migrate test

help:
		@echo Makefile Commands
		@echo make test							Runs Django Tests


deps:
		pip install --upgrade pip && pip install -r requirements.txt


migrate:
		python manage.py makemigrations && python manage.py migrate


test:
		python manage.py test


SAMPLE_SECRET := https://raw.githubusercontent.com/googleapis/google-auth-library-python-oauthlib/master/tests/unit/data/client_secrets.json

BASE_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
VERSION := $(shell python scripts/version.py)

venv:
	@if [ ! -d "./venv" ]; then python3 -m venv venv; fi
	@echo "Use following commands:"
	@echo
	@echo "To activate   - . venv/bin/activate"
	@echo "To deactivate - deactivate"
	@echo

version:
	@echo "Current version:   $(VERSION)"
	@echo "Current branch:    $(BRANCH)"


clean-build:
	@rm -rf ./build/ ./dist/ ./django_google_mailer.egg-info

clean-app:
	@rm -rf db.sqlite3
	@find ./gmailer \( \
		-name "__pycache__" -o \
		-name ".DS_Store" -o \
		-name "Thumb.db" \)  -exec rm -rf {} +

clean-venv:
	@rm -rf ./venv

clean-test:
	@rm -rf ./tox

clean-docs:
	@cd docs && make clean >/dev/null 2>&1 || rm -rf _build/doctrees _build/html

setup:
	@pip install -U pip wheel setuptools
	@pip install -r requirements.txt
	@curl -o google_client_secret.json $(SAMPLE_SECRET)
	@echo
	@echo "Save your app credentials from following link in to 'google_client_secret.json'"
	@echo
	@echo "====> https://console.cloud.google.com/apis/credentials"
	@echo

test: version
	@python manage.py test

upgrade:
	@-pip uninstall -yr requirements.txt
	@pip uninstall -y wheel setuptools
	@pip install -Ur requirements/development.txt
	@pip freeze > requirements.txt
	@pip install -U pip wheel setuptools

update: clean-docs
	@m2r2 --overwrite CHANGELOG.md
	@mv -f CHANGELOG.rst ./docs/change.rst

html: update
	@cd docs && make html
	@echo
	@echo "Location of docs:"
	@echo "====> file://$(BASE_DIR)docs/_build/html/index.html"

build: clean-build update
	@python3 setup.py sdist bdist_wheel

test-release: test build
ifeq ($(BRANCH), develop)
	@twine upload --repository testpypi dist/* --config-file .pypirc
else
	@echo
	@echo "You can only release latest version from develop branch"
	@echo
endif

release: test build
ifeq ($(BRANCH), main)
	@twine upload dist/* --config-file .pypirc
else
	@echo
	@echo "You can only release stable version from main branch"
	@echo
endif

run:
	@python manage.py makemigrations
	@python manage.py migrate
	@echo
	@echo "Use following urls for testing:"
	@echo
	@echo "====> http://localhost:8000/gmailer/auth"
	@echo "====> http://localhost:8000/gmailer/test_send_mail"
	@echo "====> http://localhost:8000/gmailer/revoke"
	@echo
	@python manage.py runserver 0.0.0.0:8000

clean: clean-build clean-app clean-venv clean-docs

.PHONY: setup build release venv clean html update version

venv:
	@if [ ! -d "./venv" ]; then python3 -m venv venv; fi
	@echo "Use following commands:"
	@echo
	@echo "To activate   - . venv/bin/activate"
	@echo "To deactivate - deactivate"
	@echo

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

clean-docs:
	@cd docs && make clean >/dev/null 2>&1 || rm -rf _build/doctrees _build/html

setup:
	@pip install -U pip wheel setuptools
	@pip install -r requirements.txt

upgrade:
	@pip install -Ur requirements/development.txt
	@pip freeze > requirements.txt

update-docs: clean-docs
	@m2r2 --overwrite CHANGELOG.md
	@mv -f CHANGELOG.rst ./docs/change.rst

html-docs: update-docs
	@cd docs && make html

build: clean-build
	@python3 setup.py sdist bdist_wheel

test-release:
	@twine upload --repository testpypi dist/* --config-file .pypirc

release:
	@twine upload dist/* --config-file .pypirc

run:
	@python manage.py makemigrations
	@python manage.py migrate
	@python manage.py runserver 0.0.0.0:8000

clean: clean-build clean-app clean-venv clean-docs

.PHONY: setup build release venv clean

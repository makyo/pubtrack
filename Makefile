VENV=venv

$(VENV):
	virtualenv $(VENV) --python=`which python3`

.PHONY: deps
deps: $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	cd tracker/media/app && npm install

.PHONY: run
run: $(VENV)/bin/django-admin tracker/media/app/node_modules/.bin/browserify
	cd tracker && ../$(VENV)/bin/python manage.py runserver

.PHONY: migrate
migrate: $(VENV)/bin/django-admin tracker/media/app/node_modules/.bin/browserify
	cd tracker && ../$(VENV)/bin/python manage.py migrate

.PHONY: migrations
migrations: $(VENV)/bin/django-admin tracker/media/app/node_modules/.bin/browserify
	cd tracker && ../$(VENV)/bin/python manage.py makemigrations

.PHONY: lint
lint: $(VENV)/bin/django-admin tracker/media/app/node_modules/.bin/browserify
	flake8

.PHONY: test
test: $(VENV)/bin/django-admin tracker/media/app/node_modules/.bin/browserify
	cd tracker && ../$(VENV)/bin/python manage.py test

.PHONY: check
check: lint test

.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf tracker/media/node_modules
	find . -name '*.py[co]' -exec rm {} \;

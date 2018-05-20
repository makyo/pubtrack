VENV=venv

$(VENV):
	virtualenv $(VENV) --python=`which python3`

$(VENV)/bin/django-admin: $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

tracker/media/app/node_modules:
	cd tracker/media/app && npm install

.PHONY: deps
deps: $(VENV)/bin/django-admin tracker/media/app/node_modules

.PHONY: run
run: deps
	cd tracker && ../$(VENV)/bin/python manage.py runserver

.PHONY: migrate
migrate: deps
	cd tracker && ../$(VENV)/bin/python manage.py migrate

.PHONY: migrations
migrations: deps
	cd tracker && ../$(VENV)/bin/python manage.py makemigrations

.PHONY: lint
lint: deps
	flake8

.PHONY: test
test: deps
	cd tracker && ../$(VENV)/bin/python manage.py test

.PHONY: check
check: lint test

.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf tracker/media/app/node_modules
	find . -name '*.py[co]' -exec rm {} \;

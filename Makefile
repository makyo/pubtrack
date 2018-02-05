VENV=venv

$(VENV):
	virtualenv $(VENV) --python=`which python3`
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: lint
lint: $(VENV)
	flake8

.PHONY: test
test: $(VENV)
	cd tracker && ../$(VENV)/bin/python manage.py test

.PHONY: check
check: lint test

.PHONY: clean
clean:
	rm -rf $(VENV)

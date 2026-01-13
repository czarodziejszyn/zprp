#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = zprp
PYTHON_VERSION = 3.13.7
PYTHON_INTERPRETER = python
BACKEND_DIR = backend
GEOCODING_DIR = geocoding
SCRAPER_DIR = scraper

VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements: create_environment
	# $(PYTHON_INTERPRETER) -m pip install -U pip
	# $(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(VENV_PIP) install -U pip
	$(VENV_PIP) install -r requirements.txt
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 .
	isort --check --diff .
	black --check .

## Format source code with black
.PHONY: format
format:
	isort .
	black .



## Run unit tests
.PHONY: unit_tests backend_tests scraper_tests geocoding_tests
unit_tests: backend_tests scraper_tests geocoding_tests




## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	# @bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	# @echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	@test -d $(VENV) || $(PYTHON_INTERPRETER) -m venv $(VENV)



.PHONY: setup
setup: create_environment requirements
	@echo "Environment ready."



#################################################################################
# BACKEND RULES                                                                 #
#################################################################################
.PHONY: backend stop_backend update_api_cache backend_tests benchmark backend_benchmark

## Start backend and import data
backend:
	$(MAKE) -C $(BACKEND_DIR) backend

## Stop backend
stop_backend:
	$(MAKE) -C $(BACKEND_DIR) stop_backend

## Update API cache
update_api_cache:
	$(MAKE) -C $(BACKEND_DIR) update_api_cache

backend_tests:
	$(MAKE) -C $(BACKEND_DIR) backend_tests


backend_benchmark: backend
	@echo ">>> Waiting for API to be fully ready..."
	@python -c "import time; time.sleep(5)"
	$(MAKE) -C $(BACKEND_DIR) benchmark
	@echo ">>> Closing API..."
	$(MAKE) -C $(BACKEND_DIR) stop_backend

#################################################################################
# OFFERS CACHE RULES                                                            #
#################################################################################
.PHONY: update_offers_cache scraper_tests geocoding_tests

## Update offers cache (scrap offers, then geocode them)
update_offers_cache:
	$(MAKE) -C $(SCRAPER_DIR) scrape
	$(MAKE) -C $(GEOCODING_DIR) geocode

scraper_tests:
	$(MAKE) -C $(SCRAPER_DIR) scraper_tests

geocoding_tests:
	$(MAKE) -C $(GEOCODING_DIR) geocoding_tests

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = zprp
PYTHON_VERSION = 3.13.7
PYTHON_INTERPRETER = python
BACKEND_DIR = backend
FRONTEND_DIR = frontend
GEOCODING_DIR = geocoding
SCRAPER_DIR = scraper

VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip
BIN = $(VENV)/bin

# Frontend (Dash) settings
FRONTEND_HOST ?= 127.0.0.1
FRONTEND_PORT ?= 8050
FRONTEND_BASE_URL ?= http://$(FRONTEND_HOST):$(FRONTEND_PORT)

# Frontend backend URL (real backend by default; tests override to mock)
FRONTEND_BACKEND_BASE_URL ?= http://localhost:8000

# Frontend e2e mock backend
MOCK_BACKEND_HOST ?= 127.0.0.1
MOCK_BACKEND_PORT ?= 8001
MOCK_BACKEND_BASE_URL := http://$(MOCK_BACKEND_HOST):$(MOCK_BACKEND_PORT)

# Frontend venv + stamps
FRONTEND_VENV_DIR ?= $(FRONTEND_DIR)/.venv
FRONTEND_VENV_PY := $(FRONTEND_VENV_DIR)/bin/python
FRONTEND_DEPS_STAMP := $(FRONTEND_VENV_DIR)/.deps_installed
FRONTEND_PW_STAMP := $(FRONTEND_VENV_DIR)/.playwright_installed
FRONTEND_DEV_STAMP := $(FRONTEND_VENV_DIR)/.dev_installed
FRONTEND_PID_FILE := $(FRONTEND_DIR)/.dash_pid
FRONTEND_MOCK_PID_FILE := $(FRONTEND_DIR)/.mock_backend_pid

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
# .PHONY: lint
# lint:
# 	flake8 .
# 	isort --check --diff .
# 	black --check .

## Lint code (flake8, isort, black)
.PHONY: lint
lint:
	$(BIN)/flake8 .
	$(BIN)/isort --check --diff .
	$(BIN)/black --check .


## Format source code with black
# .PHONY: format
# format:
# 	isort .
# 	black .

## Format code (isort + black)
.PHONY: format
format:
	$(BIN)/isort .
	$(BIN)/black .




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


.PHONY: run run_frontend

## Run full application (backend + frontend)
run:
	@echo ">>> Starting backend..."
	$(MAKE) backend
	@echo ">>> Starting frontend..."
	$(VENV_PYTHON) frontend/app.py

#################################################################################
# FRONTEND RULES                                                                #
#################################################################################
.PHONY: frontend_setup frontend_run frontend_test frontend_format frontend_linter

frontend_setup:
	@$(MAKE) -s $(FRONTEND_DEPS_STAMP) $(FRONTEND_PW_STAMP) $(FRONTEND_DEV_STAMP)

frontend_run:
	@$(MAKE) -s $(FRONTEND_DEPS_STAMP) $(FRONTEND_PW_STAMP)
	-@fuser -k $(FRONTEND_PORT)/tcp 2>/dev/null || true
	@BACKEND_BASE_URL=$(FRONTEND_BACKEND_BASE_URL) $(FRONTEND_VENV_PY) $(FRONTEND_DIR)/app.py

frontend_test:
	@$(MAKE) -s $(FRONTEND_DEPS_STAMP) $(FRONTEND_PW_STAMP)
	-@fuser -k $(FRONTEND_PORT)/tcp 2>/dev/null || true
	@nohup $(FRONTEND_VENV_PY) -m $(FRONTEND_DIR).tests.e2e.mock_backend --host $(MOCK_BACKEND_HOST) --port $(MOCK_BACKEND_PORT) >/dev/null 2>&1 & echo $$! > $(FRONTEND_MOCK_PID_FILE)
	@sleep 0.4
	@BACKEND_BASE_URL=$(MOCK_BACKEND_BASE_URL) nohup $(FRONTEND_VENV_PY) $(FRONTEND_DIR)/app.py >/dev/null 2>&1 & echo $$! > $(FRONTEND_PID_FILE)
	@sleep 2
	@FRONTEND_BASE_URL=$(FRONTEND_BASE_URL) BACKEND_BASE_URL=$(MOCK_BACKEND_BASE_URL) $(FRONTEND_VENV_PY) -m pytest -q $(FRONTEND_DIR)/tests/e2e || STATUS=$$?; \
	PID=$$(cat $(FRONTEND_PID_FILE) 2>/dev/null || echo ""); \
	test -n "$$PID" && kill $$PID 2>/dev/null || true; \
	MPID=$$(cat $(FRONTEND_MOCK_PID_FILE) 2>/dev/null || echo ""); \
	test -n "$$MPID" && kill $$MPID 2>/dev/null || true; \
	rm -f $(FRONTEND_PID_FILE) $(FRONTEND_MOCK_PID_FILE); \
	exit $$STATUS

frontend_format:
	@$(MAKE) -s $(FRONTEND_DEV_STAMP)
	@$(FRONTEND_VENV_PY) -m isort $(FRONTEND_DIR)
	@$(FRONTEND_VENV_PY) -m black $(FRONTEND_DIR)

frontend_linter:
	@$(MAKE) -s $(FRONTEND_DEV_STAMP)
	@$(FRONTEND_VENV_PY) -m flake8 $(FRONTEND_DIR)

$(FRONTEND_DEPS_STAMP): $(FRONTEND_DIR)/requirements.txt
	@test -d $(FRONTEND_VENV_DIR) || python3 -m venv $(FRONTEND_VENV_DIR)
	@$(FRONTEND_VENV_PY) -m pip install -r $(FRONTEND_DIR)/requirements.txt
	@$(FRONTEND_VENV_PY) -m pip install -q pytest pytest-playwright
	@touch $(FRONTEND_DEPS_STAMP)

$(FRONTEND_PW_STAMP):
	@test -d $(FRONTEND_VENV_DIR) || python3 -m venv $(FRONTEND_VENV_DIR)
	@$(FRONTEND_VENV_PY) -m playwright install --with-deps
	@touch $(FRONTEND_PW_STAMP)

$(FRONTEND_DEV_STAMP):
	@test -d $(FRONTEND_VENV_DIR) || python3 -m venv $(FRONTEND_VENV_DIR)
	@$(FRONTEND_VENV_PY) -m pip install -q black isort flake8
	@touch $(FRONTEND_DEV_STAMP)



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

## Run tests with coverage
.PHONY: coverage
coverage:
	$(BIN)/pytest \
		--cov=zprp \
		--cov-report=term-missing \
		--cov-report=xml \
		--cov-report=html


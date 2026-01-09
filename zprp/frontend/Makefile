PY ?= python3
VENV_DIR ?= .venv
VENV_PY := $(VENV_DIR)/bin/python
FRONTEND_HOST ?= 127.0.0.1
FRONTEND_PORT ?= 8050
FRONTEND_BASE_URL ?= http://$(FRONTEND_HOST):$(FRONTEND_PORT)
PID_FILE ?= .dash_pid
DEPS_STAMP := $(VENV_DIR)/.deps_installed
PW_STAMP := $(VENV_DIR)/.playwright_installed

.PHONY: run test

$(DEPS_STAMP): requirements.txt
	@test -d $(VENV_DIR) || $(PY) -m venv $(VENV_DIR)
	@$(VENV_PY) -m pip install -r requirements.txt
	@$(VENV_PY) -m pip install -q pytest pytest-playwright
	@touch $(DEPS_STAMP)

$(PW_STAMP):
	@test -d $(VENV_DIR) || $(PY) -m venv $(VENV_DIR)
	@$(VENV_PY) -m playwright install --with-deps
	@touch $(PW_STAMP)

run:
	@$(MAKE) -s $(DEPS_STAMP) $(PW_STAMP)
	-@fuser -k $(FRONTEND_PORT)/tcp 2>/dev/null || true
	@$(VENV_PY) app.py

test:
	@$(MAKE) -s $(DEPS_STAMP) $(PW_STAMP)
	-@fuser -k $(FRONTEND_PORT)/tcp 2>/dev/null || true
	@nohup $(VENV_PY) app.py >/dev/null 2>&1 & echo $$! > $(PID_FILE)
	@sleep 2
	@FRONTEND_BASE_URL=$(FRONTEND_BASE_URL) $(VENV_PY) -m pytest -q tests/e2e || STATUS=$$?; \
	PID=$$(cat $(PID_FILE) 2>/dev/null || echo ""); \
	test -n "$$PID" && kill $$PID 2>/dev/null || true; \
	rm -f $(PID_FILE); \
	exit $$STATUS



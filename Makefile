# Makefile for FastMCP Python project

.PHONY: install run lint test clean

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) simple_mcp_server.py

lint: install
	$(PIP) install --upgrade flake8
	$(VENV)/bin/flake8 simple_mcp_server.py

test: install
	@echo "No tests defined yet. Add test targets as needed."

clean:
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -rf {} +

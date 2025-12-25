# Makefile for FastMCP Python project

include .env

.PHONY: install run lint format-imports test clean

VENV=.venv
PYTHON=$(VENV)/bin/python
MCP=$(VENV)/bin/mcp
PIP=$(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -q -r requirements.txt

run: install
	$(MCP) run server.py

run_client: install
	$(PYTHON) client_connecting_with_llm.py
	
inspector: install
	npx --yes @modelcontextprotocol/inspector

lint: install
	$(VENV)/bin/flake8 simple_mcp_server.py

format-imports: install
	$(VENV)/bin/isort . --profile black

test: install
	@echo "No tests defined yet. Add test targets as needed."

clean:
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -rf {} +

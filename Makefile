PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install test lint format check help

help:
	@echo "LearnLog development commands"
	@echo "  make install  Install the package in editable mode with dev extras"
	@echo "  make test     Run the test suite"
	@echo "  make lint     Lint with Ruff"
	@echo "  make format   Format with Ruff"
	@echo "  make check    Run lint and tests"

install:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests
	$(PYTHON) -m ruff check --fix src tests

check: lint test

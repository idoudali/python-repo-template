# Single entry point for humans, agents, and CI: `make verify`.

.PHONY: help install fmt lint types test verify

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install: ## Sync all dependency groups with uv
	uv sync --all-groups

fmt: ## Auto-fix lint and format
	uv run ruff check --fix .
	uv run ruff format .

lint: ## Check lint and format (no writes)
	uv run ruff check .
	uv run ruff format --check .

types: ## Run mypy strict
	uv run mypy

test: ## Run the test suite (wired in the tests PR)
	@echo "pytest is not configured yet"; exit 1

verify: lint types ## Lint and types (tests join verify in the next PR)

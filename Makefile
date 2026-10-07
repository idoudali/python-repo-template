# Single entry point for humans, agents, and CI: `make verify`.

.PHONY: help install fmt lint typos types test docs docs-serve verify

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

typos: ## Spell-check with typos
	uvx typos

types: ## Run mypy strict
	uv run mypy

test: ## Run the test suite with coverage gate
	uv run pytest -q

docs: ## Build the MkDocs site (strict)
	DISABLE_MKDOCS_2_WARNING=true uv run mkdocs build --strict

docs-serve: ## Serve the docs locally
	DISABLE_MKDOCS_2_WARNING=true uv run mkdocs serve

verify: lint typos types test ## Lint, typos, types, and tests (same order as CI)

---
name: python-lint
description: Lint and format Python with Ruff (prefer Astral plugin), then mypy/pytest. Use after Python edits, before commit or PR, or when the user mentions lint, format, ruff, mypy, or style failures.
---

# Python lint and checks

Prefer OpenAI's Astral Claude plugin when it is installed:

```text
/astral:ruff
```

Install once if needed:

```text
/plugin marketplace add astral-sh/claude-code-plugins
/plugin install astral@astral-sh
```

Offline / without the plugin, use the project toolchain from `AGENTS.md`:

```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy
uv run pytest
```

Or `make verify` (lint → typos → types → test). On a small change, pass touched paths to Ruff instead of `.`.

## Rules

- Non-zero exit means the task is not finished. Fix the code; do not widen ignores.
- Do not `pip install ruff` into the system Python.
- Do not add blanket `# noqa` or `# type: ignore` without explaining why.
- `uv run pre-commit run --all-files` is an acceptable single entry point when hooks are installed.

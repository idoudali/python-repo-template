---
name: python-style
description: Apply this repo's Google Python style (Ruff, 80 cols, Google docstrings, type hints). Use when writing or reviewing Python, choosing names, formatting, or when the user mentions style, PEP 8, or Google style.
---

# Python style

1. Read `[tool.ruff]` and `[tool.ruff.lint.pydocstyle]` in `pyproject.toml`. That config is the standard.
2. Follow `AGENTS.md` for the human-readable coding standard and verify loop.
3. Write code that already matches it:
   - 4-space indent, 80-column lines, double quotes
   - Google docstrings on public functions
   - Type hints on public signatures
   - No wildcard imports
4. Do not run Black, YAPF, isort, or autopep8 unless `pyproject.toml` already says so.
5. After edits, invoke the `python-lint` skill (or run the commands in `AGENTS.md`).
6. If a requested style conflicts with Ruff, keep Ruff and tell the user.

Reference: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

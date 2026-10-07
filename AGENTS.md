# Agent instructions

This file is the source of truth for humans and coding agents (Cursor, Claude
Code, Codex, Copilot, and similar). Keep it short. Details live in
`pyproject.toml`.

## Environment

- Python version: see `.python-version` and `requires-python` in `pyproject.toml`.
- Create / sync: `uv sync --all-groups`
- Add a dependency: `uv add <pkg>` (runtime) or `uv add --group dev <pkg>`
  (tools). Never edit `uv.lock` by hand. Never `pip install` into the system
  interpreter.
- Install hooks: `uv run pre-commit install` and
  `uv run pre-commit install --hook-type commit-msg`.

## Layout

```text
src/python_repo_template/   # package
tests/                      # pytest
pyproject.toml              # deps and coding standard
Makefile                    # make verify
```

## Coding standard

Follow Google Python Style (4-space indent, 80-column lines, Google docstrings,
`snake_case` functions, `CamelCase` classes, no wildcard imports). The
**enforced** subset is Ruff + mypy in `pyproject.toml`. If Ruff and this file
disagree, Ruff wins — update this file.

Typing:

- Prefer `TypedDict` / `dataclass` / `NamedTuple` / pydantic models over naked
  `dict[str, Any]` for structured data.
- Prefer `Sequence` / `Mapping` ABCs at boundaries when appropriate.
- Avoid `Any` on public APIs.
- Use modern builtins (`list[str]`, `dict[str, int]`, `|` unions).

Public APIs need Google docstrings (`Args:` / `Returns:` / `Raises:` /
`Examples:`). They feed the MkDocs API reference once docs are enabled.

Match this shape:

```python
def add_two(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First addend.
        b: Second addend.

    Returns:
        The sum of the two arguments.
    """
    return a + b
```

Do not reformat files the task did not change.

## Docs

```bash
make docs        # mkdocs build --strict
make docs-serve  # local preview
```

Public APIs need Google docstrings because they feed the MkDocs API reference.

## Lint / type / test

```bash
make verify     # lint + types + tests, same order as CI
```

Or without make:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Auto-fix before asking the user to review:

```bash
uv run ruff check --fix .
uv run ruff format .
```

A change is not done while any of these fail. Fix the code rather than widening
`ignore` or adding `# noqa`.

## Safety

- Do not commit `.venv/`, secrets, or `.claude/settings.local.json`.
- Do not force-push `main`.
- Use conventional commits (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`).

# Development

## Environment

```bash
uv sync --all-groups
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Verify loop

```bash
make verify   # lint + types + tests (same order as CI)
make docs     # MkDocs strict build
```

Agents should follow [`AGENTS.md`](https://github.com/idoudali/python-repo-template/blob/main/AGENTS.md).

## Public APIs and docs

Public functions need Google docstrings. They feed the
[API reference](reference/index.md) via mkdocstrings. New modules under
`src/python_repo_template/` appear automatically; no manual nav edits.

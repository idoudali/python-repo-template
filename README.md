# python-repo-template

[![CI](https://github.com/idoudali/python-repo-template/actions/workflows/ci.yml/badge.svg)](https://github.com/idoudali/python-repo-template/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/idoudali/python-repo-template)](LICENSE)

Template Python package with a Typer CLI. It ships with uv, Ruff, mypy,
pytest (100% branch coverage), pre-commit, agent docs, MkDocs with a generated
API reference, packaging checks, PyInstaller binaries, and a release-please
GitHub Release flow.

## Use this template

1. Click **Use this template** on GitHub (or clone the repo).
2. Rename the project:

   ```bash
   uv run python scripts/rename_project.py my-tool
   uv lock
   ```

3. Sync and verify:

   ```bash
   uv sync --all-groups
   make verify
   ```

## Install from a release

Download a wheel or a platform binary from
[Releases](https://github.com/idoudali/python-repo-template/releases).

```bash
uv pip install python_repo_template-*.whl
python-repo-template --version
```

Or run a binary directly:

```bash
chmod +x python-repo-template-linux-x86_64
./python-repo-template-linux-x86_64 greet Ada
```

## Quick start (from source)

```bash
uv sync --all-groups
uv run python-repo-template --version
uv run python-repo-template greet Ada --count 2
uv run python-repo-template info --json
```

## Development

```bash
make verify   # lint + types + tests
make docs     # MkDocs strict build
make build    # sdist + wheel checks
make binary   # platform-tagged PyInstaller binary
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md), and the
[docs site](https://idoudali.github.io/python-repo-template/) (after Pages is
enabled).

## License

Apache-2.0. See [LICENSE](LICENSE).

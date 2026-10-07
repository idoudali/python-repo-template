# Copilot instructions

Follow [`AGENTS.md`](../AGENTS.md).

- Use `uv` for all Python tooling (`uv sync --all-groups`, `uv run …`).
- Coding standard is Google style, enforced by Ruff + mypy in `pyproject.toml`.
- After Python edits, run `make verify` (or the commands listed in `AGENTS.md`).
- Prefer small, focused changes. Do not reformat unrelated files.
- Use conventional commits.

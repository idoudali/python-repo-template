# Contributing

## Setup

```bash
uv sync --all-groups
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Verify before opening a PR

```bash
make verify
make docs
```

## Commit messages

Use [conventional commits](https://www.conventionalcommits.org/):

- `feat:` for user-facing features (bumps minor while still 0.x)
- `fix:` for bug fixes
- `docs:`, `ci:`, `chore:`, `test:` for non-release noise

## Branch protection (maintainers)

Recommended rules for `main`:

- Require a pull request before merging
- Require the CI workflow to pass. Job ids / names to require:
  `pre-commit`, `test` (matrix: `test (py… / …)`), `audit` (`pip-audit`),
  `docs`, `package` (`package / build package`), `binary` (`binary / binary
  (…)`), `zizmor`
- Do not allow force-pushes
- For release-please, allow GitHub Actions to open PRs, and set
  `RELEASE_PLEASE_TOKEN` so the Release PR triggers required checks (see
  `docs/releasing.md`)

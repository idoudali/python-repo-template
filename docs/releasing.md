# Releasing

Releases are driven by [release-please](https://github.com/googleapis/release-please).

## How a release happens

1. Merge conventional commits to `main` (`feat:`, `fix:`, `feat!:`, …).
2. On every push to `main`, the `release` workflow updates (or opens) a
   **Release PR** with the version bump and `CHANGELOG.md` section.
3. Review and merge the Release PR.
4. release-please creates the git tag (`vX.Y.Z`) and GitHub Release.
5. The same workflow builds the wheel, sdist, and platform binaries, writes
   `SHA256SUMS`, attaches build provenance attestations, and uploads the
   assets to the Release with `gh release upload`.

## Re-publishing assets

release-please only reports a new release on the run that creates the tag, so
re-running a failed release workflow does not rebuild anything. To rebuild
and re-upload the assets of an existing release, run the workflow by hand
with the tag:

```bash
gh workflow run release.yml -f tag=v0.2.0
```

This skips release-please, builds from the tag, and replaces the assets
(`gh release upload --clobber`).

## Bootstrap

`.release-please-manifest.json` starts as `{}`. The first Release PR that
release-please opens will populate the package version entry.

`release-please-config.json` bumps the project version in `uv.lock` via a TOML
jsonpath that uses `.value` on the package name filter
(`$.package[?(@.name.value=='python-repo-template')].version`). If the lock
looks stale after merging a Release PR, run `uv lock` and push a follow-up
commit.

## Required repository settings

- Create a repository secret **`RELEASE_PLEASE_TOKEN`**: a fine-grained PAT or
  GitHub App installation token with permission to open PRs, push to the
  release branch, and write issues/contents as needed by release-please. Do
  **not** rely on the default `GITHUB_TOKEN` for this step — a Release PR
  opened with it does not trigger required CI, so it may be unmergeable on a
  protected `main`. The release workflow requires this secret.
- **Allow GitHub Actions to create and approve pull requests** (Settings →
  Actions → General).
- See also
  [release-flow.md](https://github.com/idoudali/idea-space/blob/main/project-idea/python-repo-template/release-flow.md)
  in idea-space.
- Pages source: GitHub Actions (one-time):

  ```bash
  gh api -X POST repos/idoudali/python-repo-template/pages -f build_type=workflow
  ```

## Local dry run

```bash
make build
make binary
```

Pre-releases are configured in release-please when needed; prefer an
`0.x.0-rc.N` prerelease before the first stable cut.

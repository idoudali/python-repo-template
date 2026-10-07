"""Rename distribution, import package, and console script after cloning."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DIST = "python-repo-template"
DEFAULT_PKG = "python_repo_template"
_SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
_PROTECTED_REF = "idea-space/project-idea/python-repo-template"
_PROTECTED_PLACEHOLDER = "@@IDEA_SPACE_PYTHON_REPO_TEMPLATE@@"
_RENAME_HELPER_TEST = "test_rename_project.py"


def _slug_to_package(slug: str) -> str:
    """Convert a distribution slug to an import package name."""
    return slug.replace("-", "_")


def _apply_replacements(text: str, replacements: list[tuple[str, str]]) -> str:
    """Replace template identifiers while protecting idea-space URLs."""
    protected = text.replace(_PROTECTED_REF, _PROTECTED_PLACEHOLDER)
    updated = protected
    for old, new in replacements:
        updated = updated.replace(old, new)
    return updated.replace(_PROTECTED_PLACEHOLDER, _PROTECTED_REF)


def rename_project(
    *,
    dist_name: str,
    root: Path = ROOT,
    dry_run: bool = False,
) -> list[Path]:
    """Rename the template project identifiers under ``root``.

    Args:
        dist_name: New PyPI / distribution name (kebab-case).
        root: Repository root.
        dry_run: When True, report paths that would change without writing.

    Returns:
        Paths that changed (or would change, when ``dry_run``).

    Raises:
        ValueError: If ``dist_name`` is empty or not a valid slug.
    """
    if not dist_name or not _SLUG.fullmatch(dist_name):
        msg = (
            "dist_name must be lowercase kebab-case starting with a letter, "
            f"got {dist_name!r}"
        )
        raise ValueError(msg)

    pkg_name = _slug_to_package(dist_name)
    replacements = [
        (DEFAULT_DIST, dist_name),
        (DEFAULT_PKG, pkg_name),
    ]

    test_paths = sorted(
        path
        for path in (root / "tests").rglob("*.py")
        if path.name != _RENAME_HELPER_TEST
    )
    targets: list[Path] = [
        root / "pyproject.toml",
        root / "README.md",
        root / "AGENTS.md",
        root / "CLAUDE.md",
        root / "CONTRIBUTING.md",
        root / "Makefile",
        root / "mkdocs.yml",
        root / "CHANGELOG.md",
        root / "release-please-config.json",
        root / ".release-please-manifest.json",
        root / "docs" / "index.md",
        root / "docs" / "getting-started.md",
        root / "docs" / "development.md",
        root / "docs" / "cli.md",
        root / "docs" / "releasing.md",
        root / "docs" / "gen_ref_pages.py",
        root / "packaging" / "pyinstaller" / "python-repo-template.spec",
        root / "scripts" / "build_binary.py",
        root / ".github" / "workflows" / "build.yml",
        root / ".github" / "workflows" / "binary.yml",
        root / ".github" / "copilot-instructions.md",
        *sorted((root / "src" / DEFAULT_PKG).rglob("*.py")),
        *test_paths,
    ]

    changed: list[Path] = []
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        updated = _apply_replacements(text, replacements)
        if updated == text:
            continue
        changed.append(path)
        if not dry_run:
            path.write_text(updated, encoding="utf-8")

    src_old = root / "src" / DEFAULT_PKG
    src_new = root / "src" / pkg_name
    if src_old.is_dir() and src_old != src_new and not dry_run:
        src_old.rename(src_new)
        changed.append(src_new)

    spec_old = root / "packaging" / "pyinstaller" / "python-repo-template.spec"
    spec_new = root / "packaging" / "pyinstaller" / f"{dist_name}.spec"
    if spec_old.is_file() and spec_old != spec_new and not dry_run:
        spec_old.rename(spec_new)
        changed.append(spec_new)

    return changed


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for renaming the template."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dist_name",
        help="New distribution name (kebab-case), for example my-tool",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would change without writing",
    )
    args = parser.parse_args(argv)
    try:
        changed = rename_project(dist_name=args.dist_name, dry_run=args.dry_run)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    action = "Would update" if args.dry_run else "Updated"
    for path in changed:
        print(f"{action}: {path}")
    if not changed:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Tests for the template rename helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

ROOT = Path(__file__).resolve().parents[1]


def _load_rename() -> Callable[..., list[Path]]:
    path = ROOT / "scripts" / "rename_project.py"
    spec = importlib.util.spec_from_file_location("rename_project", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast("Callable[..., list[Path]]", module.rename_project)


rename_project = _load_rename()


def _seed_template(root: Path) -> None:
    (root / "src" / "python_repo_template").mkdir(parents=True)
    (root / "src" / "python_repo_template" / "__init__.py").write_text(
        '"""python_repo_template package."""\n',
        encoding="utf-8",
    )
    (root / "pyproject.toml").write_text(
        'name = "python-repo-template"\n'
        'python-repo-template = "python_repo_template.cli:app"\n',
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        "# python-repo-template\n",
        encoding="utf-8",
    )
    (root / "tests").mkdir()
    (root / "tests" / "test_version.py").write_text(
        "from python_repo_template import __version__\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_rename_project.py").write_text(
        'DEFAULT = "python-repo-template"\nPKG = "python_repo_template"\n',
        encoding="utf-8",
    )


def test_rename_project_rewrites_and_moves(tmp_path: Path) -> None:
    _seed_template(tmp_path)
    changed = rename_project(dist_name="my-tool", root=tmp_path)
    assert (tmp_path / "src" / "my_tool" / "__init__.py").is_file()
    assert not (tmp_path / "src" / "python_repo_template").exists()
    text = (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert "my-tool" in text
    assert "my_tool" in text
    assert "python-repo-template" not in text
    assert changed


def test_rename_project_dry_run_is_noop(tmp_path: Path) -> None:
    _seed_template(tmp_path)
    changed = rename_project(dist_name="my-tool", root=tmp_path, dry_run=True)
    assert changed
    assert (tmp_path / "src" / "python_repo_template").is_dir()
    assert not (tmp_path / "src" / "my_tool").exists()


def test_rename_project_rejects_bad_slug() -> None:
    with pytest.raises(ValueError, match="kebab-case"):
        rename_project(dist_name="My_Tool")


@pytest.mark.parametrize("slug", ["x", "x-cli"])
def test_rename_project_accepts_short_slugs(
    tmp_path: Path,
    slug: str,
) -> None:
    _seed_template(tmp_path)
    changed = rename_project(dist_name=slug, root=tmp_path)
    assert changed
    pkg = slug.replace("-", "_")
    assert (tmp_path / "src" / pkg / "__init__.py").is_file()


def test_rename_project_skips_helper_test_file(tmp_path: Path) -> None:
    _seed_template(tmp_path)
    helper = tmp_path / "tests" / "test_rename_project.py"
    before = helper.read_text(encoding="utf-8")
    changed = rename_project(dist_name="my-tool", root=tmp_path)
    assert helper.read_text(encoding="utf-8") == before
    assert helper not in changed
    version_test = (tmp_path / "tests" / "test_version.py").read_text(
        encoding="utf-8",
    )
    assert "my_tool" in version_test

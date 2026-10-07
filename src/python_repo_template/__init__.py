"""python-repo-template: a starter Typer CLI package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("python-repo-template")
except PackageNotFoundError:  # pragma: no cover - editable/dev fallback
    __version__ = "0.0.0"

__all__ = ["__version__"]

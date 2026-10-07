"""Package version lookup shared by the public API and core helpers."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("python-repo-template")
except PackageNotFoundError:  # pragma: no cover - editable/dev fallback
    __version__ = "0.0.0"

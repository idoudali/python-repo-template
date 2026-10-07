"""python-repo-template: a starter Typer CLI package."""

from typing import TYPE_CHECKING

from python_repo_template._version import __version__

if TYPE_CHECKING:
    from python_repo_template.core import greet as greet
    from python_repo_template.core import runtime_info as runtime_info

__all__ = ["__version__", "greet", "runtime_info"]


def __getattr__(name: str) -> object:
    """Lazy-load ``greet`` / ``runtime_info`` to avoid an import cycle."""
    if name in {"greet", "runtime_info"}:
        from python_repo_template import core

        return getattr(core, name)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)

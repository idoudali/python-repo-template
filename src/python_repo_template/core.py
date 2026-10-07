"""Pure helpers used by the CLI."""

from __future__ import annotations

import platform
import sys
from typing import TypedDict

from python_repo_template._version import __version__


class RuntimeInfo(TypedDict):
    """Version and runtime metadata returned by :func:`runtime_info`."""

    version: str
    python: str
    platform: str


def greet(name: str, *, count: int = 1, shout: bool = False) -> list[str]:
    """Build greeting lines for ``name``.

    Args:
        name: Person or thing to greet.
        count: How many times to repeat the greeting. Must be >= 1.
        shout: When True, upper-case the greeting.

    Returns:
        One greeting string per repetition.

    Raises:
        ValueError: If ``count`` is less than 1.

    Examples:
        >>> greet("Ada", count=2)
        ['Hello, Ada!', 'Hello, Ada!']
        >>> greet("Ada", shout=True)
        ['HELLO, ADA!']
    """
    if count < 1:
        msg = f"count must be >= 1, got {count}"
        raise ValueError(msg)
    message = f"Hello, {name}!"
    if shout:
        message = message.upper()
    return [message] * count


def runtime_info() -> RuntimeInfo:
    """Return version and runtime metadata.

    Returns:
        A mapping with ``version``, ``python``, and ``platform`` keys.

    Examples:
        >>> info = runtime_info()
        >>> set(info) == {"version", "python", "platform"}
        True
    """
    return {
        "version": __version__,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }

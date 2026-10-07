"""Tests for the package public API surface."""

import pytest

import python_repo_template as pkg
from python_repo_template import greet, runtime_info


def test_lazy_reexports() -> None:
    assert greet("Ada") == ["Hello, Ada!"]
    info = runtime_info()
    assert set(info) == {"version", "python", "platform"}


def test_lazy_exports_appear_in_dir() -> None:
    assert {"greet", "runtime_info"} <= set(dir(pkg))


def test_unknown_attribute_raises() -> None:
    missing = "not_a_real_export"
    with pytest.raises(AttributeError, match="no attribute"):
        getattr(pkg, missing)

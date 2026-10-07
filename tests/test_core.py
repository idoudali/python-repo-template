"""Tests for core helpers."""

import pytest

from python_repo_template.core import greet, runtime_info


@pytest.mark.parametrize(
    "case",
    [
        ("Ada", 1, False, ["Hello, Ada!"]),
        ("Ada", 2, False, ["Hello, Ada!", "Hello, Ada!"]),
        ("Ada", 1, True, ["HELLO, ADA!"]),
    ],
)
def test_greet(case: tuple[str, int, bool, list[str]]) -> None:
    name, count, shout, expected = case
    assert greet(name, count=count, shout=shout) == expected


def test_greet_rejects_non_positive_count() -> None:
    with pytest.raises(ValueError, match="count must be >= 1"):
        greet("Ada", count=0)


def test_runtime_info_keys() -> None:
    info = runtime_info()
    assert set(info) == {"version", "python", "platform"}
    assert info["version"]
    assert info["python"]
    assert info["platform"]

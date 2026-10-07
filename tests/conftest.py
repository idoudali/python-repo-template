"""Shared pytest fixtures."""

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """Return a Typer CliRunner for CLI tests."""
    return CliRunner()

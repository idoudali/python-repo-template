"""Tests for version reporting."""

from typer.testing import CliRunner

from python_repo_template import __version__
from python_repo_template.cli import _version_callback, app


def test_package_version_shape() -> None:
    assert __version__
    assert __version__[0].isdigit()


def test_cli_version_option(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_cli_help(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Template Python package CLI" in result.stdout


def test_version_callback_noop_when_false() -> None:
    _version_callback(value=False)

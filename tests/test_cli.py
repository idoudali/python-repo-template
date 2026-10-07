"""CLI integration tests."""

import json

from typer.testing import CliRunner

from python_repo_template import __version__
from python_repo_template.cli import app


def test_greet_default(runner: CliRunner) -> None:
    result = runner.invoke(app, ["greet", "Ada"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "Hello, Ada!"


def test_greet_count_and_shout(runner: CliRunner) -> None:
    result = runner.invoke(app, ["greet", "Ada", "--count", "2", "--shout"])
    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["HELLO, ADA!", "HELLO, ADA!"]


def test_info_text(runner: CliRunner) -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert f"version: {__version__}" in result.stdout
    assert "python:" in result.stdout
    assert "platform:" in result.stdout


def test_info_json(runner: CliRunner) -> None:
    result = runner.invoke(app, ["info", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["version"] == __version__
    assert "python" in payload
    assert "platform" in payload

"""Command-line interface."""

from __future__ import annotations

import json
from typing import Annotated

import typer

from python_repo_template import __version__

app = typer.Typer(
    name="python-repo-template",
    help="Template Python package CLI.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    """Print the package version and exit."""
    if value:
        typer.echo(__version__)
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            help="Show the version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Template Python package CLI."""


@app.command()
def greet(
    name: Annotated[str, typer.Argument(help="Name to greet.")],
    count: Annotated[
        int,
        typer.Option("--count", "-c", min=1, help="Repeat the greeting."),
    ] = 1,
    shout: Annotated[
        bool,
        typer.Option("--shout/--no-shout", help="Upper-case the greeting."),
    ] = False,
) -> None:
    """Greet someone one or more times."""
    # Lazy import keeps ``--help`` / ``--version`` startup light.
    from python_repo_template.core import greet as build_greetings

    for line in build_greetings(name, count=count, shout=shout):
        typer.echo(line)


@app.command()
def info(
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON."),
    ] = False,
) -> None:
    """Print version, Python, and platform information."""
    from python_repo_template.core import runtime_info

    data = runtime_info()
    if as_json:
        typer.echo(json.dumps(data, sort_keys=True))
        return
    for key, value in data.items():
        typer.echo(f"{key}: {value}")

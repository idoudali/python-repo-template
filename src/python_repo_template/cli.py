"""Command-line interface."""

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

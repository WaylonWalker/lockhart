# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT


import typer

from lockhart.cli.common import verbose_callback
from lockhart.cli.config import config_app
from lockhart.cli.history import history_app
from lockhart.cli.prompt import prompt_app
from lockhart.cli.tui import tui_app

app = typer.Typer(
    name="lockhart",
    help="Lockhart codegen",
)


def version_callback(value: bool) -> None:
    """Callback function to print the version of the lockhart package.

    Args:
        value (bool): Boolean value to determine if the version should be printed.

    Raises:
        typer.Exit: If the value is True, the version will be printed and the program will exit.

    Example:
        version_callback(True)
    """
    if value:
        from lockhart.__about__ import __version__

        typer.echo(f"{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:
    return


app.add_typer(config_app)
app.add_typer(prompt_app)
app.add_typer(history_app)
app.add_typer(tui_app)

import typer
from rich.console import Console

from lockhart.cli.common import verbose_callback
from lockhart.history import load_history

history_app = typer.Typer()


@history_app.callback()
def history(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    "history cli"


@history_app.command()
def list(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    """
    List the history of the commands.
    """
    Console().print(load_history())

import typer
from rich.console import Console

from lockhart.history import load_history

history_app = typer.Typer()


@history_app.callback()
def history():
    "history cli"


@history_app.command()
def list(
    verbose: bool = typer.Option(False, help="show the log messages"),
):
    Console().print(load_history())

import typer

from lockhart.cli.common import verbose_callback
from lockhart.tui.app import run_app

tui_app = typer.Typer()


@tui_app.callback(invoke_without_command=True)
def tui(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    run_app()

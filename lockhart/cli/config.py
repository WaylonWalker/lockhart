import typer

from lockhart.config import config as configuration
from lockhart.console import console

config_app = typer.Typer()


@config_app.callback()
def config():
    "configuration cli"


@config_app.command()
def show():
    console.print(configuration)

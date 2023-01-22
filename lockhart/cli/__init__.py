# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT


from rich.console import Console
import typer

from lockhart import prompts
from lockhart.config import config as configuration
from lockhart.console import console
from lockhart.history import load_history

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
        None, "--version", callback=version_callback, is_eager=True
    ),
) -> None:
    # Do other global stuff, handle other global options here
    return


config_app = typer.Typer()
prompt_app = typer.Typer()
history_app = typer.Typer()
app.add_typer(config_app)
app.add_typer(prompt_app)
app.add_typer(history_app)


@config_app.callback()
def config():
    "configuration cli"


@config_app.command()
def show():
    console.print(configuration)


@prompt_app.callback()
def prompt():
    "prompt cli"


@prompt_app.command()
def list():
    for prompt in configuration.get("prompts", {}).keys():
        console.print(prompt)


@prompt_app.command()
def run(
    prompt: str = typer.Argument(..., help="the configured prompt to run"),
    dry_run: bool = typer.Option(False, help="run without sending the prompt"),
    verbose: bool = typer.Option(False, help="show the log messages"),
    edit: bool = typer.Option(
        False, help="open the resulting prompt in your editor before running"
    ),
):
    if not verbose:
        console.quiet = True
    console.log(f"running configured prompt: {prompt}")
    result = prompts.run_configured_prompt(prompt, dry_run, edit)
    if result:
        try:
            Console().print(result["choices"][0]["text"])
        except KeyError:
            Console().print(result)


@history_app.callback()
def history():
    "history cli"


@history_app.command()
def list(
    verbose: bool = typer.Option(False, help="show the log messages"),
):
    Console().print(load_history())

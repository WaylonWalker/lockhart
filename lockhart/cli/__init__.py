# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT


import typer

from lockhart import prompts
from lockhart.config import config as configuration
from lockhart.console import console

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
app.add_typer(config_app)
app.add_typer(prompt_app)


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
    edit: bool = typer.Option(
        False, help="open the resulting prompt in your editor before running"
    ),
):
    result = prompts.run_configured_prompt(prompt, dry_run, edit)
    console.print(result)

    # @app.command()
    # def docstring():
    #     code = pyperclip.paste()
    #     completion = write_docstring(code)
    #     pyperclip.copy(completion)

    # @app.command()
    # def refactor():
    #     code = pyperclip.paste()
    #     completion = refactor_code(code, input("refactor the following code to "))
    #     pyperclip.copy(completion)

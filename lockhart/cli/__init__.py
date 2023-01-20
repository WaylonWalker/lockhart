# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT

import pyperclip
import typer

from lockhart.prompts import refactor_code, write_docstring

# @click.group(
#     context_settings={"help_option_names": ["-h", "--help"]},
#     invoke_without_command=True,
# )
# @click.version_option(version=__version__, prog_name="lockhart")
# @click.pass_context
# def lockhart(ctx: click.Context):
#     ...


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


@app.command()
def docstring():
    code = pyperclip.paste()
    completion = write_docstring(code)
    pyperclip.copy(completion)


@app.command()
def refactor():
    code = pyperclip.paste()
    completion = refactor_code(code, input("refactor the following code to "))
    pyperclip.copy(completion)

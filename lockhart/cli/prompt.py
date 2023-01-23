import typer
from rich.console import Console

from lockhart import prompts
from lockhart.config import config as configuration
from lockhart.console import console

prompt_app = typer.Typer()


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

import typer
from rich.console import Console

from lockhart import prompts
from lockhart.cli.common import verbose_callback
from lockhart.config import config as configuration
from lockhart.console import console

prompt_app = typer.Typer()


@prompt_app.callback(invoke_without_command=True)
def prompt(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    "prompt cli"


@prompt_app.command()
def list(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:
    for prompt in configuration.get("prompts", {}).keys():
        Console().print(prompt)


@prompt_app.command()
def run(
    prompt: str = typer.Argument(..., help="the configured prompt to run"),
    dry_run: bool = typer.Option(False, help="run without sending the prompt"),
    edit: bool = typer.Option(
        False, help="open the resulting prompt in your editor before running"
    ),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    console.log(f"running configured prompt: {prompt}")
    result = prompts.run_prompt(prompt, dry_run, edit)
    if result:
        try:
            Console().print(result["choices"][0]["text"])
        except KeyError:
            Console().print(result)
        except KeyError:
            Console().print(result)
        except KeyError:
            Console().print(result)

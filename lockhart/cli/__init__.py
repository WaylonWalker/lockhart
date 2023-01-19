# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
import ast
from collections import namedtuple

import click
import openai
import pyperclip

from ..__about__ import __version__

# from markata.plugins.load import load


my_code = """
@hook_impl
@register_attr("articles")
def load(markata: "MarkataMarkdown") -> None:
    progress = Progress(
        BarColumn(bar_width=None), transient=True, console=markata.console
    )
    if not markata.config.get("repo_url", "https://github.com/").endswith("/"):
        markata.config["repo_url"] = (
            markata.config.get("repo_url", "https://github.com/") + "/"
        )

    futures = [get_post(article, markata) for article in markata.files]
    task_id = progress.add_task("loading markdown")
    progress.update(task_id, total=len(futures))
    with progress:
        while not all([f.done() for f in futures]):
            time.sleep(0.1)
            progress.update(task_id, total=len([f for f in futures if f.done()]))
    articles = [f.result() for f in futures]
    articles = [a for a in articles if a]
    markata.articles = articles

"""


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="lockhart")
@click.pass_context
def lockhart(ctx: click.Context):
    code = pyperclip.paste()
    # code = "\n".join(code)
    completion = write_docstring(code)
    pyperclip.copy(completion)


def write_docstring(code):

    parsed = parse_function(code)
    prompt = f'# Python 3.10 \n{code}\n\n#Please write a high quality python docstring conforming to the google code style for docstrings for the above code.\nThe name of the function is: ```{parsed.name}```.\nIt has the following signature {parsed.args}. \n\nDo not return the full function.\nOnly return the docstring.\nInclude an example if you can.\nIt should start with `"""`\nfollowed immediately by a short summary line\n followed by a newline\nfollowed by a short description\n followed by another newline\nthen followed by any of the following sections sections if they apply to this function (Args: , Returns: , Raises: , Yields: , Note: , Example: )\n"""'
    # prompt = f"Please write a python docstring conforming to the google code style for docstrings.\n\n{code}\n"
    # prompt = f'# Python 3.10\n{code}\n\n# An elaborate, high quality docstring for the above function:\n"""'

    print(f"generating a response for \n\n{prompt}")
    print("-" * 80)
    print()

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        # max_tokens=500,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", '"""'],
    )
    print(response["choices"][0]["text"])
    return response["choices"][0]["text"]


def write_test(code):

    parsed = parse_function(code)
    prompt = f'Please write a test from the following function using pytest: ```{parsed.name}``` with the following signature {parsed.args}, and the following source code {code}, do not return the full function, only return the docstring surrounded by `"""`, indent the docstring to match the function indentation level'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
    )
    return response["choices"][0]["text"]


def write_blog(code):

    prompt = f"Write a blog post about the following code in Markdown. \n\n```{code}```"

    print(f"generating a response for {prompt[:200]}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
    )
    return response["choices"][0]["text"]


Function = namedtuple("Function", "name, args")


def parse_function(code: str) -> Function:
    tree = ast.parse(code)
    args = []
    name = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            args = [
                f"{arg.arg}:"  # {arg.annotation.value}"
                if arg.annotation
                else f"{arg.arg}: None"
                for arg in node.args.args
            ]
    if name is None:
        raise ValueError("input is not a FunctionDef")
    return Function(name, args)


# code_str = """def example_function(arg1:int,arg2:str)->int:
#     pass"""
# name, args, return_annotation = extract_function_signature(code_str)
# print(name)
# print(args)
# print(return_annotation)


def parse_code():
    tree = ast.parse(my_code)
    args = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            # args = [arg.arg for arg in node.args.args]
            # args = [
            #     (arg.arg, arg.annotation.value) if arg.annotation else (arg.arg, None)
            #     for arg in node.args.args
            # ]
            args = [
                f"{arg.arg}: {arg.annotation.value}"
                if arg.annotation
                else f"{arg.arg}: None"
                for arg in node.args.args
            ]
    return name, args

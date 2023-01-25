import copy
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from typing import Optional, Union

from jinja2 import Template
import openai
import tomlkit

from lockhart.config import config
from lockhart.console import console
from lockhart.history import load_history, save_history


def load_prompt(prompt: str) -> dict:
    """
    Loads the configuration for the prompt from config.  Finds the
    corresponding profile and unpacks the prompt config into that profile.
    """
    profile_name = config["prompts"][prompt].get("profile")
    prompt_config = config["prompts"][prompt]
    if profile_name is None or profile_name not in config["profiles"]:
        return prompt_config
    profile = copy.deepcopy(config["profiles"][profile_name])
    for key, value in prompt_config.items():
        if key != "profile":
            profile.update({key: value})
    return profile


def run_prompt(
    prompt_name: Union[str, dict], dry_run: bool = False, edit: bool = False
) -> Optional[str]:

    console.log("running prompt")
    text = ""

    console.log("getting stdin")

    if not sys.stdin.isatty():
        # if nothing is piped in, sys.stin.read will block forever
        text = sys.stdin.read()

    console.log(f"read stdin: {text}")

    if isinstance(prompt_name, str):
        prompt = load_prompt(prompt_name)
    else:
        prompt = prompt_name

    prompt = template_prompt(prompt, text)

    if edit:
        prompt = edit_prompt(prompt)

    if prompt is None:
        return "prompt quit"

    if dry_run:
        console.log("dry run enabled, returning prompt")
        return prompt

    console.log("prompt: ", prompt)
    console.log("running completion")
    # response = openai.Completion.create(**prompt)
    api = getattr(openai, prompt.pop("api"))
    response = api.create(**prompt)
    text = response["choices"][0]["text"]
    history = load_history()
    history.append(
        {
            "prompt_name": prompt_name,
            "datetime": datetime.now(),
            "request": prompt,
            "response": response,
        }
    )
    save_history(history)
    return response


def template_prompt(prompt: dict, text: str) -> dict:
    for key in prompt:
        console.log(f"templating {key}: {prompt[key]}")

        if isinstance(prompt[key], str):
            template = Template(prompt[key])
            value = template.render(input=input, text=text)
            prompt.update(
                {
                    key: tomlkit.string(
                        f"\n{value}\n" if "\n" in value else value,
                        multiline=("\n" in value),
                    )
                }
            )
    return prompt


def edit_prompt(prompt: dict) -> dict:
    editor = os.environ.get("EDITOR", "vim")
    console.log(f"editing prompt with {editor}")
    file = tempfile.NamedTemporaryFile(prefix="lockhart", suffix=".toml")
    file.write(tomlkit.dumps(prompt).encode())
    file.seek(0)
    st_mtime = os.stat(file.name).st_mtime  # create time by lockhart
    initial_time = time.time()
    proc = subprocess.Popen([editor, file.name])
    proc.wait()
    if os.stat(file.name).st_mtime == st_mtime:
        console.log(os.stat(file.name).st_mtime)
        console.log("st_mtime", st_mtime)
        console.log("initial_time", initial_time)
        console.log("editor quit")
        return
    console.log(os.stat(file.name).st_mtime)
    console.log(os.stat(file.name).st_atime)
    console.log(os.stat(file.name).st_ctime)

    prompt = tomlkit.loads(Path(file.name).read_text())
    console.log(f"updated prompt\n{prompt}")
    return prompt


def list_args(func: callable):
    """lists the arguments that the function takes"""
    args = func.__code__.co_varnames
    return args
    return list(func.__code__.co_varnames)

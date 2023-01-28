import copy
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import openai
import tomlkit

from lockhart.config import config
from lockhart.console import console
from lockhart.history import load_history, save_history
from lockhart.jinja_env import get_jinja_env


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
        return edit_prompt(prompt)

    if prompt is None:
        return "prompt quit"

    if dry_run:
        console.log("dry run enabled, returning prompt")
        return prompt

    console.log("prompt: ", prompt)
    console.log("running completion")
    # response = openai.Completion.create(**prompt)
    if prompt.get("api", None):
        api = getattr(openai, prompt.pop("api"))
    elif "prompt" in prompt.keys():
        api = getattr(openai, "Completion")
    else:
        api = getattr(openai, "Edit")

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
            template = get_jinja_env().from_string(prompt[key])
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
    file.write(("# edit = true\n" + tomlkit.dumps(prompt)).encode())
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
    dry_run = bool(prompt.pop("dry_run", False))
    edit = bool(prompt.pop("edit", False))
    return run_prompt(prompt, dry_run=dry_run, edit=edit)


def list_args(func: callable):
    """lists the arguments that the function takes"""
    args = func.__code__.co_varnames
    return args
    return list(func.__code__.co_varnames)

import copy
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Optional

import openai
from jinja2 import Template

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


def run_configured_prompt(prompt_name: str, dry_run: bool, edit: bool) -> Optional[str]:

    console.log("running prompt")
    text = ""

    console.log("getting stdin")
    for line in sys.stdin:
        text = text + line
    console.log("read stdin")

    prompt = load_prompt(prompt_name)

    for key in prompt:
        console.log(f"templating {key}: {prompt[key]}")

        if isinstance(prompt[key], str):
            template = Template(prompt[key])
            prompt[key] = template.render(input=input, text=text)

    if edit:
        editor = os.environ.get("EDITOR", "vim")
        console.log(f"editing prompt with {editor}")
        file = tempfile.NamedTemporaryFile(prefix="lockhart")
        file.write(prompt["prompt"].encode())
        file.seek(0)
        proc = subprocess.Popen([editor, file.name])
        proc.wait()
        if os.stat(file.name).st_mtime != os.stat(file.name).st_atime:
            console.log("editor quit")
            return

        prompt["prompt"] = file.read().decode()

    if prompt is None:
        raise KeyError(f"{prompt} is not configured")

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


def list_args(func: callable):
    """lists the arguments that the function takes"""
    args = func.__code__.co_varnames
    return args
    return list(func.__code__.co_varnames)

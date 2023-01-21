import copy
import os
import subprocess
import sys
import tempfile
from typing import Optional

from jinja2 import Template
import openai

from lockhart.config import config


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


def run_configured_prompt(prompt: str, dry_run: bool, edit: bool) -> Optional[str]:

    text = ""
    for line in sys.stdin:
        text = text + line

    prompt = load_prompt(prompt)
    template = Template(prompt["prompt"])
    prompt["prompt"] = template.render(input=input, text=text)
    if edit:
        file = tempfile.NamedTemporaryFile(prefix="lockhart")
        file.write(prompt["prompt"].encode())
        file.seek(0)
        editor = os.environ.get("EDITOR", "vim")
        proc = subprocess.Popen([editor, file.name])
        res = proc.wait()
        prompt["prompt"] = file.read().decode()
        if res != 0:
            return "editor quit"

    if prompt is None:
        raise KeyError(f"{prompt} is not configured")

    if dry_run:
        return prompt

    response = openai.Completion.create(**prompt)
    text = response["choices"][0]["text"]
    return response


def list_args(func: callable):
    """lists the arguments that the function takes"""
    args = func.__code__.co_varnames
    return args
    return list(func.__code__.co_varnames)

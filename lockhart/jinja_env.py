from pathlib import Path

import jinja2


def get_jinja_env():
    env = jinja2.Environment()
    env.globals["read_text"] = lambda file: f"## {file}\n{Path(file).read_text()}"
    return env

# lockhart/config.py
from pathlib import Path

import tomlkit


def get_config(
    config_file=Path.home() / ".config" / "lockhart" / "lockhart.toml",
    default_config_file=Path(__file__).parent / "sample-lockhart.toml",
):

    try:
        config = tomlkit.loads(config_file.read_text())
    except FileNotFoundError:
        print(f"No config file found at {config_file}. Using default config.")
        config_file = default_config_file
        config = tomlkit.loads(config_file.read_text())

    return config


config = get_config()

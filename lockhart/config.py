from pathlib import Path

import toml

# config_file = Path.home() / ".config" / "lockhart" / "lockhart.toml"
config_file = Path() / "sample-lockhart.toml"
config = toml.load(config_file)

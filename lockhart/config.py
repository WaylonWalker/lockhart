from pathlib import Path

import tomlkit

# config_file = Path.home() / ".config" / "lockhart" / "lockhart.toml"
config_file = Path() / "sample-lockhart.toml"
config = tomlkit.loads(config_file.read_text())

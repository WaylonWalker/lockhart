from lockhart.config import get_config
from pathlib import Path


def test_get_config_default(mocker):
    mocker.patch(
        "pathlib.Path.home",
        return_value=Path(__file__).parents[1] / "lockhart" / "sample-lockhart.toml",
    )
    mocker.patch("pathlib.Path.read_text", return_value='[lockhart]\nname = "Lockhart"')
    config = get_config()
    assert config["lockhart"]["name"] == "Lockhart"


def test_get_config_custom():
    config_file = Path(__file__).parents[1] / "lockhart" / "sample-lockhart.toml"
    config = get_config(config_file)
    assert config["lockhart"]["name"] == "Lockhart"

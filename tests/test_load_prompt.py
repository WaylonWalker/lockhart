import pytest

from lockhart.prompts import load_prompt


@pytest.fixture
def config():
    return {
        "prompts": {
            "prompt1": {"profile": "profile1", "key1": "value1"},
            "prompt2": {"profile": "profile2", "key2": "value2"},
            "prompt3": {"key1": "value1"},
        },
        "profiles": {"profile1": {"key3": "value3"}, "profile2": {"key4": "value4"}},
    }


def test_load_prompt(config, mocker):
    mock_config = mocker.patch("lockhart.prompts.config")
    mock_config.__getitem__.side_effect = config.__getitem__
    prompt1_config = load_prompt("prompt1")
    assert prompt1_config == {"key1": "value1", "key3": "value3"}

    prompt2_config = load_prompt("prompt2")
    assert prompt2_config == {"key2": "value2", "key4": "value4"}

    prompt3_config = load_prompt("prompt3")
    assert prompt3_config == {"key1": "value1"}

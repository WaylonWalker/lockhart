import datetime
from unittest.mock import patch

import pytest

HISTORY = []

HISTORY.append(
    {
        "prompt_name": "create-history",
        "datetime": datetime.datetime(2023, 1, 22, 10, 24, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python script to pickle a python list into a file called ~/.config/lockhart/history.pkl",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\nimport pickle\nimport os\n\ndef save_history(history):\n    """\n    Save the history to a file.\n    """\n    home = os.path.expanduser("~")\n    config_dir = os.path.join(home, ".config", "lockhart")\n    if not os.path.exists(config_dir):\n        os.makedirs(config_dir)\n    history_file = os.path.join(config_dir, "history.pkl")\n    with open(history_file, "wb") as f:\n        pickle.dump(history, f)\n\ndef load_history():\n    """\n    Load the history from a file.\n    """\n    home = os.path.expanduser("~")\n    config_dir = os.path.join(home, ".config", "lockhart")\n    history_file = os.path.join(config_dir, "history.pkl")\n    if os.path.exists(history_file):\n        with open(history_file, "rb") as f:\n            return pickle.load(f)\n    else:\n        return []\n\nif __name__ == "__main__":\n    history = load_history()\n    history.append("test")\n    save_history(history)\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)


HISTORY.append(
    {
        "prompt_name": "create-function",
        "datetime": datetime.datetime(2023, 2, 15, 12, 15, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python function to calculate the area of a circle",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\ndef area_of_circle(radius):\n    """\n    Calculate the area of a circle given the radius.\n    """\n    return 3.14 * (radius ** 2)\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)

HISTORY.append(
    {
        "prompt_name": "create-class",
        "datetime": datetime.datetime(2023, 3, 10, 14, 30, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python class to represent a person",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\nclass Person:\n    """\n    A class to represent a person.\n    """\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n    def say_hello(self):\n        print("Hello, my name is {} and I am {} years old.".format(self.name, self.age))\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)

HISTORY.append(
    {
        "prompt_name": "create-dictionary",
        "datetime": datetime.datetime(2023, 4, 5, 16, 45, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python script to create a dictionary of key-value pairs",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\ndef create_dictionary(keys, values):\n    """\n    Create a dictionary of key-value pairs.\n    """\n    return dict(zip(keys, values))\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)

HISTORY.append(
    {
        "prompt_name": "create-list",
        "datetime": datetime.datetime(2023, 5, 1, 18, 0, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python script to create a list of numbers from 1 to 10",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\ndef create_list():\n    """\n    Create a list of numbers from 1 to 10.\n    """\n    return list(range(1, 11))\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)


HISTORY.append(
    {
        "prompt_name": "create-tuple",
        "datetime": datetime.datetime(2023, 6, 20, 20, 15, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python script to create a tuple of numbers from 1 to 10",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\ndef create_tuple():\n    """\n    Create a tuple of numbers from 1 to 10.\n    """\n    return tuple(range(1, 11))\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)

HISTORY.append(
    {
        "prompt_name": "create-string",
        "datetime": datetime.datetime(2023, 7, 10, 22, 30, 8, 977243),
        "request": {
            "engine": "code-davinci-edit-001",
            "temperature": 0,
            "top_p": 1.0,
            "instruction": "write a python script to create a string of characters",
            "input": "",
        },
        "response": {
            "choices": [
                {
                    "index": 0,
                    "text": '#!/usr/bin/env python\n\ndef create_string(characters):\n    """\n    Create a string of characters.\n    """\n    return \'\'.join(characters)\n',
                }
            ],
            "created": 1674404634,
            "object": "edit",
            "usage": {
                "completion_tokens": 356,
                "prompt_tokens": 35,
                "total_tokens": 391,
            },
        },
    }
)


@pytest.fixture()
def load_history():
    with patch("lockhart.tui.app.load_history", return_value=HISTORY) as f:
        yield f

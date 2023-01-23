import os
from pathlib import Path
import pickle

import pytest

from lockhart.history import load_history, save_history


@pytest.fixture
def history_file(tmpdir):
    return tmpdir.join("history.pkl")


def test_save_history(history_file):
    history = ["test1", "test2"]
    save_history(history, history_file)
    assert os.path.exists(str(history_file))
    with open(str(history_file), "rb") as f:
        saved_history = pickle.load(f)
    assert saved_history == history


def test_load_history(history_file):
    history = ["test1", "test2"]
    with open(str(history_file), "wb") as f:
        pickle.dump(history, f)
    loaded_history = load_history(str(history_file))
    assert loaded_history == history


def test_load_history_empty(history_file):
    loaded_history = load_history(str(history_file))
    assert loaded_history == []


@pytest.fixture
def history_file_pathlib(tmpdir):
    return Path(tmpdir.join("history.pkl"))


def test_save_history_pathlib(history_file_pathlib):
    history = ["test1", "test2"]
    save_history(history, history_file_pathlib)
    assert os.path.exists(history_file_pathlib)
    with open(history_file_pathlib, "rb") as f:
        saved_history = pickle.load(f)
    assert saved_history == history


def test_load_history_pathlib(history_file_pathlib):
    history = ["test1", "test2"]
    with open(history_file_pathlib, "wb") as f:
        pickle.dump(history, f)
    loaded_history = load_history(history_file_pathlib)
    assert loaded_history == history


def test_load_history_empty_pathlib(history_file_pathlib):
    loaded_history = load_history(history_file_pathlib)
    assert loaded_history == []

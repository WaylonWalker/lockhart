#!/usr/bin/env python

from pathlib import Path
import pickle

from lockhart.console import console


def save_history(history, history_file=None):
    """Save the history to a file."""
    if history_file is None:
        history_file = get_history_file()
    if isinstance(history_file, str):
        history_file = Path(history_file)
    console.log(f"saving\n{history} to {history_file}")
    with history_file.open("wb") as f:
        pickle.dump(history, f)
    console.log(f"wrote history")


def load_history(history_file=None):
    """Load the history from a file."""
    if history_file is None:
        history_file = get_history_file()
    if isinstance(history_file, str):
        history_file = Path(history_file)
    if history_file.exists():
        with history_file.open("rb") as f:
            history = pickle.load(f)
            console.log(f"loaded {len(history)} items into history")
            return history
    else:
        console.log(f"history_file does not exist, returning empty history")
        return []


def get_history_file():
    config_dir = Path.home() / ".config" / "lockhart"
    config_dir.mkdir(parents=True, exist_ok=True)
    history_file = config_dir / "history.pkl"
    return history_file


if __name__ == "__main__":
    history = load_history()
    history.append("test")
    save_history(history)

#!/usr/bin/env python

from pathlib import Path
import pickle

from lockhart.console import console


def save_history(history):
    """Save the history to a file."""
    console.log(f"saving\n{history}")
    config_dir = Path.home() / ".config" / "lockhart"
    config_dir.mkdir(parents=True, exist_ok=True)
    history_file = config_dir / "history.pkl"
    with history_file.open("wb") as f:
        pickle.dump(history, f)
    console.log(f"wrote history")


def load_history():
    """Load the history from a file."""
    config_dir = Path.home() / ".config" / "lockhart"
    history_file = config_dir / "history.pkl"
    if history_file.exists():
        with history_file.open("rb") as f:
            history = pickle.load(f)
            console.log(f"loaded {len(history)} items into history")
            return history
    else:
        console.log(f"history_file does not exist, returning empty history")
        return []


if __name__ == "__main__":
    history = load_history()
    history.append("test")
    save_history(history)

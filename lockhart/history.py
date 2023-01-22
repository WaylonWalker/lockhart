#!/usr/bin/env python

import os
import pickle

from lockhart.console import console


def save_history(history):
    """
    Save the history to a file.
    """
    console.log(f"saving\n{history}")
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".config", "lockhart")
    if not os.path.exists(config_dir):
        console.log(f"creating {config_dir}")
        os.makedirs(config_dir)
    history_file = os.path.join(config_dir, "history.pkl")
    with open(history_file, "wb") as f:
        pickle.dump(history, f)
    console.log(f"wrote history")


def load_history():
    """
    Load the history from a file.
    """
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".config", "lockhart")
    history_file = os.path.join(config_dir, "history.pkl")
    if os.path.exists(history_file):
        with open(history_file, "rb") as f:
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

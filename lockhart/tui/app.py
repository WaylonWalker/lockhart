from pathlib import Path

import pyperclip
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Static

from lockhart.config import config
from lockhart.history import load_history
from lockhart.prompts import run_prompt

REQUEST_KEYS = ["engine", "temperature", "instruction", "input", "prompt"]
RESPONSE_KEYS = ["created", "choices", "usage"]


class Request(Static):
    """A Request widget."""

    data = reactive({})
    myid = reactive(0)

    def __init__(self, id, data, classes=None):
        super().__init__(classes=classes)
        self.data = data
        self.myid = id

    def update_data(self):
        self.log("updating")
        self.query_one("#id", Static).update(str(self.myid))
        self.query_one("#date", Static).update(str(self.data["datetime"]))
        for key in REQUEST_KEYS:
            value = str(self.data.get("request", {}).get(key, ""))
            if value == "":
                self.query_one(f"#request-{key}-container").add_class("hidden")
                self.query_one(f"#request-{key}").add_class("hidden")
                self.query_one(f"#request-{key}", Static).update("")
            else:
                self.query_one(f"#request-{key}", Static).update(value)
                self.query_one(f"#request-{key}-container").remove_class("hidden")
                self.query_one(f"#request-{key}").remove_class("hidden")
        self.query_one(f"#response-text", Static).update(
            self.data["response"]["choices"][0]["text"]
        )

    def compose(self) -> ComposeResult:
        """Create child widgets of a Request."""
        yield Container(
            Static(id="id", classes="id"),
            Static(id="date", classes="date"),
            id="id-container",
        )
        request_containers = [
            Container(
                Static(id=f"request-{key}", classes=f"request-{key}"),
                id=f"request-{key}-container",
            )
            for key in REQUEST_KEYS
        ]
        yield Static("REQUEST", id="request-header")
        yield Container(*request_containers, id="requests")
        yield Static("RESULTS", id="results-header")
        yield Container(
            Static(id="response-text", classes="response-text"),
            id="response-text-container",
        )

    def copy_to_clipboard(self):

        pyperclip.copy(self.data["response"]["choices"][0]["text"])


class RequestApp(App):
    """A Textual app to manage requests."""

    CSS_PATH = Path("__file__").parent / "app.css"
    BINDINGS = [tuple(b.values()) for b in config["lockhart"]["tui"]["bindings"]]

    @property
    def history(self):
        try:
            return self._history
        except AttributeError:
            self.update_history()
            return self._history

    def update_history(self):
        self._history = load_history()
        self._history.reverse()
        self._history

    def on_mount(self):
        self.query_one(Request).update_data()
        self.i = 0

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.i = 0
        yield Container(
            Request(id=self.i, data=self.history[self.i]),
            id="timers",
        )
        yield Footer()

    def action_next(self):
        self.activate(1)

    def action_prev(self):
        self.activate(-1)

    def action_copy_to_clipboard(self):
        self.query_one(Request).copy_to_clipboard()

    def activate(self, n=0, i=None):
        self.i = self.i + n
        if self.i > len(self.history) - 1:
            self.i = 0
        if self.i < 0:
            self.i = len(self.history) - 1
        self.query_one(Request).data = self.history[self.i]
        self.query_one(Request).myid = self.i
        self.query_one(Request).update_data()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
        self.log("going dark")

    def action_edit(self):
        prompt = self.history[self.i]["request"]
        if "input" in prompt.keys():
            prompt["api"] = "Edit"
            prompt["input"] = self.history[self.i]["response"]["choices"][0]["text"]
        else:
            prompt["api"] = "Edit"
            prompt["engine"] = "code-davinci-edit-001"
            prompt["instruction"] = ""
            prompt["input"] = self.history[self.i]["response"]["choices"][0]["text"]
            remove_keys = [
                "prompt",
                "frequency_penalty",
                "presence_penalty",
                "max_tokens",
            ]
            for key in remove_keys:
                if key in prompt.keys():
                    prompt.pop(key)
        self._driver.stop_application_mode()
        run_prompt(prompt, edit=True)
        self._driver.start_application_mode()
        self.update_history()
        self.activate(i=0)

    def action_run_prompt(self):
        prompt = self.query_one(Request).data["request"]
        self._driver.stop_application_mode()
        run_prompt(prompt, edit=True)
        self._driver.start_application_mode()
        self.update_history()
        self.activate(i=0)

    def action_new_commit(self):
        self._driver.stop_application_mode()
        run_prompt("commit", edit=True)
        self._driver.start_application_mode()
        self.update_history()
        self.activate(i=0)

    def action_new_code_edit(self):
        self._driver.stop_application_mode()
        run_prompt("code-edit", edit=True)
        self._driver.start_application_mode()
        self.update_history()
        self.activate(i=0)

    def action_new_code_create(self):
        self._driver.stop_application_mode()
        run_prompt("code-create", edit=True)
        self._driver.start_application_mode()
        self.update_history()
        self.activate(i=0)


def run_app():

    import os
    import sys

    from textual.features import parse_features

    dev = "--dev" in sys.argv
    features = set(parse_features(os.environ.get("TEXTUAL", "")))
    if dev:
        features.add("debug")
        features.add("devtools")

    os.environ["TEXTUAL"] = ",".join(sorted(features))
    app = RequestApp()
    app.run()


if __name__ == "__main__":
    run_app()

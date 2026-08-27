from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from pentui.core.models import ArgumentDefinition


class ValueInputModal(ModalScreen[str | None]):
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, argument: ArgumentDefinition, current_value: str = "") -> None:
        super().__init__()
        self.argument = argument
        self.current_value = current_value

    def compose(self) -> ComposeResult:
        with Vertical(id="modal-dialog"):
            yield Label(self.argument.description, id="modal-title")
            choices = f" (choices: {', '.join(self.argument.choices)})" if self.argument.choices else ""
            yield Label(f"{self.argument.flag}{choices}")
            yield Input(value=self.current_value, placeholder=self.argument.placeholder, id="value-input")
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel", id="cancel")
                yield Button("OK", id="ok", variant="primary")

    def on_mount(self) -> None:
        field = self.query_one("#value-input", Input)
        field.focus()
        field.cursor_position = len(field.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip() or None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(self.query_one("#value-input", Input).value.strip() or None)
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

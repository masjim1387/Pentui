from __future__ import annotations

from collections import OrderedDict

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static

from pentui.core.command_builder import build_command, display_command
from pentui.core.models import ArgumentDefinition
from pentui.core.validator import validate
from pentui.tui.screens.execution import ExecutionScreen
from pentui.tui.screens.input_modal import ValueInputModal


class ArgumentButton(Button):
    def __init__(self, argument: ArgumentDefinition, selected: bool) -> None:
        self.argument = argument
        super().__init__(self.render_label(selected), id=f"argument-{argument.id}", classes="argument")

    def render_label(self, selected: bool) -> str:
        mark = "✓" if selected else " "
        flag = self.argument.flag or ""
        return f"[{mark}] {flag:<4}  {self.argument.description}"

    def refresh_state(self, selected: bool) -> None:
        self.label = self.render_label(selected)


class NmapConfigScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back"), ("r", "run", "Run"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        tool = self.app.tool
        yield Header(show_clock=False)
        with Vertical(id="config-root"):
            yield Label(f"{tool.display_name.upper()} CONFIGURATION", id="screen-title")
            yield Static("COMMAND", classes="section-title")
            yield Static("", id="command-preview")
            with VerticalScroll(id="arguments"):
                groups: OrderedDict[str, list[ArgumentDefinition]] = OrderedDict()
                for argument in tool.arguments:
                    if argument.type != "target":
                        groups.setdefault(argument.group, []).append(argument)
                for group, arguments in groups.items():
                    yield Label(group.upper(), classes="group-title")
                    for argument in arguments:
                        yield ArgumentButton(argument, self.app.command_state.is_selected(argument))
                target_arguments = [arg for arg in tool.arguments if arg.type == "target"]
                if target_arguments:
                    yield Label("TARGET", classes="group-title")
                    yield Input(
                        value=self.app.command_state.targets[0] if self.app.command_state.targets else "",
                        placeholder=target_arguments[0].placeholder or "Host, IP, domain, or network range",
                        id="target-input",
                    )
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_preview()
        self.query_one(".argument", ArgumentButton).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "target-input":
            self.app.command_state.set_value(self.app.tool.argument("target"), event.value.strip())
            self.refresh_preview()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not isinstance(event.button, ArgumentButton):
            return
        argument = event.button.argument
        state = self.app.command_state
        if argument.type == "boolean":
            state.set_value(argument, not state.is_selected(argument))
            event.button.refresh_state(state.is_selected(argument))
            self.refresh_preview()
            return
        self.app.push_screen(
            ValueInputModal(argument, str(state.arguments.get(argument.id, ""))),
            callback=lambda value: self._set_value(argument, value),
        )

    def _set_value(self, argument: ArgumentDefinition, value: str | None) -> None:
        if value is None:
            return
        # Validate the field before selecting/storing it.
        if argument.type == "integer":
            try:
                int(value)
            except ValueError:
                self.notify(f"{argument.description} must be an integer.", severity="error")
                return
        if argument.type == "enum" and value not in argument.choices:
            self.notify(f"Choose one of: {', '.join(argument.choices)}.", severity="error")
            return
        self.app.command_state.set_value(argument, value)
        self.query_one(f"#argument-{argument.id}", ArgumentButton).refresh_state(True)
        self.refresh_preview()

    def refresh_preview(self) -> None:
        command = display_command(build_command(self.app.tool, self.app.command_state))
        self.query_one("#command-preview", Static).update(command)

    def action_run(self) -> None:
        errors = validate(self.app.tool, self.app.command_state)
        if errors:
            self.notify(f"Cannot run {self.app.tool.display_name}: " + " ".join(errors), severity="error", timeout=8)
            return
        self.app.push_screen(ExecutionScreen(build_command(self.app.tool, self.app.command_state), self.app.tool.display_name))

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_quit(self) -> None:
        self.app.exit()

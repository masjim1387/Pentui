from __future__ import annotations

from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, RichLog, Static

from pentui.core.command_builder import display_command
from pentui.core.executor import run_command


class ExecutionScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back"), ("q", "stop", "Stop")]

    def __init__(self, command: list[str], tool_name: str = "Nmap") -> None:
        super().__init__()
        self.command = command
        self.tool_name = tool_name
        self.output_worker = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="execution-root"):
            yield Label(f"{self.tool_name.upper()} — RUNNING", id="screen-title")
            yield Static("$ " + display_command(self.command), id="run-command")
            yield RichLog(id="output", wrap=True, highlight=False, markup=False)
            with Horizontal(id="execution-actions"):
                yield Button("Stop scan", id="stop-scan", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        self.output_worker = self.stream_output()

    @work(exclusive=True)
    async def stream_output(self) -> None:
        output = self.query_one("#output", RichLog)
        try:
            async for line in run_command(self.command):
                output.write(line.rstrip("\n"))
        except Exception as error:
            output.write(f"Unable to run Nmap: {error}")

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_stop(self) -> None:
        if self.output_worker is None or self.output_worker.is_cancelled:
            return
        self.output_worker.cancel()
        self.query_one("#stop-scan", Button).disabled = True
        # Return to the existing configuration screen; it retains the user's state.
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "stop-scan":
            self.action_stop()

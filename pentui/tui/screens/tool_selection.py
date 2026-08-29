from __future__ import annotations

import shutil

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from pentui.tui.screens.nmap_config import NmapConfigScreen


class ToolSelectionScreen(Screen[None]):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="tool-panel"):
                yield Label("PENTUI", id="brand")
                yield Static("SELECT TOOL", classes="section-title")
                for name in ("nmap", "sqlmap", "subfinder", "httpx", "whatweb", "ffuf"):
                    tool = self.app.tools[name]
                    status = "✓ installed" if shutil.which(tool.executable) else "✗ not installed"
                    yield Button(f"{tool.display_name}    {status}", id=name)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#nmap", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in self.app.tools:
            self.app.select_tool(event.button.id)
            if shutil.which(self.app.tool.executable) is None:
                self.notify(f"{self.app.tool.display_name} is not installed or is not on PATH.", severity="error")
                return
            self.app.push_screen(NmapConfigScreen())

    def action_quit(self) -> None:
        self.app.exit()

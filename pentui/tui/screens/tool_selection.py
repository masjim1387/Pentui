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
        installed = shutil.which(self.app.tool.executable) is not None
        status = "✓ installed" if installed else "✗ not installed"
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="tool-panel"):
                yield Label("PENTUI", id="brand")
                yield Static("SELECT TOOL", classes="section-title")
                yield Button(f"Nmap    {status}", id="nmap", variant="primary")
                yield Static("SQLMap    Coming soon", classes="coming-soon")
                yield Static("FFUF      Coming soon", classes="coming-soon")
                yield Static("Metasploit Coming soon", classes="coming-soon")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#nmap", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "nmap":
            if shutil.which(self.app.tool.executable) is None:
                self.notify("Nmap is not installed or is not on PATH.", severity="error")
                return
            self.app.push_screen(NmapConfigScreen())

    def action_quit(self) -> None:
        self.app.exit()

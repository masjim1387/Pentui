from __future__ import annotations

import shutil

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from pentui.tui.screens.nmap_config import NmapConfigScreen


class ToolSelectionScreen(Screen[None]):
    BINDINGS = [("q", "quit", "Quit")]
    TOOL_SUMMARIES = {
        "nmap": "Network discovery and service scanning",
        "sqlmap": "Web request injection testing",
        "subfinder": "Passive subdomain discovery",
        "httpx": "HTTP service probing",
        "whatweb": "Web technology identification",
        "ffuf": "Wordlist-driven content discovery",
    }

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="tool-panel"):
                yield Label("PENTUI", id="brand")
                yield Static("AUTHORIZED ASSESSMENT CONSOLE", id="brand-subtitle")
                yield Static("────────────────────────────────────────────────────────────────", id="tool-rule")
                yield Static("TOOLS  /  SELECT ONE TO CONFIGURE", id="tool-heading")
                for name in ("nmap", "sqlmap", "subfinder", "httpx", "whatweb", "ffuf"):
                    tool = self.app.tools[name]
                    installed = shutil.which(tool.executable) is not None
                    status = "READY" if installed else "MISSING"
                    label = f"{tool.display_name:<12} {self.TOOL_SUMMARIES[name]:<39} {status}"
                    state_class = "installed" if installed else "unavailable"
                    yield Button(label, id=name, classes=f"tool-button {state_class}")
                yield Static("ENTER select  ·  ↑↓ move  ·  Q quit", id="tool-help")
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

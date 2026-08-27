from __future__ import annotations

from textual.app import App

from pentui.core.models import CommandState, ToolDefinition
from pentui.tui.screens.tool_selection import ToolSelectionScreen


class PentUIApp(App[None]):
    TITLE = "PentUI"
    CSS_PATH = "pentui.tcss"

    def __init__(self, tool: ToolDefinition) -> None:
        super().__init__()
        self.tool = tool
        self.command_state = CommandState.for_tool(tool)

    def on_mount(self) -> None:
        self.push_screen(ToolSelectionScreen())

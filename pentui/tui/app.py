from __future__ import annotations

from textual.app import App

from pentui.core.models import CommandState, ToolDefinition
from pentui.tui.screens.tool_selection import ToolSelectionScreen


class PentUIApp(App[None]):
    TITLE = "PentUI"
    CSS_PATH = "pentui.tcss"

    def __init__(self, tools: list[ToolDefinition]) -> None:
        super().__init__()
        self.tools = {tool.name: tool for tool in tools}
        self.states = {tool.name: CommandState.for_tool(tool) for tool in tools}
        self.active_tool_name = "nmap"

    @property
    def tool(self) -> ToolDefinition:
        return self.tools[self.active_tool_name]

    @property
    def command_state(self) -> CommandState:
        return self.states[self.active_tool_name]

    def select_tool(self, name: str) -> None:
        self.active_tool_name = name

    def on_mount(self) -> None:
        self.push_screen(ToolSelectionScreen())

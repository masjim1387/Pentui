from pentui.core.tool_loader import load_tool_definition
from pentui.tui.app import PentUIApp


def main() -> None:
    """Load the MVP tool definition and start the terminal interface."""
    tool = load_tool_definition()
    PentUIApp(tool).run()

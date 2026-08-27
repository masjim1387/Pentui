from pentui.core.tool_loader import load_tool_definition
from pentui.tui.app import PentUIApp


def main() -> None:
    """Load available tool definitions and start the terminal interface."""
    nmap = load_tool_definition()
    definitions_dir = nmap.source_path.parent
    sqlmap = load_tool_definition(definitions_dir / "sqlmap.yaml")
    subfinder = load_tool_definition(definitions_dir / "subfinder.yaml")
    httpx = load_tool_definition(definitions_dir / "httpx.yaml")
    whatweb = load_tool_definition(definitions_dir / "whatweb.yaml")
    PentUIApp([nmap, sqlmap, subfinder, httpx, whatweb]).run()

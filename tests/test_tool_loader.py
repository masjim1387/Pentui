from pentui.core.tool_loader import load_tool_definition


def test_nmap_definition_loads() -> None:
    tool = load_tool_definition()
    assert tool.name == "nmap"
    assert tool.executable == "nmap"
    assert tool.argument("ports").requires_value
    assert tool.argument("target").required

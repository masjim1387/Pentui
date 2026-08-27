from pentui.core.command_builder import build_command
from pentui.core.models import CommandState
from pentui.core.tool_loader import load_tool_definition


def test_builds_structured_nmap_command() -> None:
    tool = load_tool_definition()
    state = CommandState.for_tool(tool)
    state.arguments.update({"service_version": True, "no_ping": True, "ports": "80,443"})
    state.targets = ["192.168.1.10"]
    assert build_command(tool, state) == ["nmap", "-sV", "-Pn", "-p", "80,443", "192.168.1.10"]


def test_deselected_boolean_is_not_emitted() -> None:
    tool = load_tool_definition()
    state = CommandState.for_tool(tool)
    state.arguments["no_ping"] = True
    assert "-Pn" in build_command(tool, state)
    state.arguments["no_ping"] = False
    assert "-Pn" not in build_command(tool, state)


def test_missing_parameter_value_never_emits_bare_flag() -> None:
    tool = load_tool_definition()
    state = CommandState.for_tool(tool)
    state.arguments["ports"] = ""
    assert "-p" not in build_command(tool, state)

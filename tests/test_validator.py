from pentui.core.models import CommandState
from pentui.core.tool_loader import load_tool_definition
from pentui.core.validator import validate


def test_empty_target_fails_validation() -> None:
    tool = load_tool_definition()
    errors = validate(tool, CommandState.for_tool(tool), check_executable=False)
    assert any("required" in error.lower() for error in errors)


def test_invalid_enum_fails_validation() -> None:
    tool = load_tool_definition()
    state = CommandState.for_tool(tool)
    state.targets = ["example.com"]
    state.arguments["timing"] = "9"
    errors = validate(tool, state, check_executable=False)
    assert any("one of" in error for error in errors)


def test_missing_executable_blocks_execution(monkeypatch) -> None:
    tool = load_tool_definition()
    state = CommandState.for_tool(tool)
    state.targets = ["example.com"]
    monkeypatch.setattr("pentui.core.validator.shutil.which", lambda _: None)
    assert any("not found" in error for error in validate(tool, state))

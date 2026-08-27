from __future__ import annotations

import shlex

from .models import CommandState, ToolDefinition


def build_command(tool: ToolDefinition, state: CommandState) -> list[str]:
    """Build an argv list in selection order; it is safe to hand to a subprocess."""
    command = [state.executable]
    definitions = {argument.id: argument for argument in tool.arguments}
    for argument_id, value in state.arguments.items():
        argument = definitions.get(argument_id)
        if argument is None or argument.type == "target":
            continue
        if argument.type == "boolean":
            if value is True:
                command.append(argument.flag or "")
        elif value not in (None, ""):
            command.extend([argument.flag or "", str(value)])
    command.extend(state.targets)
    return command


def display_command(command: list[str]) -> str:
    return shlex.join(command)

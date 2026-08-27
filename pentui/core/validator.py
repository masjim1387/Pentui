from __future__ import annotations

import shutil
from pathlib import Path

from .models import CommandState, ToolDefinition


def validate(tool: ToolDefinition, state: CommandState, *, check_executable: bool = True) -> list[str]:
    errors: list[str] = []
    if check_executable and shutil.which(state.executable) is None:
        errors.append(f"{tool.display_name} executable was not found on PATH.")

    for argument in tool.arguments:
        value = state.targets[0] if argument.type == "target" and state.targets else None if argument.type == "target" else state.arguments.get(argument.id)
        if argument.required and value in (None, ""):
            errors.append(f"{argument.description} is required.")
            continue
        if value in (None, ""):
            continue
        if argument.type == "integer":
            try:
                int(str(value))
            except ValueError:
                errors.append(f"{argument.description} must be an integer.")
        elif argument.type == "enum" and str(value) not in argument.choices:
            errors.append(f"{argument.description} must be one of: {', '.join(argument.choices)}.")
        elif argument.type == "filepath" and not str(value).strip():
            errors.append(f"{argument.description} cannot be empty.")
        elif argument.type == "target" and not _valid_target(str(value)):
            errors.append("Target must be a host, IP address, domain, or network range.")
    return errors


def _valid_target(value: str) -> bool:
    # MVP validation intentionally permits hostnames and CIDR forms without DNS lookup.
    return bool(value.strip()) and not any(char.isspace() for char in value)

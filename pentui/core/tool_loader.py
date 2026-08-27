from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import ArgumentDefinition, ToolDefinition, VALUE_TYPES


DEFAULT_DEFINITION = Path(__file__).resolve().parents[2] / "tools" / "nmap.yaml"


def load_tool_definition(path: Path | str = DEFAULT_DEFINITION) -> ToolDefinition:
    path = Path(path)
    with path.open(encoding="utf-8") as definition_file:
        data: dict[str, Any] = yaml.safe_load(definition_file)
    if not data or not all(key in data for key in ("name", "display_name", "executable", "arguments")):
        raise ValueError(f"Invalid tool definition: {path}")

    arguments = []
    for raw in data["arguments"]:
        argument_type = raw.get("type")
        if argument_type not in VALUE_TYPES:
            raise ValueError(f"Unsupported argument type {argument_type!r} in {path}")
        if not raw.get("id") or not raw.get("description"):
            raise ValueError(f"Each argument needs id and description in {path}")
        if argument_type != "target" and not raw.get("flag"):
            raise ValueError(f"Argument {raw['id']} needs a flag in {path}")
        arguments.append(ArgumentDefinition(
            id=raw["id"], type=argument_type, description=raw["description"],
            flag=raw.get("flag"), required=raw.get("required", False),
            default=raw.get("default"), choices=[str(value) for value in raw.get("choices", [])],
            placeholder=raw.get("placeholder", ""), group=raw.get("group", "General"),
        ))
    return ToolDefinition(data["name"], data["display_name"], data["executable"], arguments, path)

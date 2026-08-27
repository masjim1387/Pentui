from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


VALUE_TYPES = {"boolean", "string", "integer", "enum", "filepath", "target"}


@dataclass(frozen=True)
class ArgumentDefinition:
    id: str
    type: str
    description: str
    flag: str | None = None
    required: bool = False
    default: Any = None
    choices: list[str] = field(default_factory=list)
    placeholder: str = ""
    group: str = "General"

    @property
    def requires_value(self) -> bool:
        return self.type not in {"boolean", "target"}


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    display_name: str
    executable: str
    arguments: list[ArgumentDefinition]
    source_path: Path | None = None

    def argument(self, argument_id: str) -> ArgumentDefinition:
        return next(arg for arg in self.arguments if arg.id == argument_id)


@dataclass
class CommandState:
    """Structured configuration; never a shell command string."""

    executable: str
    arguments: dict[str, Any] = field(default_factory=dict)
    targets: list[str] = field(default_factory=list)

    @classmethod
    def for_tool(cls, tool: ToolDefinition) -> "CommandState":
        values = {
            arg.id: arg.default
            for arg in tool.arguments
            if arg.default is not None and arg.type != "target"
        }
        return cls(executable=tool.executable, arguments=values)

    def is_selected(self, argument: ArgumentDefinition) -> bool:
        if argument.type == "target":
            return bool(self.targets)
        value = self.arguments.get(argument.id)
        return value is True if argument.type == "boolean" else value not in (None, "")

    def set_value(self, argument: ArgumentDefinition, value: Any) -> None:
        if argument.type == "target":
            self.targets = [value] if value else []
        else:
            self.arguments[argument.id] = value

    def clear(self, argument: ArgumentDefinition) -> None:
        if argument.type == "target":
            self.targets = []
        else:
            self.arguments.pop(argument.id, None)

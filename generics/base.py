from abc import ABC, abstractmethod
from typing import Any

CommandOptionName = str
CommandOptionValue = str | int | float

ArgumentValues = dict[CommandOptionName, CommandOptionValue]


class Command(ABC):
    def __init__(self, args: ArgumentValues):
        self.args = args

    @classmethod
    def parse_options(cls, command_parts: list[str]) -> dict[str, Any]:
        """
        Default option parsing.
        Override per command if needed.
        """
        options: dict[str, Any] = {}

        for part in command_parts[1:]:
            if "=" not in part:
                raise ValueError(f"Invalid option format: '{part}'. Expected key=value")
            key, value = part.split("=", 1)
            options[key] = value

        return options


class CommandHandler(ABC):

    """Command event handler"""
    @abstractmethod
    def handle(self, args: Command | None):
        pass

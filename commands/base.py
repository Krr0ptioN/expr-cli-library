from abc import ABC, abstractmethod
from dataclasses import dataclass

CommandOptionName = str
CommandOptionValue = str | int | float

ArgumentValues = dict[CommandOptionName, CommandOptionValue]


@dataclass
class Command(ABC):

    """Command Event

    Attributes:
        id: [TODO:attribute]
        command_name: [TODO:attribute]
        command_options: [TODO:attribute]
    """
    name: str
    args: ArgumentValues

    def __init__(self, args: ArgumentValues):
        self.args = args

    @staticmethod
    def parse_options(command_parts: list[str]):
        return {
            tuple(part.split("="))
            for part in command_parts
        }


class CommandHandler(ABC):

    """Command event handler"""
    @abstractmethod
    def handle(self, args: Command | None):
        pass

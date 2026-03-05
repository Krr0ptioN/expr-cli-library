from abc import ABC, abstractmethod

CommandOptionName = str
CommandOptionValue = str | int | float


class Command(ABC):

    """Command Event

    Attributes:
        id: [TODO:attribute]
        command_name: [TODO:attribute]
        command_options: [TODO:attribute]
    """
    id: str
    command_name: str
    command_options: dict[CommandOptionName, CommandOptionValue]

class CommandHandler(ABC):

    """Command event handler"""

    def __parseOptions(self):
        pass

    @abstractmethod
    def execute(self, cmd: Command):
        pass

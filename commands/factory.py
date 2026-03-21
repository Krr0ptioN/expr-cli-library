
from commands import CreateTaskCommand, Command


class CommandFactory:
    """
    CommandFactory is responsible for creating command instances
    based on the command name and options provided.

    Attributes:
        __commands: A mapping of command names to their corresponding command classes.
    """
    __commands: dict[str, type[Command]] = {
        "create": CreateTaskCommand,
    }

    @staticmethod
    def get(command_name: str, command_options) -> Command:
        return CommandFactory.__commands[command_name](command_options)

from typing import Callable
from commands import CommandHandler, Command

HandlerFactory = Callable[[], CommandHandler]

class CommandBus:
    """
    CommandBus is responsible for managing the registration
    and execution of commands.
    """

    def __init__(self) -> None:
        self._command_handlers: dict[type[Command], HandlerFactory] = {}

    def register(
        self,
        command_type: type[Command],
        handler_factory: HandlerFactory,
    ) -> None:
        """Registers a command handler for a specific command type.

        Args:
            command_type: The type of command that the handler will manage.
            handler_factory: A factory function that creates an instance of the command handler.
        """
        self._command_handlers[command_type] = handler_factory

    def execute(self, command: Command) -> None:
        """Constructs and executes the appropriate command handler for the given command.

        Args:
            command: Command to be executed.

        Raises:
            ValueError: Command type is not registered in the command bus.
        """
        handler = self._command_handlers.get(type(command))
        if handler is None:
            raise ValueError(
                f"No handler registered for command type: {type(command).__name__}"
            )

        handler.handle(command)


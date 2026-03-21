
from .base import Command, CommandHandler


class CommandHandlerRegistry:
    _handlers: dict[type[Command], type[CommandHandler]] = {}

    @classmethod
    def register(cls, command_type: type[Command]):
        """Registers a command handler for a specific command type.

        Args:
            command_type: The type of command that the handler will manage.
        Returns:
            A decorator that registers the handler for the specified command type.

        Raises:
            ValueError: If a handler is already registered for the given command type.
        """
        def decorator(handler_type: type[CommandHandler]) -> type[CommandHandler]:
            if command_type in cls._handlers:
                raise ValueError(
                    f"Handler already registered for {command_type.__name__}"
                )
            cls._handlers[command_type] = handler_type
            return handler_type
        return decorator

    @classmethod
    def get_handler(cls, command_type: type[Command]) -> type[CommandHandler]:
        """
        Retrieves the command handler class associated with a specific command type.

        Args:
            command_type: The type of command for which to retrieve the handler.

        Returns:
            The command handler class associated with the specified command type.

        Raises:
            ValueError: If no handler is registered for the given command type.
        """
        try:
            return cls._handlers[command_type]
        except KeyError as e:
            raise ValueError(
                f"No handler registered for {command_type.__name__}"
            ) from e


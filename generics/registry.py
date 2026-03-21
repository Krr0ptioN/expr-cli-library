from __future__ import annotations

from .base import Command, CommandHandler


class CommandRegistry:
    _commands: dict[str, type[Command]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(command_cls: type[Command]) -> type[Command]:
            normalized = name.strip().lower()

            if not normalized:
                raise ValueError("Command name cannot be empty")

            if normalized in cls._commands:
                raise ValueError(f"Command '{normalized}' is already registered")

            cls._commands[normalized] = command_cls
            return command_cls

        return decorator

    @classmethod
    def get_command(cls, name: str) -> type[Command]:
        normalized = name.strip().lower()

        try:
            return cls._commands[normalized]
        except KeyError as e:
            raise ValueError(f"Unknown command: '{name}'") from e

    @classmethod
    def all_commands(cls) -> dict[str, type[Command]]:
        return dict(cls._commands)


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

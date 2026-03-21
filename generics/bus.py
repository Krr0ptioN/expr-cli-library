from .base import Command
from .registry import CommandHandlerRegistry
from .handler_factory import HandlerFactory


class CommandBus:
    def __init__(self, handler_factory: HandlerFactory) -> None:
        self.handler_factory = handler_factory

    def execute(self, command: Command) -> None:
        """
        CommandBus is responsible for executing generics by finding the
        appropriate handler and invoking it.

        Args:
            command: The command to be executed.
        """
        handler_cls = CommandHandlerRegistry.get_handler(type(command))
        handler = self.handler_factory.create(handler_cls)
        handler.handle(command)

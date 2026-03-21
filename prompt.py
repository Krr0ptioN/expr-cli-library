from bus import CommandBus
from commands import CommandFactory, Command


class CommandPrompter:

    """
    CommandPrompt is responsible for handling user input and executing
    commands related to task management.

    Attributes:
        task_repo: CommandPrompt uses this to execute commands that manipulate tasks.
    """

    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus

    def __parse_command_input(self, command_input: str):
        command_parts = command_input.split(" ")
        command_name = command_parts[0]

        command_arguments = Command.parse_options(command_parts)

        return command_name, command_arguments

    # TODO: Gracefull Exit
    # a way to exit the loop gracefully, e.g.,  by typing "exit" or "quit".

    # TODO: Feedback and Error Handling
    # Error handling for invalid commands or options.

    # TODO: Help and Documentation
    # A help command to list available commands and their usage.

    # TODO: Command History and Auto-completion
    # command history and auto-completion for a better user experience.

    # TODO: Clean Output
    # A way to display command output or results to the user,
    # E.g., by printing to the console or using a more sophisticated UI.

    def prompt_loop(self):
        """
        Starts the command prompt loop, continuously waiting for user
        input and executing commands.
        """

        while True:
            command_input = input("[Home]-> ")

            (name, options) = self.__parse_command_input(command_input)

            command = CommandFactory.get(name, options)
            self.command_bus.execute(command)

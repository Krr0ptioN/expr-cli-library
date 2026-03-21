import os
import subprocess
from generics.bus import CommandBus
from generics import Command, CommandRegistry


class CommandPrompter:

    """
    CommandPrompt is responsible for handling user input and executing
    generics related to task management.

    Attributes:
        task_repo: CommandPrompt uses this to execute generics that manipulate tasks.
    """

    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus

    def __parse_command_input(self, command_input: str):
        command_parts = command_input.split(" ")
        command_name = command_parts[0]

        command_arguments = Command.parse_options(command_parts)

        return command_name, command_arguments

    def _clear_terminal(self) -> None:
        subprocess.call("cls" if os.name == "nt" else "clear")

    def prompt_loop(self):
        while True:
            # try:
            command_input = input("[Home]-> ").strip()

            if not command_input:
                continue

            if command_input == "clear":
                self._clear_terminal()
                continue

            if command_input.lower() in {"exit", "quit"}:
                print("Exiting...")
                break

            command_name, options = self.__parse_command_input(command_input)
            command_cls = CommandRegistry.get_command(command_name)
            command = command_cls(options)
            self.command_bus.execute(command)

            # except Exception as exc:
            #     print(f"Error: {exc}")


    # TODO: Gracefull Exit
    # a way to exit the loop gracefully, e.g.,  by typing "exit" or "quit".

    # TODO: Feedback and Error Handling
    # Error handling for invalid generics or options.

    # TODO: Help and Documentation
    # A help command to list available generics and their usage.

    # TODO: Command History and Auto-completion
    # command history and auto-completion for a better user experience.

    # TODO: Clean Output
    # A way to display command output or results to the user,
    # E.g., by printing to the console or using a more sophisticated UI.

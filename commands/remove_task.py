from generics import (
    Command,
    CommandHandler,
    CommandHandlerRegistry,
    CommandRegistry)

from repositories import TaskRepository

@CommandRegistry.register("remove")
class RemoveTaskCommand(Command):
    def __init__(self, args: Command.args):
        super().__init__(args)

CommandArgument = tuple[str, str]

@CommandHandlerRegistry.register(RemoveTaskCommand)
class RemoveTaskCommandHandler(CommandHandler):
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def handle(self, args: list[CommandArgument]):

        # TODO: Handle args and options
        # - If an ID is passed as an arg, skip the prompt and remove directly.

        task_id = input("Enter task ID to remove: ")
        removed = self.repo.delete(task_id)

        if removed:
            print(f"\nTask [{task_id}] removed successfully.")
        else:
            print(f"\nNo task found with ID [{task_id}].")

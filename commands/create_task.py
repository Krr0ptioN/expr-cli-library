from generics import (
    Command,
    CommandHandler,
    CommandHandlerRegistry,
    CommandRegistry
)

from entities.task import TaskEntity
from repositories import TaskRepository


@CommandRegistry.register("create")
class CreateTaskCommand(Command):
    def __init__(self, args: Command.args):
        super().__init__(args)


CommandArgument = tuple[str, str]


@CommandHandlerRegistry.register(CreateTaskCommand)
class CreateTaskCommandHandler(CommandHandler):
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def handle(self, args: list[CommandArgument]):

        # TODO: Handle args and options
        # - Theese can be used to create tasks with specific titles and
        #   descriptions without prompting the user for input.
        # - If the args are provided, use them to create the task. If not,
        #   prompt the user for input as currently implemented.

        title = input("Enter task's title: ")
        descrption = input("Enter task's descrption: ")
        task = TaskEntity(title, descrption)
        self.repo.insert(task)

        print(f"\n[{task.status.value}] {task.title}: {task.description}")

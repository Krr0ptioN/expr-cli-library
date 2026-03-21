from commands.registry import CommandHandlerRegistry
from entities.task import TaskEntity
from repositories import TaskRepository
from .base import CommandHandler, Command


class ListTaskCommand(Command):
    name = "list"

    def __init__(self, args: Command.args):
        super().__init__(args)


CommandArgument = tuple[str, str]


@CommandHandlerRegistry.register(ListTaskCommand)
class ListTaskCommandHandler(CommandHandler):
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def __tasks_table(self, tasks: list[TaskEntity]):
        # column header
        print(f"{'ID':<10} {'Status':<10} {'Title':<20} {'Description':<30}")
        print("-" * 70)

        for task in tasks:
            print(f"{task.id:<10} {task.status.value:<10} {task.title:<20} {task.description:<30}")

    def handle(self, args: list[CommandArgument]):

        tasks = self.repo.list()
        self.__tasks_table(tasks)


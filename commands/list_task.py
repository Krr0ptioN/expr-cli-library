from generics import (
    CommandHandlerRegistry,
    CommandRegistry,
    CommandHandler,
    Command
)
from entities.task import TaskEntity
from repositories import TaskRepository


@CommandRegistry.register("list")
class ListTaskCommand(Command):
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

        # TODO: query options
        # - Theese can be used to filter tasks by status, title, or other attributes
        # - AND operator can be used to combine multiple filters, e.g., "list status=completed title=Report" to list all completed tasks with "Report" in the title.
        tasks = self.repo.list()
        self.__tasks_table(tasks)


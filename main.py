"""
This is the main entry point for the application. 
It initializes the necessary components and starts the command prompt loop.
"""


from commands import (
    CreateTaskCommand,
    CreateTaskCommandHandler,
    ListTaskCommand,
    ListTaskCommandHandler
)
from mappers.task import TaskEntityMapper
from repositories.task_repository_store import TaskRepositoryStore
from store import JsonTaskStore
from prompt import CommandBus, CommandPrompter


def main():
    store = JsonTaskStore('./db.json')
    task_repository = TaskRepositoryStore(store, TaskEntityMapper())

    bus = CommandBus()

    bus.register(
        CreateTaskCommand,
        CreateTaskCommandHandler(repo=task_repository)
    )


    bus.register(
        ListTaskCommand,
        ListTaskCommandHandler(repo=task_repository)
    )
    prompter = CommandPrompter(bus)

    prompter.prompt_loop()


if __name__ == "__main__":
    main()

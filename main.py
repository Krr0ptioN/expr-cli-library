"""
This is the main entry point for the application.
It initializes the necessary components and starts the command prompt loop.
"""

from generics import HandlerFactory, CommandBus
from mappers.task import TaskEntityMapper
from repositories.task_repository_store import TaskRepositoryStore
from store import JsonTaskStore
from prompt import CommandPrompter

import commands

def main():
    store = JsonTaskStore('./db.json')
    task_repository = TaskRepositoryStore(store, TaskEntityMapper())

    handler_factory = HandlerFactory(task_repository)
    bus = CommandBus(handler_factory)
    prompter = CommandPrompter(bus)

    prompter.prompt_loop()


if __name__ == "__main__":
    main()

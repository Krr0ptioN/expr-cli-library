

from entities import TaskEntity


class Store:
    file_storage = ""
    __tasks = {}

    def __init__(self, file_backup: str):
        self.file_storage = file_backup

    def save(self):
        pass


    def addTask(self, newTask: TaskEntity):
        self.__tasks[newTask.id] = newTask

    @property
    def tasks(self):
        return self.__tasks.values()

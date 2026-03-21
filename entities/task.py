from enum import Enum

from .base import Entity


class TaskStatus(Enum):
    """TaskStatus represents the status of a task in the system

    Attributes:
        TODO: The task is yet to be started
        DOING: The task is currently being worked on
        DONE: The task is completed
    """
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskEntity(Entity):
    """TaskEntity represents a task in the system

    Attributes:
        title: The title of the task
        description: The description of the task
        status: The status of the task
        id: The unique identifier of the task
    """
    title: str
    description: str
    status: TaskStatus
    id: str

    def __init__(self, title: str, descrption: str = ""):
        self.title = title
        self.description = descrption
        self.status = TaskStatus.TODO
        self.id = Entity.randomHashId()

    def progress(self):
        """Progress the task to the next status"""
        if self.status == TaskStatus.TODO:
            self.status = TaskStatus.DOING
        elif self.status == TaskStatus.DOING:
            self.status = TaskStatus.DONE


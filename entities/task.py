from enum import Enum

from .base import Entity


class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskEntity(Entity):
    title: str
    description: str
    status: TaskStatus
    id: str

    def __init__(self, title: str, descrption: str = ""):
        self.title = title
        self.description = descrption
        self.status = TaskStatus.TODO
        self.id = Entity.randomHashId()

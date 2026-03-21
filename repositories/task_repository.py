
from abc import ABC, abstractmethod

from entities import TaskEntity


class TaskRepository(ABC):
    @abstractmethod
    def insert(self, task: TaskEntity):
        pass

    @abstractmethod
    def get(self, task_id: str):
        pass

    @abstractmethod
    def update(self, task_id: str, updated_data: dict):
        pass

    @abstractmethod
    def delete(self, task_id: str):
        pass


    @abstractmethod
    def list(self):
        pass

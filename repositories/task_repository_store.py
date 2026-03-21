from entities import TaskEntity
from mappers.task import TaskEntityMapper
from repositories.task_repository import TaskRepository


class TaskRepositoryStore(TaskRepository):

    def __init__(self, store, mapper: TaskEntityMapper):
        self.store = store
        self.mapper = mapper

    def insert(self, task: TaskEntity):
        self.store.add_task(
            self.mapper.to_dict(task)
        )

    def get(self, task_id):
        # Code to retrieve a task by its ID from the database
        return self.store.tasks[task_id]

    def update(self, task_id, updated_data):
        self.store.tasks[task_id] = updated_data

    def delete(self, task_id):
        self.store.delete_task(task_id)

    def list(self):
        return self.store.list_tasks()

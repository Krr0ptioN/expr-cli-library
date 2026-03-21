
from entities import TaskEntity


class TaskEntityMapper:

    @staticmethod
    def to_entity(task_dict: dict) -> TaskEntity:
        """Convert a dictionary to a TaskEntity

        Args:
            task_dict: dict: The dictionary containing task information
        Returns:
            TaskEntity: The task entity created from the dictionary
        """
        task = TaskEntity(task_dict["title"], task_dict["description"])
        return task

    @staticmethod
    def to_dict(task: TaskEntity) -> dict:
        """Convert a TaskEntity to a dictionary

        Args:
            task: TaskEntity: The task entity to convert to a dictionary
        Returns:
            dict: A dictionary representation of the task entity
        """
        return {
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "id": task.id
        }

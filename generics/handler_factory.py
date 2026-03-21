from __future__ import annotations


class HandlerFactory:
    def __init__(self, task_repository) -> None:
        self.task_repository = task_repository

    def create(self, handler_cls):
        return handler_cls(repo=self.task_repository)

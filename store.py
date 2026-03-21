from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any

from mappers.task import TaskEntityMapper


class StoreError(Exception):
    """Base exception for store failures."""


class StoreCorruptedError(StoreError):
    """Raised when persisted JSON is invalid or has an unexpected structure."""


class TaskNotFoundError(StoreError):
    """Raised when a requested task does not exist."""


class JsonTaskStore:
    """JSON-backed local task store with atomic persistence and thread safety.

    Responsibilities:
        - maintain an in-memory index of tasks by ID
        - load/store tasks from a JSON file
        - serialize/deserialize via TaskEntityMapper
        - provide a repository-like API for CRUD operations

    Persistence format:
        {
            "tasks": [
                { ...task dict... },
                { ...task dict... }
            ]
        }
    """

    def __init__(self, file_path: str | Path):
        self._file_path = Path(file_path)
        self._lock = threading.RLock()
        self._tasks: dict[str, Any] = {}

        self._ensure_parent_dir()
        self._load()

    # -------------------------
    # Public API
    # -------------------------

    def add_task(self, task: dict[str, Any] | Any) -> None:
        """Add a new task.

        Accepts either a plain task dict or a TaskEntity-like object that
        TaskEntityMapper can serialize.
        """
        with self._lock:
            entity = self._normalize_to_entity(task)
            task_id = self._extract_task_id(entity)

            if task_id in self._tasks:
                raise ValueError(f"Task with id '{task_id}' already exists")

            self._tasks[task_id] = entity
            self._flush()

    def get_task(self, task_id: str) -> Any | None:
        with self._lock:
            return self._tasks.get(task_id)

    def require_task(self, task_id: str) -> Any:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(f"Task '{task_id}' not found")
            return task

    def list_tasks(self) -> list[Any]:
        with self._lock:
            return list(self._tasks.values())

    def update_task(self, task_id: str, updated_data: dict[str, Any]) -> Any:
        """Patch an existing task.

        This assumes the entity can be converted to/from dict through the mapper.
        """
        with self._lock:
            current = self._tasks.get(task_id)
            if current is None:
                raise TaskNotFoundError(f"Task '{task_id}' not found")

            current_dict = self._entity_to_dict(current)
            current_dict.update(updated_data)

            updated_entity = TaskEntityMapper.to_entity(current_dict)
            self._tasks[task_id] = updated_entity
            self._flush()
            return updated_entity

    def replace_task(self, task_id: str, task: dict[str, Any] | Any) -> None:
        """Replace a task entirely."""
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(f"Task '{task_id}' not found")

            entity = self._normalize_to_entity(task)
            normalized_id = self._extract_task_id(entity)
            if normalized_id != task_id:
                raise ValueError(
                    f"Replacement task id '{normalized_id}' does not match target id '{task_id}'"
                )

            self._tasks[task_id] = entity
            self._flush()

    def delete_task(self, task_id: str) -> None:
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(f"Task '{task_id}' not found")

            del self._tasks[task_id]
            self._flush()

    def exists(self, task_id: str) -> bool:
        with self._lock:
            return task_id in self._tasks

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._flush()

    def reload(self) -> None:
        with self._lock:
            self._load()

    @property
    def tasks(self) -> tuple[Any, ...]:
        with self._lock:
            return tuple(self._tasks)

    # -------------------------
    # Internal loading/saving
    # -------------------------

    def _ensure_parent_dir(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        """Load state from disk.

        Creates the file if it does not exist.
        """
        if not self._file_path.exists():
            self._tasks = {}
            self._flush()
            return

        try:
            raw = self._file_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise StoreError(f"Failed to read store file '{self._file_path}'") from exc

        if raw == "":
            self._tasks = {}
            self._flush()
            return

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise StoreCorruptedError(
                f"Store file '{self._file_path}' contains invalid JSON"
            ) from exc

        if not isinstance(data, dict):
            raise StoreCorruptedError("Store root must be a JSON object")

        raw_tasks = data.get("tasks")
        if not isinstance(raw_tasks, list):
            raise StoreCorruptedError("Store must contain a 'tasks' list")

        loaded: dict[str, Any] = {}
        for item in raw_tasks:
            if not isinstance(item, dict):
                raise StoreCorruptedError("Each task must be a JSON object")

            entity = TaskEntityMapper.to_entity(item)
            task_id = self._extract_task_id(entity)

            if task_id in loaded:
                raise StoreCorruptedError(f"Duplicate task id detected: '{task_id}'")

            loaded[task_id] = entity

        self._tasks = loaded

    def _flush(self) -> None:
        """Persist current state using atomic write-replace."""
        payload = {
            "tasks": [self._entity_to_dict(task) for task in self._tasks.values()]
        }

        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )

        self._atomic_write_text(serialized)

    def _atomic_write_text(self, content: str) -> None:
        """Write content atomically to avoid file corruption on partial writes."""
        directory = self._file_path.parent

        fd, tmp_path = tempfile.mkstemp(
            dir=directory,
            prefix=f"{self._file_path.name}.",
            suffix=".tmp",
            text=True,
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
                tmp_file.write(content)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            os.replace(tmp_path, self._file_path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    # -------------------------
    # Serialization helpers
    # -------------------------

    def _normalize_to_entity(self, task: dict[str, Any] | Any) -> Any:
        if isinstance(task, dict):
            return TaskEntityMapper.to_entity(task)
        return task

    def _entity_to_dict(self, entity: Any) -> dict[str, Any]:
        """Convert entity to dict for JSON persistence.
        """
        if hasattr(TaskEntityMapper, "to_dict"):
            return TaskEntityMapper.to_dict(entity)

        if isinstance(entity, dict):
            return entity

        raise TypeError(
            "TaskEntityMapper.to_dict(entity) is required to serialize task entities"
        )

    def _extract_task_id(self, entity: Any) -> str:
        if isinstance(entity, dict):
            task_id = entity.get("id")
        else:
            task_id = getattr(entity, "id", None)

        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("Task must have a non-empty string 'id'")

        return task_id

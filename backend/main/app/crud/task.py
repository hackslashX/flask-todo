""" CRUD Operations for Tasks """

from copy import deepcopy
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.db.base import Tag, Task, TaskTag
from sqlalchemy.orm import Session

TaskCreate = TypeVar("TaskCreate", bound=dict)
TaskUpdate = TypeVar("TaskUpdate", bound=dict)


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_by_id(self, db: Session, *, id: int, user_id: int) -> Optional[Task]:
        """Get a single object by id

        Args:
            db (Session): The database session.
            id (Any): The id of the object.
            user_id (int): The id of the user.

        Returns:
            Optional[ModelType]: The object if found, else None.
        """
        return db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()

    def get_multi(self, db: Session, *, user_id: int) -> List[Optional[Task]]:
        """Get all tasks for a user

        Args:
            db (Session): The database session.
            user_id (int): The id of the user.

        Returns:
            List[Optional[Task]]: The list of tasks.
        """
        return db.query(Task).filter(Task.user_id == user_id).all()

    def get_multi_by_status(
        self, db: Session, *, status: str, user_id: int
    ) -> List[Optional[Task]]:
        """Get all tasks for a user by status

        Args:
            db (Session): The database session.
            status (str): The status of the task.
            user_id (int): The id of the user.

        Returns:
            List[Optional[Task]]: The list of tasks.
        """
        return (
            db.query(Task).filter(Task.status == status, Task.user_id == user_id).all()
        )

    def get_multi_by_tag(
        self, db: Session, *, tag_id: int, user_id: int
    ) -> List[Optional[Task]]:
        """Get all tasks for a user by tag

        Args:
            db (Session): The database session.
            tag_id (int): The id of the tag.
            user_id (int): The id of the user.

        Returns:
            List[Optional[Task]]: The list of tasks.
        """
        return (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .join(TaskTag)
            .filter(TaskTag.tag_id == tag_id)
            .join(Tag)
            .filter(Tag.user_id == user_id, Tag.id == tag_id)
            .all()
        )

    def remove(self, db: Session, *, id: int, user_id: int) -> Task:
        """Remove a task

        Args:
            db (Session): The database session.
            id (int): The id of the task.
            user_id (int): The id of the user.

        Returns:
            Task: The task that was removed.
        """
        obj = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj


task = CRUDTask(Task)

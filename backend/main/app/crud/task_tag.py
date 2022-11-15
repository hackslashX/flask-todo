""" CRUD operations for Task Tags. """

from copy import deepcopy
from typing import List, TypeVar

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.db.base import TaskTag
from sqlalchemy.orm import Session

TaskTagCreate = TypeVar("TaskTagCreate", bound=dict)
TaskTagUpdate = TypeVar("TaskTagUpdate", bound=dict)


class CRUDTaskTag(CRUDBase[TaskTag, TaskTagCreate, TaskTagUpdate]):
    def create_multi(
        self, db: Session, *, obj_in: List[int], task_id: int
    ) -> List[TaskTag]:
        """Create multiple task tags.

        Args:
            db (Session): The database session.
            obj_in (List[int]): The list of tag ids.
            task_id (int): The id of the task.

        Returns:
            List[TaskTag]: The list of task tags.
        """
        if not obj_in:
            return []
        obj_in = [{"tag_id": tag_id, "task_id": task_id} for tag_id in obj_in]
        db_objs = [self.model(**obj_in_item) for obj_in_item in obj_in]
        db.bulk_save_objects(db_objs)
        db.commit()

    def get_multi(self, db: Session, *, task_id: int) -> List[TaskTag]:
        """Get all task tags for a task.

        Args:
            db (Session): The database session.
            task_id (int): The id of the task.

        Returns:
            List[TaskTag]: The list of task tags.
        """
        return db.query(TaskTag).filter(TaskTag.task_id == task_id).all()

    def delete_multi(
        self, db: Session, *, task_id: int, tag_ids: List[int]
    ) -> List[TaskTag]:
        """Delete multiple task tags.

        Args:
            db (Session): The database session.
            task_id (int): The id of the task.
            tag_ids (List[int]): The list of tag ids.

        Returns:
            List[TaskTag]: The list of task tags.
        """
        db.query(TaskTag).filter(
            TaskTag.task_id == task_id, TaskTag.tag_id.in_(tag_ids)
        ).delete(synchronize_session=False)
        db.commit()


task_tag = CRUDTaskTag(TaskTag)

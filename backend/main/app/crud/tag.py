""" CRUD operations for Tags. """

from copy import deepcopy
from typing import List, Optional, TypeVar

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.db.base import Tag
from sqlalchemy.orm import Session

TagCreate = TypeVar("TagCreate", bound=dict)
TagUpdate = TypeVar("TagUpdate", bound=dict)


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def get(self, db: Session, id: int, user_id: int) -> Optional[Tag]:
        """Get a single object by id

        Args:
            db (Session): The database session.
            id (Any): The id of the object.
            user_id (int): The id of the user.

        Returns:
            Optional[ModelType]: The object if found, else None.
        """
        return db.query(Tag).filter(Tag.id == id, Tag.user_id == user_id).first()

    def get_by_name(self, db: Session, *, name: str, user_id: int) -> Optional[Tag]:
        """Get a single object by name

        Args:
            db (Session): The database session.
            name (str): The name of the object.
            user_id (int): The id of the user.

        Returns:
            Optional[ModelType]: The object if found, else None.
        """
        return db.query(Tag).filter(Tag.name == name, Tag.user_id == user_id).first()

    def get_multi(self, db: Session, *, user_id: int) -> List[Optional[Tag]]:
        """Get all tags for a user

        Args:
            db (Session): The database session.
            user_id (int): The id of the user.

        Returns:
            List[Optional[Tag]]: The list of tags.
        """
        return db.query(Tag).filter(Tag.user_id == user_id).all()

    def get_multi_id(
        self, db: Session, *, ids: List[int], user_id: int
    ) -> List[Optional[Tag]]:
        """Get all tags for a user by id

        Args:
            db (Session): The database session.
            ids (List[int]): The list of ids.
            user_id (int): The id of the user.

        Returns:
            List[Optional[Tag]]: The list of tags.
        """
        return db.query(Tag).filter(Tag.id.in_(ids), Tag.user_id == user_id).all()

    def remove(self, db: Session, *, id: int, user_id: int) -> Tag:
        """Remove a tag

        Args:
            db (Session): The database session.
            id (int): The id of the tag.
            user_id (int): The id of the user.

        Returns:
            Tag: The removed tag.
        """
        obj = db.query(Tag).filter(Tag.id == id, Tag.user_id == user_id).first()
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj


tag = CRUDTag(Tag)

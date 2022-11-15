""" CRUD Operations for User. """

from copy import deepcopy
from typing import Any, Dict, Optional, TypeVar, Union

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.db.base import User
from sqlalchemy.orm import Session

UserCreate = TypeVar("UserCreate", bound=dict)
UserUpdate = TypeVar("UserUpdate", bound=dict)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user.

        Args:
            db (Session): The database session.
            obj_in (UserCreate): The user object.

        Returns:
            User: The created user.
        """
        create_data = deepcopy(obj_in)
        create_data["hashed_password"] = get_password_hash(create_data.pop("password"))
        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update a user.

        Args:
            db (Session): The database session.
            db_obj (User): The user object.
            obj_in (Union[UserUpdate, Dict[str, Any]]): The user object.

        Returns:
            User: The updated user.
        """
        update_data = deepcopy(obj_in)
        if update_data.get("password"):
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            db (Session): The database session.
            email (str): The user's email.

        Returns:
            Optional[User]: The user object if found, else None.
        """
        return db.query(User).filter(User.email == email).first()


user = CRUDUser(User)

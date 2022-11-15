""" Base CRUD class """

from typing import Any, Generic, List, Optional, Type, TypeVar

from app.db.base_class import Base
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=dict)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=dict)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD class"""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single object by id

        Args:
            db (Session): The database session.
            id (Any): The id of the object.

        Returns:
            Optional[ModelType]: The object if found, else None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[ModelType]:
        """Get multiple objects

        Args:
            db (Session): The database session.
            skip (int, optional): The number of objects to skip. Defaults to 0.
            limit (int, optional): The number of objects to return. Defaults to 5000.

        Returns:
            List[ModelType]: The list of objects.
        """
        return (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object

        Args:
            db (Session): The database session.
            obj_in (CreateSchemaType): The object to create.

        Returns:
            ModelType: The created object.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update an object

        Args:
            db (Session): The database session.
            db_obj (ModelType): The object to update.
            obj_in (UpdateSchemaType): The updated object.

        Returns:
            ModelType: The updated object.
        """
        obj_data = db_obj.dict()
        for field in obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove an object

        Args:
            db (Session): The database session.
            id (int): The id of the object.

        Returns:
            ModelType: The removed object.
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

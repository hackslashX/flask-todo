""" Authorization Functionality """

from typing import Optional

from app import crud
from app.core.security import verify_password
from app.db.base import User
from sqlalchemy.orm import Session


def authenticate(email: str, password: str, db: Session) -> Optional[User]:
    """Authenticate a user.

    Args:
        email (str): The user's email.
        password (str): The user's password.
        db (Session): The database session.

    Returns:
        Optional[User]: The user object if authenticated, else None.
    """
    user = crud.user.get_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

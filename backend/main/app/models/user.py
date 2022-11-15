""" User relation """

from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType


class User(Base):
    """User model"""

    first_name = Column(String(256), nullable=False, index=True)
    last_name = Column(String(256), nullable=False, index=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)

    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", backref="user", cascade="all, delete-orphan")

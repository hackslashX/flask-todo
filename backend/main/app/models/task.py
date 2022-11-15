""" Task relation """

from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship
from strenum import StrEnum


class TaskStatus(StrEnum):
    """Task status enum"""

    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    """Task model"""

    title = Column(String(256), nullable=False, index=True)
    description = Column(TEXT, nullable=False)
    status = Column(Enum(TaskStatus), default="pending", index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)

    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    task_tags = relationship("TaskTag", backref="task", cascade="all, delete-orphan")

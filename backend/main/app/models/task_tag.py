""" Task Tag relation """

from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint


class TaskTag(Base):
    """Task Tag model"""

    task_id = Column(Integer, ForeignKey("task.id"), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False, index=True)

    date_created = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("task_id", "tag_id", name="task_tag_unique"),)

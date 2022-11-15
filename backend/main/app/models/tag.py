""" Tag relation """

from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Tag(Base):
    """Tag model"""

    name = Column(String(24), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)

    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    task_tags = relationship("TaskTag", backref="tag", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("name", "user_id", name="tag_unique"),)

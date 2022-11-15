""" Task Tag Schema """

from app.schemas.base import BaseSchema
from marshmallow import EXCLUDE, fields


class TaskTagBase(BaseSchema):
    """Task Tag base schema"""

    task_id = fields.Int(required=True)
    tag_id = fields.Int(required=True)


class TaskTagCreate(TaskTagBase):
    """Task Tag create schema"""


class TaskTagUpdate(TaskTagBase):
    """Task Tag update schema"""


class TaskTagInDB(TaskTagBase):
    """Task Tag in database schema"""

    class Meta:
        """Meta class"""

        unknown = EXCLUDE

    id = fields.Int()
    date_created = fields.DateTime()


class TaskTag(TaskTagInDB):
    """Task Tag schema"""

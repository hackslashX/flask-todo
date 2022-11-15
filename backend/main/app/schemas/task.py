""" Task Schema """

from app.models.task import TaskStatus
from app.schemas.base import BaseSchema
from app.schemas.tag import Tag
from marshmallow import EXCLUDE, fields, validate


class TaskBase(BaseSchema):
    """Task base schema"""

    title = fields.String(validate=validate.Length(min=2, max=256), required=True)
    description = fields.String(required=True)


class TaskTagsBase(TaskBase):
    """Task tags base schema"""

    tags = fields.List(fields.Int, required=False, allow_blank=True)


class TaskCreate(TaskTagsBase):
    """Task create schema"""


class TaskUpdate(TaskTagsBase):
    """Task update schema"""

    title = fields.String(validate=validate.Length(min=2, max=256), required=False)
    description = fields.String(required=False)
    status = fields.Enum(enum=TaskStatus, required=False)


class TaskInDB(TaskBase):
    """Task in database schema"""

    class Meta:
        """Meta class"""

        unknown = EXCLUDE

    id = fields.Int()
    user_id = fields.Int()
    status = fields.Enum(enum=TaskStatus)
    date_created = fields.DateTime()
    date_updated = fields.DateTime()


class Task(TaskInDB):
    """Task schema"""

    tags = fields.List(fields.Nested(Tag), required=False, allow_blank=True)

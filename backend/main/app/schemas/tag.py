""" Tag Schemas """

from app.schemas.base import BaseSchema
from marshmallow import EXCLUDE, fields, validate


class TagBase(BaseSchema):
    """Tag base schema"""

    name = fields.String(validate=validate.Length(min=2, max=256), required=True)


class TagCreate(TagBase):
    """Tag create schema"""


class TagUpdate(TagBase):
    """Tag update schema"""


class TagInDB(TagBase):
    """Tag in database schema"""

    class Meta:
        """Meta class"""

        unknown = EXCLUDE

    id = fields.Int()
    user_id = fields.Int()
    date_created = fields.DateTime()
    date_updated = fields.DateTime()


class Tag(TagInDB):
    """Tag schema"""

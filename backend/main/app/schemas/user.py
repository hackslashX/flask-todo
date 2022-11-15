""" User Schema """

from app.schemas.base import BaseSchema
from app.utils.constants import PASSWORD_REGEX
from marshmallow import EXCLUDE, fields, validate


class UserBase(BaseSchema):
    """User base schema"""

    first_name = fields.String(validate=validate.Length(min=2, max=256), required=True)
    last_name = fields.String(validate=validate.Length(min=2, max=256), required=True)
    email = fields.Email(required=True)


class UserCreate(UserBase):
    """User create schema"""

    password = fields.String(
        validate=validate.Regexp(regex=PASSWORD_REGEX), required=True
    )


class UserUpdate(BaseSchema):
    """User update schema"""

    first_name = fields.String(validate=validate.Length(min=2, max=256), required=False)
    last_name = fields.String(validate=validate.Length(min=2, max=256), required=False)
    password = fields.String(
        validate=validate.Regexp(regex=PASSWORD_REGEX), required=False
    )


class UserInDB(UserBase):
    """User in database schema"""

    class Meta:
        """Meta class"""

        unknown = EXCLUDE

    id = fields.Int()
    is_active = fields.Boolean()
    date_created = fields.DateTime()
    date_updated = fields.DateTime()
    last_login = fields.DateTime()


class User(UserInDB):
    """User schema"""

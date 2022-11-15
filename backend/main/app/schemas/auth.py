""" Auth Schemas """

from app.schemas.base import BaseSchema
from marshmallow import fields, validate


class AuthLogin(BaseSchema):
    """Auth login schema"""

    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=1), required=True)


class AuthLoginTokens(BaseSchema):
    """Auth login tokens schema"""

    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)
    key = fields.String(required=True)

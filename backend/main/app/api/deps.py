""" Contains API dependency functions, such as Response Classes,
    DB Sessions, Injection Decorators, etc. """

import json
from http import HTTPStatus
from typing import Any, Generator

from app.core.crypt import encrypt_data_aes, generate_determinstic_aes_key
from app.db.base import User
from app.db.session import SessionLocal
from app.strings import GeneralStrings
from flask import Response, request
from flask_jwt_extended import get_jwt, get_jwt_identity
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest


class BaseResponse(dict):
    """Base API Response Class"""

    def __init__(
        self, message: str, status: int, data: Any = None, error: bool = False
    ):
        if data is None:
            data = {}
        if isinstance(data, ValidationError):
            data = data.__dict__
        self.status = status
        self.error = error
        super().__init__(msg=message, data=data)

    def dict(self):
        """Returns the response as a dictionary

        Returns:
            dict: The response as a dictionary
        """
        return self

    def json(self):
        """Returns the response as a JSON string

        Returns:
            str: The response as a JSON string
        """
        return json.dumps(self)


def get_db() -> Generator:
    """Get a database session.

    Yields:
        Generator: A database session.
    """

    db_object = SessionLocal()
    db_object.current_user_id = None
    try:
        yield db_object
    finally:
        db_object.close()


def request_inject(
    input_schema: Schema,
    output_schema: Schema,
    encrypt_response: bool = True,
) -> Any:
    """Validate and deserialize request data.

    Args:
        schema (Any): A marshmallow schema.
        **kwargs (Any): Keyword arguments to pass to schema.load.

    Returns:
        Any: A decorator.
    """

    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            db_object = next(get_db())

            # If encrypt_response is True, get salt from JWT token and construct key
            if encrypt_response:
                salt = get_jwt()["salt"]
                key = generate_determinstic_aes_key(
                    password=db_object.query(User)
                    .get(get_jwt_identity())
                    .hashed_password,
                    salt=salt,
                )

            if input_schema is not None:
                try:
                    json_data = request.get_json(force=True)
                except BadRequest:
                    base_response = BaseResponse(
                        message=GeneralStrings.invalid_request_data(),
                        status=HTTPStatus.BAD_REQUEST,
                        error=True,
                    )
                    return Response(
                        response=base_response.json(),
                        status=base_response.status,
                        mimetype="application/json",
                    )
                # Validate and deserialize input
                try:
                    data_schema = input_schema()
                    data = data_schema.load(json_data)
                except ValidationError as err:
                    base_response = BaseResponse(
                        message=GeneralStrings.invalid_request_data(),
                        status=HTTPStatus.BAD_REQUEST,
                        data=err,
                        error=True,
                    )
                    return Response(
                        response=base_response.json(),
                        status=base_response.status,
                        mimetype="application/json",
                    )
                base_response = func(request_data=data, db=db_object, *args, **kwargs)
            else:
                base_response = func(db=db_object, *args, **kwargs)

            if base_response.error:
                return Response(
                    base_response.json(),
                    status=base_response.status,
                    mimetype="application/json",
                )

            # Validate and serialize output
            try:
                # Convert data to a list
                is_list = False
                if not isinstance(base_response["data"], list):
                    mid_data = [base_response["data"]]
                else:
                    is_list = True
                    mid_data = base_response["data"]

                # Serialize data
                if mid_data:
                    data_schema = output_schema(many=True)
                    if not isinstance(mid_data[0], dict):
                        mid_data = [item.dict() for item in mid_data]

                    data = data_schema.load(mid_data)
                    data = data_schema.dump(data)

                    # Convert back
                    if is_list:
                        base_response["data"] = data
                    else:
                        base_response["data"] = data[0]

                # Encrypt response
                if encrypt_response:
                    data = json.dumps(base_response["data"]).encode("utf-8")
                    base_response["data"] = encrypt_data_aes(data=data, key=key)

                return Response(
                    base_response.json(),
                    status=base_response.status,
                    mimetype="application/json",
                )
            except ValidationError:
                base_response = BaseResponse(
                    message=GeneralStrings.invalid_response_data(),
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    error=True,
                )
                return Response(
                    base_response.json(),
                    status=base_response.status,
                    mimetype="application/json",
                )

        return wrapper

    return decorator

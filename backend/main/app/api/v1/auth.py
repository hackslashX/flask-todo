""" Authentication API """

from http import HTTPStatus

from app import crud, schemas
from app.api.deps import BaseResponse, get_db, request_inject
from app.core.auth import authenticate
from app.core.crypt import generate_aes_key
from app.db.session import SessionLocal
from app.strings import AuthStrings, GeneralStrings
from flask import Blueprint, Response, request
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/login", methods=["POST"], endpoint="login")
@request_inject(
    input_schema=schemas.AuthLogin,
    output_schema=schemas.AuthLoginTokens,
    encrypt_response=False,
)
def login_user(request_data: dict, db: Session) -> BaseResponse:
    """Login a user.
    Args:
        request_data (dict): The request data.
        db (Session): The database session.

    Returns:
        BaseResponse: The response object.
    """

    # Authenticate user
    user = authenticate(
        email=request_data["email"], password=request_data["password"], db=db
    )
    if not user:
        return BaseResponse(
            message=AuthStrings.incorrect_email_or_password(),
            status=HTTPStatus.UNAUTHORIZED,
            error=True,
        )

    # Generate a unique AES key
    key, salt = generate_aes_key(user.hashed_password)

    # Generate access and refresh tokens
    # Add salt to access token
    access_token = create_access_token(
        identity=user.id, additional_claims={"salt": salt}
    )
    refresh_token = create_refresh_token(identity=user.id)

    # Return
    return BaseResponse(
        message=AuthStrings.user_logged_in(),
        status=HTTPStatus.OK,
        data={"access_token": access_token, "refresh_token": refresh_token, "key": key},
    )

""" User API """

from http import HTTPStatus

from app import crud, schemas
from app.api.deps import BaseResponse, get_db, request_inject
from app.strings import UserStrings
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from sqlalchemy.orm import Session

user_blueprint = Blueprint("user", __name__)
user_api = Api(user_blueprint)


class User(Resource):
    """User API"""

    @request_inject(
        input_schema=schemas.UserCreate,
        output_schema=schemas.User,
        encrypt_response=False,
    )
    def put(self, request_data: dict, db: Session) -> BaseResponse:
        """Create a user.

        Args:
            request_data (dict): The request data.
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        # Check if user already exists
        user = crud.user.get_by_email(db=db, email=request_data["email"])
        if user:
            return BaseResponse(
                message=UserStrings.user_already_exists(),
                status=HTTPStatus.CONFLICT,
                error=True,
            )

        # Input data is valid, create the user in database
        user = crud.user.create(db=db, obj_in=request_data)

        # Return
        return BaseResponse(
            message=UserStrings.user_created(),
            status=HTTPStatus.CREATED,
            data=user,
        )

    @jwt_required()
    @request_inject(input_schema=None, output_schema=schemas.User)
    def get(self, db: Session) -> BaseResponse:
        """Get current user.

        Args:
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        # Return current user
        user_id = get_jwt_identity()
        user = crud.user.get(db=db, id=user_id)

        return BaseResponse(
            message=UserStrings.get_success(),
            status=HTTPStatus.OK,
            data=user,
        )

    @jwt_required()
    @request_inject(input_schema=schemas.UserUpdate, output_schema=schemas.User)
    def patch(self, request_data: dict, db: Session) -> BaseResponse:
        """Update current user.

        Args:
            request_data (dict): The request data.
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        # Update current user
        user_id = get_jwt_identity()
        user = crud.user.update(
            db=db, db_obj=crud.user.get(db=db, id=user_id), obj_in=request_data
        )

        return BaseResponse(
            message=UserStrings.update_success(),
            status=HTTPStatus.OK,
            data=user,
        )


user_api.add_resource(User, "/user")

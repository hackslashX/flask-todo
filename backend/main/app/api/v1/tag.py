""" Tag API """

from http import HTTPStatus

from app import crud, schemas
from app.api.deps import BaseResponse, get_db, request_inject
from app.strings import TagStrings
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from sqlalchemy.orm import Session

tag_blueprint = Blueprint("tag", __name__)
tag_api = Api(tag_blueprint)


class Tag(Resource):
    """Tag API"""

    method_decorators = [jwt_required()]

    @request_inject(input_schema=schemas.TagCreate, output_schema=schemas.Tag)
    def put(self, request_data: dict, db: Session) -> BaseResponse:
        """Create a tag.

        Args:
            request_data (dict): The request data.
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()

        # Check if tag already exists
        tag = crud.tag.get_by_name(db=db, name=request_data["name"], user_id=user_id)
        if tag:
            return BaseResponse(
                message=TagStrings.already_exists(),
                status=HTTPStatus.CONFLICT,
                error=True,
            )

        request_data["user_id"] = user_id
        # Input data is valid, create the tag in database
        tag = crud.tag.create(db=db, obj_in=request_data)

        # Return
        return BaseResponse(
            message=TagStrings.create_success(),
            status=HTTPStatus.CREATED,
            data=tag,
        )

    @request_inject(input_schema=None, output_schema=schemas.Tag)
    def get(self, db: Session) -> BaseResponse:
        """Get all tags.

        Args:
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tags = crud.tag.get_multi(db=db, user_id=user_id)

        return BaseResponse(
            message=TagStrings.get_success(),
            status=HTTPStatus.OK,
            data=tags,
        )


class TagById(Resource):
    """Tag by ID API"""

    method_decorators = [jwt_required()]

    @request_inject(input_schema=None, output_schema=schemas.Tag)
    def get(self, db: Session, tag_id: int) -> BaseResponse:
        """Get a tag by ID.

        Args:
            db (Session): The database session.
            tag_id (int): The tag ID.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tag = crud.tag.get(db=db, id=tag_id, user_id=user_id)

        if not tag:
            return BaseResponse(
                message=TagStrings.not_found(),
                status=HTTPStatus.NOT_FOUND,
                error=True,
            )

        return BaseResponse(
            message=TagStrings.get_success(),
            status=HTTPStatus.OK,
            data=tag,
        )

    @request_inject(input_schema=schemas.TagUpdate, output_schema=schemas.Tag)
    def patch(self, request_data: dict, db: Session, tag_id: int) -> BaseResponse:
        """Update a tag by ID.

        Args:
            request_data (dict): The request data.
            db (Session): The database session.
            tag_id (int): The tag ID.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tag = crud.tag.get(db=db, id=tag_id, user_id=user_id)

        if not tag:
            return BaseResponse(
                message=TagStrings.not_found(),
                status=HTTPStatus.NOT_FOUND,
                error=True,
            )

        tag = crud.tag.update(db=db, db_obj=tag, obj_in=request_data)

        return BaseResponse(
            message=TagStrings.update_success(),
            status=HTTPStatus.OK,
            data=tag,
        )

    @request_inject(input_schema=None, output_schema=schemas.Tag)
    def delete(self, db: Session, tag_id: int) -> BaseResponse:
        """Delete a tag by ID.

        Args:
            db (Session): The database session.
            tag_id (int): The tag ID.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tag = crud.tag.remove(db=db, id=tag_id, user_id=user_id)

        if tag:
            return BaseResponse(
                message=TagStrings.delete_success(),
                status=HTTPStatus.OK,
                data=tag,
            )

        return BaseResponse(
            message=TagStrings.not_found(),
            status=HTTPStatus.NOT_FOUND,
            error=True,
        )


tag_api.add_resource(Tag, "/tag")
tag_api.add_resource(TagById, "/tag/<int:tag_id>")

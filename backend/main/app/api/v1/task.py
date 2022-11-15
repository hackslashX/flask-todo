""" Task API """

from http import HTTPStatus

from app import crud, schemas
from app.api.deps import BaseResponse, get_db, request_inject
from app.strings import TaskStrings, TagStrings
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from sqlalchemy.orm import Session

task_blueprint = Blueprint("task", __name__)
task_api = Api(task_blueprint)


class Task(Resource):
    """Task API"""

    method_decorators = [jwt_required()]

    @request_inject(input_schema=schemas.TaskCreate, output_schema=schemas.Task)
    def put(self, request_data: dict, db: Session) -> BaseResponse:
        """Create a task.

        Args:
            request_data (dict): The request data.
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()

        tags = []
        tags_data = []
        if request_data.get("tags"):
            # Verify that all tags provided exist
            tags = crud.tag.get_multi_id(
                db=db, ids=request_data["tags"], user_id=user_id
            )
            if len(tags) != len(request_data["tags"]):
                return BaseResponse(
                    message=TagStrings.not_found(),
                    status=HTTPStatus.NOT_FOUND,
                    error=True,
                )

            # Remove tags from request data
            tags_data = [tag.dict() for tag in tags]
            tags = request_data.pop("tags")

        request_data["user_id"] = user_id
        # Input data is valid, create the task in database
        task = crud.task.create(db=db, obj_in=request_data)

        # Add tags to task
        crud.task_tag.create_multi(db=db, obj_in=tags, task_id=task.id)
        # Add tags to task
        task = task.dict()
        task["tags"] = tags_data

        # Return
        return BaseResponse(
            message=TaskStrings.create_success(),
            status=HTTPStatus.CREATED,
            data=task,
        )

    @request_inject(input_schema=None, output_schema=schemas.Task)
    def get(self, db: Session) -> BaseResponse:
        """Get all tasks.

        Args:
            db (Session): The database session.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tasks = crud.task.get_multi(db=db, user_id=user_id)

        return BaseResponse(
            message=TaskStrings.get_success(),
            status=HTTPStatus.OK,
            data=tasks,
        )


class TaskById(Resource):
    """Task API"""

    method_decorators = [jwt_required()]

    @request_inject(input_schema=None, output_schema=schemas.Task)
    def get(self, db: Session, task_id: int) -> BaseResponse:
        """Get a task by id.

        Args:
            db (Session): The database session.
            task_id (int): The task id.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        task = crud.task.get_by_id(db=db, id=task_id, user_id=user_id)

        if not task:
            return BaseResponse(
                message=TaskStrings.not_found(),
                status=HTTPStatus.NOT_FOUND,
                error=True,
            )

        # Get task tags
        tags = crud.task_tag.get_multi(db=db, task_id=task_id)
        tags = [tag.tag.dict() for tag in tags]

        # Add tags to task
        task = task.dict()
        task["tags"] = tags

        return BaseResponse(
            message=TaskStrings.get_success(),
            status=HTTPStatus.OK,
            data=task,
        )

    @request_inject(input_schema=schemas.TaskUpdate, output_schema=schemas.Task)
    def patch(self, request_data: dict, db: Session, task_id: int) -> BaseResponse:
        """Update a task by id.

        Args:
            request_data (dict): The request data.
            db (Session): The database session.
            task_id (int): The task id.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        task = crud.task.get_by_id(db=db, id=task_id, user_id=user_id)

        if not task:
            return BaseResponse(
                message=TaskStrings.not_found(),
                status=HTTPStatus.NOT_FOUND,
                error=True,
            )

        tags = None
        tags_data = []
        if request_data.get("tags"):
            # Verify that all tags provided exist
            tags = crud.tag.get_multi_id(
                db=db, ids=request_data["tags"], user_id=user_id
            )
            if len(tags) != len(request_data["tags"]):
                return BaseResponse(
                    message=TagStrings.not_found(),
                    status=HTTPStatus.NOT_FOUND,
                    error=True,
                )

            # Remove tags from request data
            tags_data = [tag.dict() for tag in tags]
            tags = request_data.pop("tags")
        else:
            # Get task tags
            task_tags = crud.task_tag.get_multi(db=db, task_id=task_id)
            current_tags = [tag.tag_id for tag in task_tags]
            tags_data = crud.tag.get_multi_id(db=db, ids=current_tags, user_id=user_id)
            tags_data = [tag.dict() for tag in tags_data]

        # Update task
        if (request_data.get("title") and task.title != request_data.get("title")) or (
            request_data.get("description")
            and task.description != request_data.get("description")
            or (
                request_data.get("status") and task.status != request_data.get("status")
            )
        ):
            task = crud.task.update(db=db, db_obj=task, obj_in=request_data)

        # Update tags
        if tags:
            # Get current task tags
            task_tags = crud.task_tag.get_multi(db=db, task_id=task_id)
            current_tags = set([tag.tag_id for tag in task_tags])
            # Get tags from request
            request_tags = set(tags)
            # Delete tags that are in current_tags but not in request_tags
            tags_to_delete = current_tags - request_tags
            crud.task_tag.delete_multi(db=db, task_id=task_id, tag_ids=tags_to_delete)
            # Create tags that are in request_tags but not in current_tags
            tags_to_create = request_tags - current_tags
            new_tags = crud.task_tag.create_multi(
                db=db, obj_in=tags_to_create, task_id=task_id
            )

        # Add tags to task
        task = task.dict()
        task["tags"] = tags_data

        return BaseResponse(
            message=TaskStrings.update_success(),
            status=HTTPStatus.OK,
            data=task,
        )

    @request_inject(input_schema=None, output_schema=schemas.Task)
    def delete(self, db: Session, task_id: int) -> BaseResponse:
        """Delete a task by id.

        Args:
            db (Session): The database session.
            task_id (int): The task id.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        task = crud.task.remove(db=db, id=task_id, user_id=user_id)

        if not task:
            return BaseResponse(
                message=TaskStrings.not_found(),
                status=HTTPStatus.NOT_FOUND,
                error=True,
            )

        return BaseResponse(
            message=TaskStrings.delete_success(),
            status=HTTPStatus.OK,
            data=task,
        )


class TaskByStatus(Resource):
    """Task API"""

    method_decorators = [jwt_required()]

    @request_inject(input_schema=None, output_schema=schemas.Task)
    def get(self, db: Session, status: str) -> BaseResponse:
        """Get a task by status.

        Args:
            db (Session): The database session.
            status (str): The task status.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tasks = crud.task.get_multi_by_status(db=db, user_id=user_id, status=status)

        return BaseResponse(
            message=TaskStrings.get_success(),
            status=HTTPStatus.OK,
            data=tasks,
        )


class TaskByTag(Resource):
    """Task API"""

    method_decorators = [jwt_required()]

    @request_inject(input_schema=None, output_schema=schemas.Task)
    def get(self, db: Session, tag_id: int) -> BaseResponse:
        """Get a task by tag.

        Args:
            db (Session): The database session.
            tag_id (int): The tag id.

        Returns:
            BaseResponse: The response object.
        """
        user_id = get_jwt_identity()
        tasks = crud.task.get_multi_by_tag(db=db, user_id=user_id, tag_id=tag_id)

        return BaseResponse(
            message=TaskStrings.get_success(),
            status=HTTPStatus.OK,
            data=tasks,
        )


task_api.add_resource(Task, "/task")
task_api.add_resource(TaskById, "/task/<int:task_id>")
task_api.add_resource(TaskByStatus, "/task/status/<string:status>")
task_api.add_resource(TaskByTag, "/task/tag/<int:tag_id>")

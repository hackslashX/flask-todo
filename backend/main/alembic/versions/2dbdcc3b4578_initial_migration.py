"""initial migration

Revision ID: 2dbdcc3b4578
Revises: 
Create Date: 2022-11-16 00:48:13.061587

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "2dbdcc3b4578"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(length=256), nullable=False),
        sa.Column("last_name", sa.String(length=256), nullable=False),
        sa.Column(
            "email", sqlalchemy_utils.types.email.EmailType(length=255), nullable=False
        ),
        sa.Column("hashed_password", sa.String(length=256), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_first_name"), "user", ["first_name"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_last_name"), "user", ["last_name"], unique=False)
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=24), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "user_id", name="tag_unique"),
    )
    op.create_index(op.f("ix_tag_id"), "tag", ["id"], unique=False)
    op.create_index(op.f("ix_tag_name"), "tag", ["name"], unique=False)
    op.create_index(op.f("ix_tag_user_id"), "tag", ["user_id"], unique=False)
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "in_progress", "done", name="taskstatus"),
            nullable=True,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_task_id"), "task", ["id"], unique=False)
    op.create_index(op.f("ix_task_status"), "task", ["status"], unique=False)
    op.create_index(op.f("ix_task_title"), "task", ["title"], unique=False)
    op.create_index(op.f("ix_task_user_id"), "task", ["user_id"], unique=False)
    op.create_table(
        "task_tag",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tag.id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["task.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("task_id", "tag_id", name="task_tag_unique"),
    )
    op.create_index(op.f("ix_task_tag_id"), "task_tag", ["id"], unique=False)
    op.create_index(op.f("ix_task_tag_tag_id"), "task_tag", ["tag_id"], unique=False)
    op.create_index(op.f("ix_task_tag_task_id"), "task_tag", ["task_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_task_tag_task_id"), table_name="task_tag")
    op.drop_index(op.f("ix_task_tag_tag_id"), table_name="task_tag")
    op.drop_index(op.f("ix_task_tag_id"), table_name="task_tag")
    op.drop_table("task_tag")
    op.drop_index(op.f("ix_task_user_id"), table_name="task")
    op.drop_index(op.f("ix_task_title"), table_name="task")
    op.drop_index(op.f("ix_task_status"), table_name="task")
    op.drop_index(op.f("ix_task_id"), table_name="task")
    op.drop_table("task")
    op.drop_index(op.f("ix_tag_user_id"), table_name="tag")
    op.drop_index(op.f("ix_tag_name"), table_name="tag")
    op.drop_index(op.f("ix_tag_id"), table_name="tag")
    op.drop_table("tag")
    op.drop_index(op.f("ix_user_last_name"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_first_name"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###

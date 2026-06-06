"""add geo_export_jobs table

Revision ID: b2c3d4e5f6a7
Revises: 861a0419ccf8
Create Date: 2026-06-06 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "861a0419ccf8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    export_status = sa.Enum(
        "pending", "running", "done", "error",
        name="exportstatus",
    )
    export_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "geo_export_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("kommune_id", sa.Integer(), nullable=False),
        sa.Column("export_type", sa.String(length=32), nullable=False),
        sa.Column("status", export_status, nullable=True),
        sa.Column("file_path", sa.String(length=512), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["kommune_id"], ["kommunen.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_geo_export_jobs_id"), "geo_export_jobs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_geo_export_jobs_id"), table_name="geo_export_jobs")
    op.drop_table("geo_export_jobs")
    sa.Enum(name="exportstatus").drop(op.get_bind(), checkfirst=True)

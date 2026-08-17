"""Assessment-Kind-Prozess: PID/Abbruch/Queue-Spalten an project_statuses + Status QUEUED

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2026-07-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e6f7a8b9c0d1"
down_revision: Union[str, None] = "d5e6f7a8b9c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("project_statuses", sa.Column("worker_pid", sa.Integer(), nullable=True))
    op.add_column("project_statuses", sa.Column("worker_start_ticks", sa.BigInteger(), nullable=True))
    op.add_column(
        "project_statuses",
        sa.Column("abort_requested", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("project_statuses", sa.Column("queued_at", sa.DateTime(), nullable=True))
    op.add_column(
        "project_statuses",
        sa.Column("recalc_recommended", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    # Postgres persistiert Enum-NAMEN (PENDING, RUNNING, …); ADD VALUE ist
    # transaktionsbeschränkt → Autocommit-Block.
    if op.get_bind().dialect.name == "postgresql":
        with op.get_context().autocommit_block():
            op.execute("ALTER TYPE assessmentstatus ADD VALUE IF NOT EXISTS 'QUEUED'")


def downgrade() -> None:
    op.drop_column("project_statuses", "recalc_recommended")
    op.drop_column("project_statuses", "queued_at")
    op.drop_column("project_statuses", "abort_requested")
    op.drop_column("project_statuses", "worker_start_ticks")
    op.drop_column("project_statuses", "worker_pid")
    # Enum-Wert QUEUED bleibt bestehen (Postgres kann Werte nicht entfernen);
    # er ist ohne die Spalten harmlos.

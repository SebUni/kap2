"""Zensus 100m grid columns on grid_cells

Revision ID: c4d5e6f7a8b9
Revises: b2c3d4e5f6a7
Create Date: 2026-06-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4d5e6f7a8b9"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Grid change invalidates derived data — wipe dependent tables first.
    op.execute("TRUNCATE measure_impacts, risk_zone_cells, risk_zones, cell_assessments, grid_cells RESTART IDENTITY CASCADE")

    op.add_column("grid_cells", sa.Column("gitter_id", sa.String(length=64), nullable=True))
    op.add_column("grid_cells", sa.Column("x_3035", sa.Integer(), nullable=True))
    op.add_column("grid_cells", sa.Column("y_3035", sa.Integer(), nullable=True))

    op.execute(
        "UPDATE grid_cells SET gitter_id = 'LEGACY_' || id::text, "
        "x_3035 = col_idx * 100, y_3035 = row_idx * 100 WHERE gitter_id IS NULL"
    )

    op.alter_column("grid_cells", "gitter_id", nullable=False)
    op.alter_column("grid_cells", "x_3035", nullable=False)
    op.alter_column("grid_cells", "y_3035", nullable=False)
    op.create_index(op.f("ix_grid_cells_gitter_id"), "grid_cells", ["gitter_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_grid_cells_gitter_id"), table_name="grid_cells")
    op.drop_column("grid_cells", "y_3035")
    op.drop_column("grid_cells", "x_3035")
    op.drop_column("grid_cells", "gitter_id")

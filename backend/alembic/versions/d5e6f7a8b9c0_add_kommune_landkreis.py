"""Landkreis-Spalte an kommunen (Dashboard-Kopf, Nominatim address.county)

Revision ID: d5e6f7a8b9c0
Revises: aa0fe1d8c95e
Create Date: 2026-07-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d5e6f7a8b9c0"
down_revision: Union[str, None] = "aa0fe1d8c95e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("kommunen", sa.Column("landkreis", sa.String(length=150), nullable=True))


def downgrade() -> None:
    op.drop_column("kommunen", "landkreis")

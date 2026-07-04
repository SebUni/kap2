"""Measure-level impact_summary column on adaptation_measures

Revision ID: aa0fe1d8c95e
Revises: c4d5e6f7a8b9
Create Date: 2026-07-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aa0fe1d8c95e"
down_revision: Union[str, None] = "c4d5e6f7a8b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ersetzt die frühere (fehlerhafte) Praxis, das Kosten-Ergebnis von
    # compute_impact() auf eine beliebige measure_impacts-Zelle zu schreiben:
    # jetzt ein eigenes Feld auf der Maßnahme selbst.
    op.add_column(
        "adaptation_measures",
        sa.Column("impact_summary", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("adaptation_measures", "impact_summary")

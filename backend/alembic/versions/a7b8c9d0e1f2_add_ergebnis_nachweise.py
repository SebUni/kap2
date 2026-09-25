"""Nachweise zur Einbeziehung: ergebnis_nachweise

Revision ID: a7b8c9d0e1f2
Revises: f1a2b3c4d5e6
Create Date: 2026-09-25

Nachweisfelder zu ISO 14091 A6 (Fachabteilungen, externe Expertise) und A10
(angrenzende Kommunen, Land): Welche Stelle hat die Ergebnisse wann gelesen.
Erfasst werden nur Stellen oder Organisationen, keine Personennamen.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, None] = "f1a2b3c4d5e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ergebnis_nachweise",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "kommune_id",
            sa.Integer(),
            sa.ForeignKey("kommunen.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("art", sa.String(length=40), nullable=False),
        sa.Column("stelle", sa.String(length=255), nullable=False),
        sa.Column("datum", sa.Date(), nullable=False),
        sa.Column("vermerk", sa.Text(), nullable=True),
        sa.Column("erfasst_am", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_ergebnis_nachweise_id", "ergebnis_nachweise", ["id"])
    op.create_index("ix_ergebnis_nachweise_kommune_id", "ergebnis_nachweise", ["kommune_id"])


def downgrade() -> None:
    op.drop_index("ix_ergebnis_nachweise_kommune_id", table_name="ergebnis_nachweise")
    op.drop_index("ix_ergebnis_nachweise_id", table_name="ergebnis_nachweise")
    op.drop_table("ergebnis_nachweise")

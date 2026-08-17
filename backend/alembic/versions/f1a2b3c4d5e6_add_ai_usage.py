"""KI-Assistent: ai_usage (Token-Verbrauchs-Ledger)

Revision ID: f1a2b3c4d5e6
Revises: e6f7a8b9c0d1
Create Date: 2026-07-07

Token-Verbrauchs-Ledger (ai_usage) für den KI-Assistenten. Einstellungen
(Mistral-API-Schlüssel, Modell, Token-Limits) liegen im bereits vorhandenen
globalen Key-Value-Store ``app_settings`` (Demo-Feature) — daher hier nur die
neue ai_usage-Tabelle. Auf Dev-Instanzen entsteht sie zusätzlich über den
Startup-``create_all`` (app/main.py); diese Migration hält Prod-DBs synchron.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f1a2b3c4d5e6"
down_revision: Union[str, None] = "e6f7a8b9c0d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("kommune_id", sa.Integer(), nullable=True),
        sa.Column("model", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("prompt_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("completion_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_tokens", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_ai_usage_id", "ai_usage", ["id"])
    op.create_index("ix_ai_usage_created_at", "ai_usage", ["created_at"])
    op.create_index("ix_ai_usage_total_tokens", "ai_usage", ["total_tokens"])


def downgrade() -> None:
    op.drop_index("ix_ai_usage_total_tokens", table_name="ai_usage")
    op.drop_index("ix_ai_usage_created_at", table_name="ai_usage")
    op.drop_index("ix_ai_usage_id", table_name="ai_usage")
    op.drop_table("ai_usage")

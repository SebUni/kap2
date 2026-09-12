"""Basis-Schema: die 15 Tabellen, die nie eine Migration angelegt hat

Revision ID: b1aadda418b4
Revises:
Create Date: 2026-09-12

Wurzel der Migrationskette (T-0209). Bis hierher begann die Kette bei
``861a0419ccf8``, die bereits Fremdschlüssel auf ``kommunen`` und
``grid_cells`` setzt — auf einer leeren Datenbank brach sie deshalb sofort ab.
Die Tabellen entstanden bis dahin nur über ``Base.metadata.create_all()``
(app/main.py).

Erzeugt mit ``alembic revision --autogenerate`` gegen eine leere PostGIS-
Datenbank und anschließend von Hand auf den Stand VOR den nachfolgenden
Revisionen zurückgeschnitten, damit die Kette kollisionsfrei weiterläuft:

* ohne die vier Tabellen, die spätere Revisionen selbst anlegen (Risikozonen
  und ihre Zellen: 861a0419ccf8; Geodaten-Exportaufträge: b2c3d4e5f6a7;
  KI-Token-Ledger: f1a2b3c4d5e6),
* ohne die neun Spalten, die spätere Revisionen nachrüsten (Zensus-Gitter an
  ``grid_cells``: c4d5e6f7a8b9; Kosten-Zusammenfassung an
  ``adaptation_measures``: aa0fe1d8c95e; Kreis an ``kommunen``: d5e6f7a8b9c0;
  die fünf Worker-/Queue-Spalten an ``project_statuses``: e6f7a8b9c0d1).

Der PG-Typ ``assessmentstatus`` entsteht hier (``project_statuses.status``);
``exportstatus`` legt b2c3d4e5f6a7 an. Die GiST-Indizes auf den Geometrie-
Spalten legt GeoAlchemy2 beim ``CREATE TABLE`` selbst an — deshalb stehen sie
hier nicht explizit (wie schon in 861a0419ccf8).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = 'b1aadda418b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('app_settings',
    sa.Column('key', sa.String(length=100), nullable=False),
    sa.Column('value', sa.JSON(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_table('demo_sessions',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_seen_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_demo_sessions_last_seen_at'), 'demo_sessions', ['last_seen_at'], unique=False)
    op.create_table('gemeinden',
    sa.Column('ags', sa.String(length=8), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('bez', sa.String(length=80), nullable=True),
    sa.Column('bundesland', sa.String(length=100), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('area_km2', sa.Float(), nullable=True),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('geometry_simplified', sa.Text(), nullable=True),
    sa.Column('rep_lon', sa.Float(), nullable=True),
    sa.Column('rep_lat', sa.Float(), nullable=True),
    sa.Column('demographics', sa.JSON(), nullable=True),
    sa.Column('vg250_stand', sa.String(length=10), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('ags')
    )
    op.create_table('kommunen',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('bundesland', sa.String(length=100), nullable=True),
    sa.Column('osm_id', sa.String(length=50), nullable=True),
    sa.Column('boundary', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('area_km2', sa.Float(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('osm_id')
    )
    op.create_index(op.f('ix_kommunen_id'), 'kommunen', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('display_name', sa.String(length=255), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('adaptation_measures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kommune_id', sa.Integer(), nullable=False),
    sa.Column('demo_session_id', sa.String(length=36), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('measure_type', sa.String(length=100), nullable=False),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('config', sa.JSON(), nullable=True),
    sa.Column('implementation_year', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['demo_session_id'], ['demo_sessions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['kommune_id'], ['kommunen.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adaptation_measures_demo_session_id'), 'adaptation_measures', ['demo_session_id'], unique=False)
    op.create_index(op.f('ix_adaptation_measures_id'), 'adaptation_measures', ['id'], unique=False)
    op.create_table('config_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kommune_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('key', sa.String(length=100), nullable=False),
    sa.Column('value', sa.JSON(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('parameter_id', sa.String(length=200), nullable=True),
    sa.Column('source', sa.Text(), nullable=True),
    sa.Column('custom_source', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['kommune_id'], ['kommunen.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kommune_id', 'category', 'key', name='uq_config_kommune_cat_key')
    )
    op.create_index(op.f('ix_config_parameters_id'), 'config_parameters', ['id'], unique=False)
    op.create_table('grid_cells',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kommune_id', sa.Integer(), nullable=False),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('row_idx', sa.Integer(), nullable=False),
    sa.Column('col_idx', sa.Integer(), nullable=False),
    sa.Column('cell_size_m', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['kommune_id'], ['kommunen.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grid_cells_id'), 'grid_cells', ['id'], unique=False)
    op.create_table('lite_batch_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('phase', sa.String(length=32), nullable=True),
    sa.Column('progress_pct', sa.Float(), nullable=True),
    sa.Column('processed', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('error_count', sa.Integer(), nullable=True),
    sa.Column('params', sa.JSON(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('finished_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lite_batch_runs_id'), 'lite_batch_runs', ['id'], unique=False)
    op.create_table('project_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kommune_id', sa.Integer(), nullable=False),
    sa.Column('task_key', sa.String(length=64), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('progress_pct', sa.Float(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'QUEUED', 'RUNNING', 'DONE', 'ERROR', name='assessmentstatus'), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('finished_at', sa.DateTime(), nullable=True),
    sa.Column('step_history', sa.JSON(), nullable=True),
    sa.Column('eta_seconds', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['kommune_id'], ['kommunen.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kommune_id', 'task_key', 'level', name='uq_status_kommune_task_level')
    )
    op.create_index(op.f('ix_project_statuses_id'), 'project_statuses', ['id'], unique=False)
    op.create_table('user_kommunen',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('kommune_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['kommune_id'], ['kommunen.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'kommune_id')
    )
    op.create_table('user_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token_hash', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('last_seen_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_sessions_id'), 'user_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_user_sessions_token_hash'), 'user_sessions', ['token_hash'], unique=True)
    op.create_table('cell_assessments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kommune_id', sa.Integer(), nullable=False),
    sa.Column('grid_cell_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('calculated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['grid_cell_id'], ['grid_cells.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['kommune_id'], ['kommunen.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kommune_id', 'grid_cell_id', name='uq_cell_assessment')
    )
    op.create_index(op.f('ix_cell_assessments_id'), 'cell_assessments', ['id'], unique=False)
    op.create_table('gemeinde_lite_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ags', sa.String(length=8), nullable=False),
    sa.Column('risk_code', sa.String(length=64), nullable=False),
    sa.Column('raw_score', sa.Float(), nullable=True),
    sa.Column('index_value', sa.Float(), nullable=True),
    sa.Column('outcome_value', sa.Float(), nullable=True),
    sa.Column('outcome_unit', sa.String(length=32), nullable=True),
    sa.Column('cost_eur', sa.Float(), nullable=True),
    sa.Column('drivers', sa.JSON(), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.Column('computed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ags'], ['gemeinden.ags'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['batch_id'], ['lite_batch_runs.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ags', 'risk_code', name='uq_gemeinde_risk')
    )
    op.create_index(op.f('ix_gemeinde_lite_results_ags'), 'gemeinde_lite_results', ['ags'], unique=False)
    op.create_index(op.f('ix_gemeinde_lite_results_id'), 'gemeinde_lite_results', ['id'], unique=False)
    op.create_index(op.f('ix_gemeinde_lite_results_risk_code'), 'gemeinde_lite_results', ['risk_code'], unique=False)
    op.create_table('measure_impacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measure_id', sa.Integer(), nullable=False),
    sa.Column('grid_cell_id', sa.Integer(), nullable=False),
    sa.Column('indicator_deltas', sa.JSON(), nullable=True),
    sa.Column('costs', sa.JSON(), nullable=True),
    sa.Column('savings', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['grid_cell_id'], ['grid_cells.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['measure_id'], ['adaptation_measures.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_measure_impacts_id'), 'measure_impacts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_measure_impacts_id'), table_name='measure_impacts')
    op.drop_table('measure_impacts')
    op.drop_index(op.f('ix_gemeinde_lite_results_risk_code'), table_name='gemeinde_lite_results')
    op.drop_index(op.f('ix_gemeinde_lite_results_id'), table_name='gemeinde_lite_results')
    op.drop_index(op.f('ix_gemeinde_lite_results_ags'), table_name='gemeinde_lite_results')
    op.drop_table('gemeinde_lite_results')
    op.drop_index(op.f('ix_cell_assessments_id'), table_name='cell_assessments')
    op.drop_table('cell_assessments')
    op.drop_index(op.f('ix_user_sessions_token_hash'), table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_id'), table_name='user_sessions')
    op.drop_table('user_sessions')
    op.drop_table('user_kommunen')
    op.drop_index(op.f('ix_project_statuses_id'), table_name='project_statuses')
    op.drop_table('project_statuses')
    op.drop_index(op.f('ix_lite_batch_runs_id'), table_name='lite_batch_runs')
    op.drop_table('lite_batch_runs')
    op.drop_index(op.f('ix_grid_cells_id'), table_name='grid_cells')
    op.drop_table('grid_cells')
    op.drop_index(op.f('ix_config_parameters_id'), table_name='config_parameters')
    op.drop_table('config_parameters')
    op.drop_index(op.f('ix_adaptation_measures_id'), table_name='adaptation_measures')
    op.drop_index(op.f('ix_adaptation_measures_demo_session_id'), table_name='adaptation_measures')
    op.drop_table('adaptation_measures')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_kommunen_id'), table_name='kommunen')
    op.drop_table('kommunen')
    op.drop_table('gemeinden')
    op.drop_index(op.f('ix_demo_sessions_last_seen_at'), table_name='demo_sessions')
    op.drop_table('demo_sessions')
    op.drop_table('app_settings')
    sa.Enum(name="assessmentstatus").drop(op.get_bind(), checkfirst=True)

"""T-0196: Migration 861a0419ccf8 muss zum Modell RiskZone passen.

Prueft woertlich, dass die Migration keinen nie angelegten ENUM-Typ
(climatetype) mehr referenziert, sondern das Textfeld ``layer_code`` anlegt -
und dass der Unique-Constraint-Name und die Spaltenliste mit
``backend/app/models/models.py::RiskZone`` uebereinstimmen.
"""
from pathlib import Path

MIGRATION_PATH = (
    Path(__file__).resolve().parents[1]
    / "alembic"
    / "versions"
    / "861a0419ccf8_add_risk_zones_and_risk_zone_cells_.py"
)
MODELS_PATH = Path(__file__).resolve().parents[1] / "app" / "models" / "models.py"


def _migration_source() -> str:
    return MIGRATION_PATH.read_text(encoding="utf-8")


def _models_source() -> str:
    return MODELS_PATH.read_text(encoding="utf-8")


def test_migration_referenziert_keinen_climatetype_enum():
    source = _migration_source()
    assert "climatetype" not in source
    assert "climate_type" not in source


def test_migration_hat_layer_code_spalte_wie_im_modell():
    source = _migration_source()
    assert "sa.Column('layer_code', sa.String(64), nullable=False)" in source

    models_source = _models_source()
    assert 'layer_code = Column(String(64), nullable=False)' in models_source


def test_migration_unique_constraint_passt_zum_modell():
    source = _migration_source()
    assert (
        "sa.UniqueConstraint('kommune_id', 'layer_code', 'level', 'zone_index', "
        "name='uq_risk_zone_kommune_layer_level_idx')"
    ) in source

    models_source = _models_source()
    assert (
        'UniqueConstraint("kommune_id", "layer_code", "level", "zone_index",'
    ) in models_source
    assert 'name="uq_risk_zone_kommune_layer_level_idx"' in models_source

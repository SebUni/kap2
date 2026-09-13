"""Statische Kontrolle: Jede Modelltabelle hat eine Migration und umgekehrt.

Vergleicht `Base.metadata.tables` (alle SQLAlchemy-Modelle) mit den
`op.create_table(`-Aufrufen in `alembic/versions/*.py`. Öffnet bewusst keine
Datenbankverbindung (keine PostGIS-Instanz nötig, siehe T-0210): Die Modelle
nutzen `geoalchemy2.Geometry`, was gegen SQLite nicht funktioniert.
"""

import re
from pathlib import Path

VERSIONS_DIR = Path(__file__).resolve().parent.parent / "alembic" / "versions"

# Erlaubt mehrzeilige Aufrufe: der Tabellenname kann in der nächsten Zeile
# stehen (z.B. `op.create_table(\n    "name",`).
CREATE_TABLE_RE = re.compile(r"op\.create_table\(\s*['\"](\w+)['\"]")
DOWN_REVISION_NONE_RE = re.compile(r"down_revision[^=]*=\s*None")


def _migration_table_names() -> set[str]:
    names: set[str] = set()
    for path in VERSIONS_DIR.glob("*.py"):
        text = path.read_text()
        names.update(CREATE_TABLE_RE.findall(text))
    return names


def test_migrationskette_deckt_alle_modelltabellen_ab():
    from app.models import models, auth_models, demo_models, lite_models  # noqa: F401
    from app.models.models import Base

    model_tables = set(Base.metadata.tables.keys())
    migration_tables = _migration_table_names()

    fehlen_in_migration = model_tables - migration_tables
    fehlen_im_modell = migration_tables - model_tables

    assert model_tables == migration_tables, (
        "Migrationskette und Modell laufen auseinander.\n"
        f"Im Modell, aber ohne Migration: {sorted(fehlen_in_migration)}\n"
        f"In Migrationen, aber ohne Modell: {sorted(fehlen_im_modell)}"
    )


def test_genau_eine_migration_ist_die_basis():
    basis_dateien = []
    for path in VERSIONS_DIR.glob("*.py"):
        text = path.read_text()
        if DOWN_REVISION_NONE_RE.search(text):
            basis_dateien.append(path.name)

    assert len(basis_dateien) == 1, (
        "Es muss genau eine Basis-Migration mit down_revision = None geben, "
        f"gefunden: {sorted(basis_dateien)}"
    )

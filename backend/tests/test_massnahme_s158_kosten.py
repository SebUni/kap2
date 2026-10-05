"""P1: Katalogkosten der Pollen-Frühwarnung (S158) mit Herleitung.

Bericht #96 §5.1 (docs/methodik/96_aeroallergene.md): Anschaffung 15.000 € je Station
(Z. 1781 f.), Betrieb 4.000 € je Station und Jahr (Z. 1857 f.); beide sind Abschätzungen von KAP3 („Modellannahme“). Der Test bindet
die Werte der Registry an den Bericht und verlangt Klasse ``abgeschaetzt`` sowie eine
Herleitung mit Wert, Band und Sensitivität.

DB-frei.
"""

from __future__ import annotations

import pytest

from app.services import parameter_registry

CODE = "POLLEN_EARLY_WARNING"


def test_katalogkosten_der_fruehwarnung_mit_herleitung():
    params = {p["id"]: p for p in parameter_registry.catalog_parameters(
        layer_code=CODE, layer_category="measures")}
    soll = {"capex_per_unit": 15000.0, "opex_per_unit_year": 4000.0}
    for name, wert in soll.items():
        zeile = params[f"measures.{CODE}.{name}"]
        assert zeile["value"] == pytest.approx(wert, abs=1e-9)
        assert zeile["evidence_class"] == "abgeschaetzt"
        herleitung = zeile["evidence_derivation"]
        for feld in ("wert", "band", "sensitivitaet"):
            assert str(herleitung.get(feld) or "").strip(), f"{name}: {feld} leer"

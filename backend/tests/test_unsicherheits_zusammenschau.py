"""T-0451: Handlungsfeldübergreifende Unsicherheits-Zusammenschau (Checkliste Zeile 19).

Prüft ``app.services.unsicherheits_zusammenschau``:
(a) jedes Handlungsfeld des Katalogs kommt in der Zusammenschau genau einmal vor,
(b) bei mindestens einer Klimawirkung mit Stufe ``gering`` steht das betroffene
    Handlungsfeld in der Vorsichtsliste und der Hinweistext ist gesetzt,
(c) sind alle Stufen ``mittel`` oder besser, ist die Liste leer und kein Hinweistext gesetzt.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import unsicherheits_zusammenschau as uz  # noqa: E402

KOMMUNE_ID = 1


def _katalog_handlungsfelder() -> set[str]:
    return {r.get("kwra_field") or "ohne Handlungsfeld" for r in catalog.RISKS}


def test_a_jedes_handlungsfeld_genau_einmal_mit_drei_angaben():
    ergebnis = uz.unsicherheits_zusammenschau(KOMMUNE_ID)
    felder = [e["handlungsfeld"] for e in ergebnis["handlungsfelder"]]
    assert len(felder) == len(set(felder))
    assert set(felder) == _katalog_handlungsfelder()
    for e in ergebnis["handlungsfelder"]:
        assert set(e) == {"handlungsfeld", "niedrigste_gewissheit",
                          "parameter_nicht_belegt", "klimawirkungen_niedrigste_stufe"}
        assert isinstance(e["parameter_nicht_belegt"], int)
        assert e["klimawirkungen_niedrigste_stufe"]


def test_b_stufe_gering_setzt_liste_und_hinweis():
    codes = list(catalog.RISKS_BY_CODE)
    stufen = {c: "hoch" for c in codes}
    betroffen = codes[0]
    stufen[betroffen] = "gering"
    feld = catalog.RISKS_BY_CODE[betroffen].get("kwra_field") or "ohne Handlungsfeld"

    ergebnis = uz.unsicherheits_zusammenschau(KOMMUNE_ID, _stufen=stufen)

    assert feld in ergebnis["handlungsfelder_vorsicht"]
    eintrag = next(e for e in ergebnis["handlungsfelder"] if e["handlungsfeld"] == feld)
    assert eintrag["niedrigste_gewissheit"] == "gering"
    assert eintrag["klimawirkungen_niedrigste_stufe"] == [betroffen]
    assert ergebnis["hinweis"]
    assert "vorsichtige Interpretation" in ergebnis["hinweis"]


def test_c_alle_stufen_mittel_oder_besser_ohne_liste_und_hinweis():
    codes = list(catalog.RISKS_BY_CODE)
    stufen = {c: ("mittel" if i % 2 else "hoch") for i, c in enumerate(codes)}

    ergebnis = uz.unsicherheits_zusammenschau(KOMMUNE_ID, _stufen=stufen)

    assert ergebnis["handlungsfelder_vorsicht"] == []
    assert ergebnis["hinweis"] is None

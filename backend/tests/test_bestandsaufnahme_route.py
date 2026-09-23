"""Route GET /api/kommune/{kommune_id}/bestandsaufnahme (T-0758, Vorhaben T-0447).

Prüft: (a) Status 200 und Content-Type ``text/markdown`` für eine berechtigte
Kommune, wenn ``bestandsaufnahme_fuer_kommune`` per monkeypatch ein festes
Ergebnis liefert; (b) Antworttext identisch mit
``bestandsaufnahme_markdown(festes_ergebnis)``; (c) die Route steht in
``kommunenbezogene_routen()`` aus ``test_mandantentrennung.py``, trägt also
``require_kommune_access``.

Der Testaufbau (SQLite, Kommunen A/B, angemeldete Nutzer) wird aus
``test_mandantentrennung.py`` übernommen, nicht nachgebaut.
"""

from __future__ import annotations

from app.services import bestandsaufnahme_service
from app.services.bestandsaufnahme_markdown import bestandsaufnahme_markdown

from test_mandantentrennung import (  # noqa: F401  (Fixtures)
    KOMMUNE_A_ID,
    aufbau,
    client_a,
    client_ohne_kommune,
    kommunenbezogene_routen,
)

PFAD = "/api/kommune/{kommune_id}/bestandsaufnahme"

FESTES_ERGEBNIS = {
    "kommune_id": KOMMUNE_A_ID,
    "name": "Alpenstadt",
    "groessen": [
        {"code": "aeltere_ab_65", "gruppe": "vulnerable_personen",
         "label": "Anteil der Einwohner ab 65 Jahren", "wert": 21.46,
         "einheit": "%", "quellen": ["Zensus_2022"], "luecke_satz": ""},
        {"code": "krankenhaeuser", "gruppe": "klimasensible_strukturen",
         "label": "Krankenhäuser", "wert": None, "einheit": "Anzahl",
         "quellen": [], "luecke_satz": "Für Krankenhäuser liegt kein Wert vor."},
    ],
}


def _fest(monkeypatch):
    aufrufe = []

    def _ersatz(db, kommune):
        aufrufe.append(kommune.id)
        return FESTES_ERGEBNIS

    monkeypatch.setattr(bestandsaufnahme_service, "bestandsaufnahme_fuer_kommune", _ersatz)
    return aufrufe


def test_route_liefert_markdown_fuer_berechtigte_kommune(monkeypatch, client_a):
    aufrufe = _fest(monkeypatch)
    antwort = client_a.get(f"/api/kommune/{KOMMUNE_A_ID}/bestandsaufnahme")
    # (a) Status und Content-Type (Zeichensatz-Zusatz erlaubt)
    assert antwort.status_code == 200, antwort.text
    assert antwort.headers["content-type"].split(";")[0].strip() == "text/markdown"
    # (b) Antworttext identisch mit dem Renderer auf dem festen Ergebnis
    assert antwort.text == bestandsaufnahme_markdown(FESTES_ERGEBNIS)
    assert aufrufe == [KOMMUNE_A_ID]


def test_route_ist_mandantengeschuetzt():
    # (c) in der Laufzeit-Prüfliste, also mit require_kommune_access
    routen = [r for r in kommunenbezogene_routen() if r.pfad == PFAD]
    assert len(routen) == 1, [r.pfad for r in kommunenbezogene_routen()]
    assert routen[0].methoden == ("GET",)
    assert routen[0].pfad_parameter == ("kommune_id",)


def test_route_weist_nutzer_ohne_zuordnung_ab(monkeypatch, client_ohne_kommune):
    aufrufe = _fest(monkeypatch)
    antwort = client_ohne_kommune.get(f"/api/kommune/{KOMMUNE_A_ID}/bestandsaufnahme")
    assert antwort.status_code == 403
    assert aufrufe == []

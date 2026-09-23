"""Route POST /api/anpassungskapazitaet/bewertung (T-0764, Vorhaben T-0448).

Prüft: (1) angemeldeter Aufruf liefert 200, Gesamtstufe nach Engpassregel und
den Markdown-Abschnitt; (2) unbekannte Komponente liefert 422; (3) ein Aufruf
ohne Anmeldung wird mit demselben Statuscode abgewiesen wie die übrigen
``_PROTECTED``-Routen — 401 („Nicht angemeldet“ aus ``require_actor``).

Der Testaufbau (SQLite, angemeldete Nutzer, anonymer Client) wird aus
``test_mandantentrennung.py`` übernommen, nicht nachgebaut.
"""

from __future__ import annotations

from test_mandantentrennung import (  # noqa: F401  (Fixtures)
    KOMMUNE_A_ID,
    aufbau,
    client_a,
    client_anonym,
)

PFAD = "/api/anpassungskapazitaet/bewertung"
EINSCHAETZUNG = {"organisation": 2, "technik": 3, "finanzen": 1, "oekosystem": 2}
STATUS_OHNE_ANMELDUNG = 401


def test_angemeldet_liefert_bewertung_und_markdown(client_a):
    antwort = client_a.post(PFAD, json={"einschaetzung": EINSCHAETZUNG})
    assert antwort.status_code == 200, antwort.text
    daten = antwort.json()
    assert daten["bewertung"]["gesamtstufe"] == 1
    assert daten["markdown"].startswith("## Anpassungskapazität (optionaler Analyseschritt)")


def test_unbekannte_komponente_liefert_422(client_a):
    antwort = client_a.post(PFAD, json={"einschaetzung": {"foo": 1}})
    assert antwort.status_code == 422, antwort.text


def test_ohne_anmeldung_wie_uebrige_geschuetzte_routen(client_anonym):
    vergleich = client_anonym.get(f"/api/kommune/{KOMMUNE_A_ID}/bestandsaufnahme")
    antwort = client_anonym.post(PFAD, json={"einschaetzung": EINSCHAETZUNG})
    assert vergleich.status_code == STATUS_OHNE_ANMELDUNG
    assert antwort.status_code == STATUS_OHNE_ANMELDUNG

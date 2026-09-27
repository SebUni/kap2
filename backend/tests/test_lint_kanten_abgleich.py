"""Test für T-1490-ceo: Der Kanten-Abgleich vergleicht Risikonummern, nicht Knotenkennungen.

Anlass: Der Abgleich Bericht → Mappe verglich Knotenkennungen (E/R/S/W) mit den
Output_IDs der Netzwerkliste, die Risikonummern führen. Damit blieben die Kanten
#95 → #87/#101 ungeprüft, und W196/W197 aus dem Erklärtext von Bericht 96 war ein
Fehlalarm. Geprüft werden die Regeln (d) bis (h) an kleinen Beispieltexten, ohne
Arbeitsmappe.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import (  # noqa: E402
    Lint,
    _kanten_pruefen,
    _netzwerk_kanten,
    _unterabschnitt,
    _weitergaben_lesen,
)

KOPF = "| Output-Kanten (Abgleich-Protokoll) | Konto-Ausschlüsse |\n|---|---|\n"


def _weitergaben(*zeilen: str) -> str:
    return (
        "### Weitergaben (zweispaltig)\n\n" + KOPF + "".join(z + "\n" for z in zeilen)
        + "\n### Konto-Einbettung\n\n- Text mit #55 und W999.\n"
    )


def _pruefen(nr: str, text: str, kanten: set[str]) -> Lint:
    lint = Lint()
    _kanten_pruefen(nr, _unterabschnitt(text, "### Weitergaben"), kanten, lint)
    return lint


ZEILE_87 = "| → **#87** Leistungseinbußen (K2) — **P8** (AP Z12) | Systemvorhaltung → K8 via **ID 102** |"
ZEILE_101 = "| → **#101** Verletzungen — Partitionszitat (ID 101): „Hitzetote (ID 95)“ | #65 rechts zählt nicht |"
ZEILE_KEINE = ("| **keine** — die Netzwerkliste führt für #96 keine Output-Kanten. (W-Ebene: W189 speist "
               "W196/W197) | Arbeitsausfall → K2 via **#87** |")


# (d) Risikonummern der ersten Spalte werden mit Output_IDs_Wirkung verglichen.
def test_d_risikonummern_gedeckt_gruen() -> None:
    lint = _pruefen("95", _weitergaben(ZEILE_87, ZEILE_101), {"87", "101"})
    assert lint.fehler == []


def test_d_nicht_gefuehrte_risikonummer_rot() -> None:
    text = _weitergaben(ZEILE_87, ZEILE_101.replace("#101", "#999"))
    lint = _pruefen("95", text, {"87", "101"})
    rot = [f for f in lint.fehler if f.startswith("Kanten-Abgleich 95 (Bericht → Mappe):")]
    assert len(rot) == 1 and "999" in rot[0]


def test_d_nur_erste_spalte_und_nur_der_abschnitt() -> None:
    risiken, fremde = _weitergaben_lesen(_unterabschnitt(_weitergaben(ZEILE_87), "### Weitergaben"))
    assert risiken == {"87"}  # nicht #65/#55 aus zweiter Spalte oder Folgeabschnitt
    assert fremde == []  # P8, Z12 sind keine Knotenkennungen


# (e) Eine Zelle, die mit **keine** beginnt, ist Erklärtext.
def test_e_keine_zelle_ist_erklaertext_gruen() -> None:
    risiken, fremde = _weitergaben_lesen(_unterabschnitt(_weitergaben(ZEILE_KEINE), "### Weitergaben"))
    assert risiken == set() and fremde == []
    assert _pruefen("96", _weitergaben(ZEILE_KEINE), set()).fehler == []


def test_e_keine_zelle_bei_gefuehrter_kante_rot() -> None:
    # Die Mappe führt eine Kante, der Bericht verneint sie: ROT über Regel (h).
    lint = _pruefen("96", _weitergaben(ZEILE_KEINE), {"87"})
    assert any(f.startswith("Kanten-Abgleich 96 (Mappe → Bericht):") and "87" in f for f in lint.fehler)


# (f) Eine Knotenkennung außerhalb einer **keine**-Zelle ist keine Risikonummer.
def test_f_kennung_statt_risikonummer_rot() -> None:
    text = _weitergaben(ZEILE_KEINE.replace("| **keine** —", "| S999 —"))
    lint = _pruefen("96", text, set())
    rot = [f for f in lint.fehler if "S999" in f]
    assert len(rot) == 1 and "keine Risikonummer" in rot[0]


def test_f_kennung_neben_risikonummer_rot() -> None:
    lint = _pruefen("95", _weitergaben("| → **#87** über W182 | – |"), {"87"})
    assert any("W182" in f and "keine Risikonummer" in f for f in lint.fehler)


# (g) „Ergänzte Kanten aus Abgleich (eingehend)“ ist nur eingehend.
KOPF_NETZ = ["Id", "Name", "Input_IDs_Wirkung", "Output_IDs_Wirkung",
             "Ergänzte Kanten aus Abgleich (eingehend)", "Anmerkung"]


def test_g_ergaenzte_kanten_nur_eingehend() -> None:
    aus, ein = _netzwerk_kanten(KOPF_NETZ, (101, "Verletzungen", "12; 43; 95", None, "12; 95", None))
    assert aus == set()
    assert ein == {"12", "43", "95"}


def test_g_output_ids_ausgehend() -> None:
    aus, ein = _netzwerk_kanten(KOPF_NETZ, (95, "Hitzebelastung", "62; 63", "87; 101", None, None))
    assert aus == {"87", "101"}
    assert ein == {"62", "63"}


def test_g_ergaenzte_kante_macht_behauptete_kante_nicht_gruen() -> None:
    aus, _ = _netzwerk_kanten(KOPF_NETZ, (101, "Verletzungen", "95", None, "12", None))
    lint = _pruefen("101", _weitergaben("| → **#12** Rutschungen | – |"), aus)
    assert any(f.startswith("Kanten-Abgleich 101 (Bericht → Mappe):") and "12" in f for f in lint.fehler)


# (h) Jede Output-Kante der Mappe steht als #<Zahl> in der ersten Spalte.
def test_h_fehlende_kante_rot() -> None:
    lint = _pruefen("95", _weitergaben(ZEILE_101), {"87", "101"})
    rot = [f for f in lint.fehler if f.startswith("Kanten-Abgleich 95 (Mappe → Bericht):")]
    assert len(rot) == 1 and "87" in rot[0] and "101" not in rot[0]


def test_h_kante_nur_in_zweiter_spalte_rot() -> None:
    lint = _pruefen("95", _weitergaben("| **keine** | → **#87** |"), {"87"})
    assert any(f.startswith("Kanten-Abgleich 95 (Mappe → Bericht):") for f in lint.fehler)


def test_h_ohne_kanten_und_ohne_behauptung_gruen() -> None:
    assert _pruefen("98", _weitergaben("| **keine** — keine Output-Kanten | – |"), set()).fehler == []

"""Schlüsse für die Anpassungsplanung und methodische Grenze aus KWRA 2021, TB 6, Kap. 7 (T-1126-cto).

Konformitätsliste Zeile 10, A10 und A11: Die Schlüsse stehen mit Seite (S. 153–154), das
Handlungserfordernis gilt dem ganzen Bereich „Natürliche Systeme und Ressourcen“, die methodische
Grenze trägt Fußnote 30 und beide Folgen (verzerrtes Bild, nicht alle Wirkbeziehungen erfasst).
"""

from app.data.kwra_kap7_schluesse import (
    METHODISCHE_GRENZE as G,
    SCHLUESSE_ANPASSUNGSPLANUNG as S,
)
from app.data.kwra_querverbindungen import SYSTEMBEREICH_MATRIX

NAT = "Natürliche Systeme und Ressourcen"


def _schluss(kennung):
    return next(e for e in S if e["schluss"] == kennung)


def test_jeder_schluss_hat_seite_153_oder_154_und_eine_aussage():
    assert S
    assert len({e["schluss"] for e in S}) == len(S)
    for e in S:
        assert e["seiten"] and set(e["seiten"]) <= {153, 154}, e["schluss"]
        assert e["titel"].strip() and e["aussage"].strip(), e["schluss"]


def test_a10_kernaussagen_der_schluesse():
    alle = " ".join(e["aussage"] for e in S)
    assert "stärker vom Klimawandel betroffen" in alle
    assert "Anpassungsdauer tendenziell deutlich höher" in alle
    assert "vergleichsweise gering" in alle
    assert "Rückwirkungen auf alle anderen Systembereiche" in alle
    assert "vorgelagerte Klimawirkungen" in alle
    assert "Raumplanung" in _schluss("zielkonflikte_wasser_land_raumplanung")["aussage"]
    assert "Wasserressourcen" in _schluss("zielkonflikte_wasser_land_raumplanung")["aussage"]


def test_handlungserfordernis_fuer_den_ganzen_bereich_nicht_aus_kaskadeneffekten():
    h = _schluss("besonderes_handlungserfordernis")
    assert "besonderes Handlungserfordernis" in h["aussage"]
    assert "Kaskadeneffekten" in h["aussage"]
    assert "ganzer Systembereich" in h["geltungsbereich"] and NAT in h["geltungsbereich"]
    assert h["seiten"] == [154]


def test_mehr_als_die_haelfte_der_ausgehenden_beziehungen_passt_zu_tabelle_28():
    v = _schluss("vorgelagert_mehr_als_die_haelfte")
    summe = sum(z["summe_ausgehend"] for z in SYSTEMBEREICH_MATRIX.values())
    assert v["ausgehend_summe"] == summe == 157
    assert v["ausgehend_natuerliche_systeme"] == SYSTEMBEREICH_MATRIX[NAT]["summe_ausgehend"] == 80
    assert 2 * v["ausgehend_natuerliche_systeme"] > v["ausgehend_summe"]


def test_a11_methodische_grenze_mit_fussnote_30():
    assert G["fussnote"] == 30
    assert G["seiten"] == [153, 154]
    assert "vorgelagerten Klimawirkungen" in G["aussage"]
    assert "verzerrt" in G["aussage"]
    assert "alle Wirkbeziehungen" in G["aussage"]
    assert "Anpassungskapazitäten" in G["fussnote_text"] and "S. 153" in G["fussnote_text"]
    assert len(G["folgen"]) == 2

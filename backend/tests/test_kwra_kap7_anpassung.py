"""Bereichsvergleich der Anpassungsfähigkeit aus KWRA 2021, Teilbericht 6, Kap. 7 (T-1125-cto).

Prüft die übernommenen Aussagen gegen die Stellen der Quelle (S. 146–154): Wirksamkeit,
Klimarisiko mit Anpassung, Anpassungsdauer und Grenzen je Systembereich; für naturferne
Wirtschaftssysteme (S. 150) und Menschen und soziale Systeme (S. 151) keine valide Aussage.
"""

from app.data import catalog
from app.data.kwra_kap7_anpassung import (
    BEREICHSVERGLEICH_ANPASSUNG as V,
    BLOECKE,
    bereiche_ohne_valide_aussage,
)

B = catalog.KWRA_SYSTEMBEREICHE


def test_genau_die_fuenf_bereiche_in_katalogreihenfolge():
    assert tuple(V) == B


def test_jeder_block_hat_seiten_aus_kapitel_7_und_eine_aussage():
    for b in B:
        assert set(V[b]) >= set(BLOECKE), b
        for k in BLOECKE:
            eintrag = V[b][k]
            assert eintrag["seiten"], (b, k)
            assert set(eintrag["seiten"]) <= set(range(146, 155)), (b, k)
            assert isinstance(eintrag["valide_aussage"], bool), (b, k)
            assert eintrag["aussage"].strip(), (b, k)


def test_keine_valide_aussage_zur_wirksamkeit_wo_die_quelle_das_sagt():
    assert [V[b]["wirksamkeit"]["valide_aussage"] for b in B] == [True, True, True, False, False]
    assert bereiche_ohne_valide_aussage() == ["Naturferne Wirtschaftssysteme", "Menschen und soziale Systeme"]
    assert V["Naturferne Wirtschaftssysteme"]["wirksamkeit"]["seiten"] == [150]
    assert V["Naturferne Wirtschaftssysteme"]["wirksamkeit"]["anzahl_untersucht"] == 1
    assert V["Menschen und soziale Systeme"]["wirksamkeit"]["seiten"] == [151]
    assert V["Menschen und soziale Systeme"]["wirksamkeit"]["anzahl_untersucht"] == 3


def test_ohne_valide_aussage_steht_kein_wert():
    for b in B:
        for k in BLOECKE:
            eintrag = V[b][k]
            if not eintrag["valide_aussage"]:
                assert "vergleich" not in eintrag, (b, k)
                assert not eintrag.get("klimawirkungen"), (b, k)


def test_grenzen_natuerliche_und_naturnutzende_systeme():
    g = V["Natürliche Systeme und Ressourcen"]["grenzen"]
    assert g["anzahl_ohne_anpassungsmoeglichkeit"] == len(g["klimawirkungen"]) == 4
    assert 147 in g["seiten"]
    g = V["Naturnutzende Wirtschaftssysteme"]["grenzen"]
    assert g["anzahl_ohne_anpassungsmoeglichkeit"] == 0 and g["seiten"] == [148]


def test_klimarisiko_mit_anpassung():
    k = V["Natürliche Systeme und Ressourcen"]["klimarisiko_mit_anpassung"]
    assert len(k["klimawirkungen"]) == 5 and k["seiten"] == [147]
    k = V["Naturnutzende Wirtschaftssysteme"]["klimarisiko_mit_anpassung"]
    assert (k["anzahl_mittel_hoch"], k["anzahl_bewertet"]) == (6, 11)
    assert len(k["klimawirkungen"]) == 6
    k = V["Infrastrukturen und Gebäude"]["klimarisiko_mit_anpassung"]
    assert "gering-mittel" in k["aussage"] and 150 in k["seiten"]


def test_anpassungsdauer():
    assert "über 50 Jahre" in V["Natürliche Systeme und Ressourcen"]["anpassungsdauer"]["aussage"]
    assert "weniger als zehn Jahren" in V["Naturferne Wirtschaftssysteme"]["anpassungsdauer"]["aussage"]
    assert "zwei Drittel" in V["Menschen und soziale Systeme"]["anpassungsdauer"]["aussage"]
    assert all(V[b]["anpassungsdauer"]["valide_aussage"] for b in B)

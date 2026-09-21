"""Fundament der Verwechslungssperre Klasse A/B im Katalog (T-0513).

Prüft NO_EURO_LAYER_TEXT, risk_has_euro_layer() und euro_coverage() —
noch ohne echten Klasse-B-Eintrag im Bestand (siehe Folgetickets).
"""

from app.data import catalog


def test_no_euro_layer_text_wortlaut():
    assert catalog.NO_EURO_LAYER_TEXT == "Screening ohne Euro-Bezifferung"


def test_risk_has_euro_layer_klasse_a_und_b():
    for r in catalog.RISKS:
        assert catalog.risk_has_euro_layer(r) is True

    klasse_b_testeintrag = {"code": "TEST_KLASSE_B", "euro_layer": False}
    assert catalog.risk_has_euro_layer(klasse_b_testeintrag) is False


def test_euro_coverage_voller_katalog():
    ergebnis = catalog.euro_coverage()
    assert ergebnis.covered == ergebnis.total == len(catalog.RISKS)


def test_euro_coverage_mit_klasse_b_testeintrag():
    klasse_b_testeintrag = {"code": "TEST_KLASSE_B", "euro_layer": False}
    risiken = list(catalog.RISKS) + [klasse_b_testeintrag]

    ergebnis = catalog.euro_coverage(risiken)

    assert ergebnis.total == len(catalog.RISKS) + 1
    assert ergebnis.covered == len(catalog.RISKS)
    assert ergebnis.text.endswith("Klimawirkungen in Euro beziffert")

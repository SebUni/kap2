"""Teil 6 des PDF-Ergebnisberichts: Maßnahmen (T-1419).

Beispieldatensatz: vier Maßnahmen aus dem Katalog, deren ``impact_summary`` so gebaut ist wie in
``measure_service.compute_impact`` — Kosten und Kostenkomponenten samt Quelle echt aus
``compute_costs``, der Nutzen je Jahr als Testwert. Drei sind in Euro beziffert (in bewusst
falscher Eingabereihenfolge), eine ist qualitativ (Vermerk ``benefit_display`` statt Betrag, wie
bei der allergenarmen Baumwahl ohne Baumkronendaten).

Geprüft wird (a) die Rangfolge absteigend nach Nutzen-Kosten-Verhältnis, (b) CAPEX, OPEX je Jahr,
vermiedene Schäden je Jahr und je Kostenkomponente eine Quelle, (c) Gewissheit und Umsetzung
gleich den Spalten „Gewissheit“ und „Umsetzung“ des Maßnahmen-Excel (Paket 12), (d) die
qualitative Maßnahme mit Vermerk „qualitativ“ und ohne Euro-Betrag; dazu die harten Regeln
an Teil 6 und der Fall ohne Maßnahmen.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import sys
from types import SimpleNamespace

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
sys.path.insert(0, BACKEND)
sys.path.insert(0, HIER)

from test_ergebnisbericht_regeln import REGELN, Element, baum, html_text  # noqa: E402

# (Code, Name, Ort, Umsetzungsjahr, Anzahl, Fläche m², vermiedene Schäden je Jahr)
BEZIFFERT = [
    ("VULNERABLE_GROUP_PROGRAMS", "Besuchsdienst für Ältere", "Ortsteil Warmsen", 2028, 1, 0.0,
     6_000.0),
    ("COOLING_ROOMS_DRINKING_WATER", "Kühlräume und Trinkwasser", "Rathaus und Dorfgemeinschaftshaus",
     2027, 2, 0.0, 9_000.0),
    ("HEAT_ACTION_PLANS", "Hitzeaktionsplan", "ganze Kommune", 2027, 1, 0.0, 30_000.0),
]
QUALITATIV_CODE = "LOW_ALLERGEN_TREE_SELECTION"


def _summary(code: str, anzahl: int, flaeche: float, nutzen: float | None) -> dict:
    from app.data import catalog
    from app.services import measure_service as ms

    mdef = catalog.MEASURES_BY_CODE[code]
    kosten = ms.compute_costs(mdef, anzahl, flaeche)
    s = {
        "measure_type": code, "affected_area_m2": flaeche,
        "capex_eur": kosten["capex"]["total_eur"], "opex_annual_eur": kosten["opex"]["total_eur"],
        "cost_breakdown": kosten,
        "annual_benefit_damage_eur": nutzen or 0.0, "annual_benefit_flat_eur": 0.0,
        "annual_benefit_direct_eur": 0.0, "annual_benefit_eur": nutzen or 0.0,
    }
    if nutzen is None:
        s["benefit_display"] = ms.STADTBAUM_NO_CANOPY_TEXT
    return s


@pytest.fixture(scope="module")
def zeilen():
    from app.services.ergebnisbericht.massnahmen import massnahmenzeile
    z = [massnahmenzeile(code, name, _summary(code, n, f, nutzen), ort=ort, umsetzungsjahr=j)
         for code, name, ort, j, n, f, nutzen in BEZIFFERT]
    z.insert(1, massnahmenzeile(QUALITATIV_CODE, "Allergenarme Baumwahl",
                                _summary(QUALITATIV_CODE, 0, 0.0, None),
                                ort="Neupflanzungen an Straßen", umsetzungsjahr=2027))
    return z


def _daten(massnahmen):
    from app.services.ergebnisbericht.beispiel import beispiel
    from app.services.ergebnisbericht.sammler import Stand
    return SimpleNamespace(
        kommune=beispiel("warmsen"), massnahmen=massnahmen,
        beziffert_text="1 von 3 Klimawirkungen in Euro beziffert",
        stand=Stand("Fassung 0.1", "#95", "M", "Zensus 2022", dt.date(2026, 9, 29)))


@pytest.fixture(scope="module")
def teil6(zeilen) -> Element:
    from app.services.ergebnisbericht.teile import teil_6
    return baum(f'<html><body><section class="teil">{teil_6(_daten(zeilen))}</section></body></html>')


def _bloecke(w: Element) -> list[Element]:
    return [e for e in w.alle() if e.tag == "div" and "massnahme" in e.klassen]


def _zelle(block: Element, klasse: str) -> Element:
    treffer = [e for e in block.alle() if e.tag == "td" and klasse in e.klassen]
    assert len(treffer) == 1, klasse
    return treffer[0]


def _zeilentexte(td: Element) -> list[str]:
    return [e.text() for e in td.alle() if e.tag == "div" and "zeile" in e.klassen]


def test_beispieldatensatz_hat_bezifferte_und_qualitative(zeilen):
    assert sum(not z.qualitativ for z in zeilen) >= 1
    assert sum(z.qualitativ for z in zeilen) >= 1


def test_a_rangfolge_absteigend_nach_nutzen_kosten(teil6, zeilen):
    bloecke = _bloecke(teil6)
    assert len(bloecke) == len(zeilen)
    nach_code = {z.code: z for z in zeilen}
    reihe = [nach_code[b.attrs["data-code"]] for b in bloecke]
    assert [b.attrs["data-rang"] for b in bloecke] == [str(i) for i in range(1, len(zeilen) + 1)]
    bezifferte = [z for z in reihe if not z.qualitativ]
    verhaeltnisse = [z.nutzen_kosten for z in bezifferte]
    assert verhaeltnisse == sorted(verhaeltnisse, reverse=True)
    assert len(set(verhaeltnisse)) == len(verhaeltnisse)   # Rangfolge ist eindeutig
    # Eingabereihenfolge war eine andere: Die Rangfolge kommt aus dem Teil, nicht aus den Daten.
    assert [z.code for z in bezifferte] != [c for c, *_ in BEZIFFERT]
    # Qualitative Maßnahmen stehen hinter allen bezifferten.
    assert all(z.qualitativ for z in reihe[len(bezifferte):])
    # Der gedruckte Wert ist das Verhältnis der Zeile.
    from app.services.ergebnisbericht.teile import de_zahl
    for b, z in zip(bloecke, reihe):
        if not z.qualitativ:
            assert _zelle(b, "verhaeltnis").text() == de_zahl(z.nutzen_kosten, 1)


def test_nutzen_kosten_formel(zeilen):
    from app.services.ergebnisbericht.massnahmen import HORIZONT_ENDE
    z = next(z for z in zeilen if z.code == "HEAT_ACTION_PLANS")
    jahre = HORIZONT_ENDE - 2027 + 1
    assert z.nutzen_kosten == pytest.approx(30_000.0 * jahre / (z.capex_eur + z.opex_eur * jahre))


def test_b_bezifferte_zeigen_capex_opex_vermieden_und_quelle_je_komponente(teil6, zeilen):
    from app.services.ergebnisbericht.teile import de_euro
    nach_code = {z.code: z for z in zeilen}
    geprueft = 0
    for b in _bloecke(teil6):
        z = nach_code[b.attrs["data-code"]]
        if z.qualitativ:
            continue
        geprueft += 1
        for klasse, wert in (("capex", z.capex_eur), ("opex", z.opex_eur),
                             ("vermieden", z.vermiedene_schaeden_eur)):
            betraege = _zelle(b, klasse).mit_klasse("betrag")
            assert len(betraege) == 1, (z.code, klasse)
            assert betraege[0].text() == de_euro(wert)
        komponenten = [e for e in b.alle() if e.tag == "tr" and "komponente" in e.klassen]
        assert len(komponenten) == len(z.komponenten) >= 1
        assert {e.attrs["data-block"] for e in komponenten} == {"capex", "opex"}
        for tr, k in zip(komponenten, z.komponenten):
            quelle = _zelle(tr, "quelle").text().strip()
            assert quelle and quelle == k.quelle
    assert geprueft == len(BEZIFFERT)


def test_b_quellen_kommen_aus_dem_katalog(zeilen):
    from app.data import catalog
    for z in zeilen:
        mdef = catalog.MEASURES_BY_CODE[z.code]
        for k in z.komponenten:
            assert k.quelle in {s for s in (mdef.get("sources") or {}).values()} | {mdef.get("source")}


def test_b_komponente_ohne_quelle_bricht_ab():
    from app.services.ergebnisbericht.massnahmen import massnahmenzeile
    s = _summary("HEAT_ACTION_PLANS", 1, 0.0, 1000.0)
    s["cost_breakdown"]["capex"]["components"][0]["source"] = ""
    with pytest.raises(ValueError):
        massnahmenzeile("HEAT_ACTION_PLANS", "x", s, ort="ganze Kommune", umsetzungsjahr=2027)


def test_c_gewissheit_und_umsetzung_wie_im_massnahmen_excel(teil6, zeilen):
    """Dieselben Zellentexte, mit denen ``export_measures_xlsx`` die Spalten füllt."""
    from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
    from app.services import massnahmen_gewissheit as mg
    from app.services.ergebnisbericht.massnahmen import ohne_ablageort
    from app.services.export_service import gewissheit_text, umsetzung_text

    gewissheit = {g["code"]: g for g in mg.massnahmen_gewissheit()}
    bloecke = _bloecke(teil6)
    assert {b.attrs["data-code"] for b in bloecke} == {z.code for z in zeilen}
    for b in bloecke:
        code = b.attrs["data-code"]
        excel_g = gewissheit_text(gewissheit.get(code))
        excel_u = umsetzung_text(MASSNAHMEN_UMSETZUNG.get(code))
        assert excel_g != "nicht hinterlegt" and excel_u != "nicht hinterlegt"
        assert _zeilentexte(_zelle(b, "gewissheit")) == excel_g.split("\n")
        # Umsetzung: Zeile für Zeile wie im Excel, nur ohne den Ablagevermerk „abgelegt unter
        # docs/…“ (harte Regel 4). Alle Werte — Träger, Ebenen, Partner, Quelle, Seite — bleiben.
        pdf_u = _zeilentexte(_zelle(b, "umsetzung"))
        excel_zeilen = excel_u.split("\n")
        assert len(pdf_u) == len(excel_zeilen)
        for p, x in zip(pdf_u, excel_zeilen):
            assert p == ohne_ablageort(x)
            assert "docs/" not in p
            # Unabhängig von der Funktion: Der Unterschied zum Excel besteht nur aus Einschüben
            # im Excel-Text, und jeder Einschub ist ein Ablagevermerk.
            import difflib
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, p, x, autojunk=False).get_opcodes():
                if op == "equal":
                    continue
                assert op == "insert", (op, p[i1:i2], x[j1:j2])
                assert re.fullmatch(r";?\s*abgelegt unter docs/\S*?", x[j1:j2]), x[j1:j2]


def test_c_ablagevermerk_entfernt_nur_den_pfad():
    from app.services.ergebnisbericht.massnahmen import ohne_ablageort
    x = ("Quelle: BMU, Handlungsempfehlungen, https://example.org/hap.pdf (PDF-Seite gleich gedruckter "
         "Seite; abgelegt unter docs/quellen/hitzeaktionsplaene/hap.pdf), S. 12")
    assert ohne_ablageort(x) == ("Quelle: BMU, Handlungsempfehlungen, https://example.org/hap.pdf "
                                 "(PDF-Seite gleich gedruckter Seite), S. 12")
    assert ohne_ablageort("Kommune allein") == "Kommune allein"


def test_c_excel_fuellt_spalten_mit_denselben_funktionen():
    """Die Spalten „Gewissheit“ und „Umsetzung“ des Excel stehen am Ende und werden mit
    ``gewissheit_text``/``umsetzung_text`` gefüllt — sonst wäre der Vergleich oben keiner."""
    import inspect

    from app.services import export_service
    quelle = inspect.getsource(export_service.export_measures_xlsx)
    assert '"Gewissheit", "Umsetzung",' in quelle
    assert "gewissheit_text(gewissheit_map.get(m.measure_type))" in quelle
    assert "umsetzung_text(MASSNAHMEN_UMSETZUNG.get(m.measure_type))" in quelle


def test_d_qualitative_massnahme_mit_vermerk_ohne_euro(teil6, zeilen):
    qualitative = [b for b in _bloecke(teil6) if b.attrs.get("data-qualitativ") == "ja"]
    assert [b.attrs["data-code"] for b in qualitative] == [QUALITATIV_CODE]
    b = qualitative[0]
    assert [e.text() for e in b.mit_klasse("qualitativ")] == ["qualitativ"]
    assert "qualitativ" in _zelle(b, "vermieden").text()
    assert not b.mit_klasse("betrag")
    assert "€" not in b.text() and "Euro-Betrag" not in b.text()


def test_ohne_massnahmen_steht_der_grund():
    from app.services.ergebnisbericht.teile import teil_6
    w = baum(f'<html><body><section class="teil">{teil_6(_daten([]))}</section></body></html>')
    assert not _bloecke(w)
    assert "keine Maßnahme angelegt" in w.text()
    for nr in sorted(REGELN):
        assert REGELN[nr](w, [html_text(w)]) == []


def test_teil6_im_bericht_registriert():
    from app.services.ergebnisbericht.teile import TEILE, UEBERSCHRIFTEN
    assert 6 in TEILE and UEBERSCHRIFTEN[6] == "Teil 6 · Maßnahmen"


@pytest.mark.parametrize("nr", sorted(REGELN))
def test_harte_regeln_an_teil_6(teil6, nr):
    assert REGELN[nr](teil6, [html_text(teil6)]) == []

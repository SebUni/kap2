"""Teil 6 des Ergebnisberichts: CAPEX „–“ bei offenen Kosten, Einleitung und s_unbek-Hinweis (T-1810).

Die Zeilen entstehen mit ``massnahmenzeile()`` aus einem summary in der Form von
``measure_service._stadtbaum_kosten``; ``extra`` wird nicht von Hand gesetzt.
"""

from __future__ import annotations

import datetime as dt
import os
import sys
from types import SimpleNamespace

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))

from test_ergebnisbericht_regeln import REGELN, baum, html_text  # noqa: E402

KATALOG_TEXT = "keine Investition im Katalog hinterlegt"
HINWEIS = ("Der Ausgangslauf ist älter und speichert den Anteil der Kronen ohne Gattung noch "
           "nicht. Die Senkung rechnet mit dem heutigen Wert. Rechnen Sie den Ausgangslauf neu.")


def _summary(felder: dict | None = None, *, capex: float = 0.0) -> dict:
    s = {
        "measure_type": "HEAT_ACTION_PLANS", "affected_area_m2": 0.0,
        "capex_eur": capex, "opex_annual_eur": 0.0,
        "cost_breakdown": {"capex": {"components": []}, "opex": {"components": []}},
        "annual_benefit_damage_eur": 5_000.0, "annual_benefit_flat_eur": 0.0,
        "annual_benefit_direct_eur": 0.0, "annual_benefit_eur": 5_000.0,
    }
    s.update(felder or {})
    return s


def _summary_kein_fall() -> dict:
    from app.services.measure_service import STADTBAUM_FALL_WAEHLEN_TEXT
    return _summary({
        "kosten_nutzen_kennzahl_offen": True,
        "capex_je_fall": {"nachpflanzung": 12_000.0, "vorgezogen": 48_000.0},
        "kosten_vermerk": STADTBAUM_FALL_WAEHLEN_TEXT,
    })


def _summary_baumzahl_fehlt() -> dict:
    from app.services.measure_service import STADTBAUM_COUNT_FEHLT_TEXT
    return _summary({
        "kosten_nutzen_kennzahl_offen": True,
        "kosten_vermerk": STADTBAUM_COUNT_FEHLT_TEXT,
    })


def _zeile(summary: dict, name: str = "Stadtbaumwahl", code: str = "HEAT_ACTION_PLANS"):
    from app.services.ergebnisbericht.massnahmen import massnahmenzeile
    return massnahmenzeile(code, name, summary, ort="Straßen", umsetzungsjahr=2027)


def _html(zeilen: list) -> str:
    from app.services.ergebnisbericht.sammler import Stand
    from app.services.ergebnisbericht.teile import teil_6
    from app.services.ergebnisbericht.beispiel import beispiel
    d = SimpleNamespace(
        kommune=beispiel("warmsen"), massnahmen=list(zeilen),
        beziffert_text="1 von 3 Klimawirkungen in Euro beziffert",
        stand=Stand("Fassung 0.1", "#95", "M", "Zensus 2022", dt.date(2026, 9, 29)))
    return f'<html><body><section class="teil">{teil_6(d)}</section></body></html>'


def _zelle(html: str, klasse: str, code: str | None = None) -> str:
    wurzel = baum(html)
    for block in wurzel.mit_klasse("massnahme"):
        if code is None or block.attrs.get("data-code") == code:
            return block.mit_klasse(klasse)[0].text()
    raise AssertionError(f"kein Block für {code}")


def test_massnahmenzeile_uebernimmt_hinweis():
    z = _zeile(_summary({"stadtbaum_s_unbek_hinweis": HINWEIS}))
    assert z.extra["stadtbaum_s_unbek_hinweis"] == HINWEIS


def test_massnahmenzeile_ohne_hinweis_bleibt_leer():
    z = _zeile(_summary())
    assert not z.extra.get("stadtbaum_s_unbek_hinweis")


def test_capex_kein_fall_gewaehlt():
    from app.services.measure_service import STADTBAUM_FALL_WAEHLEN_TEXT
    z = _zeile(_summary_kein_fall())
    assert z.kosten_offen and z.nutzen_kosten is None
    capex = _zelle(_html([z]), "capex")
    assert capex.startswith("–")
    assert STADTBAUM_FALL_WAEHLEN_TEXT in capex
    assert "0 €" not in capex
    assert KATALOG_TEXT not in capex


def test_capex_baumzahl_fehlt():
    from app.services.measure_service import STADTBAUM_COUNT_FEHLT_TEXT
    z = _zeile(_summary_baumzahl_fehlt())
    assert z.kosten_offen and z.nutzen_kosten is None
    capex = _zelle(_html([z]), "capex")
    assert capex.startswith("–")
    assert STADTBAUM_COUNT_FEHLT_TEXT in capex
    assert "0 €" not in capex
    assert KATALOG_TEXT not in capex


def test_capex_null_ohne_kosten_offen_bleibt_katalogsatz():
    z = _zeile(_summary())
    assert not z.kosten_offen and z.capex_eur == 0.0
    capex = _zelle(_html([z]), "capex")
    assert capex == KATALOG_TEXT


def test_einleitung_nennt_zeilen_mit_kosten_offen():
    html = _html([_zeile(_summary_kein_fall(), "Stadtbaumwahl", "STADTBAUM"),
                  _zeile(_summary_baumzahl_fehlt(), "Zweite Baumwahl", "BAUM_2")])
    erster = next(e for e in baum(html).alle()
                  if e.tag == "p" and "Nutzen-Kosten-Verhältnis" in e.text())
    text = erster.text()
    assert "2 Maßnahme(n) zeigen „Kosten offen“" in text
    assert "zwischen den bezifferten und den qualitativen Maßnahmen" in text


def test_einleitung_ohne_kosten_offen_unveraendert():
    html = _html([_zeile(_summary())])
    assert "Kosten offen" not in html
    assert "zwischen den bezifferten" not in html


def test_einleitung_reihenfolge_zwischen_bezifferten_und_qualitativen():
    qual = _summary({"benefit_display": "Keine Wirkung in Euro."})
    qual["annual_benefit_damage_eur"] = 0.0
    qual["annual_benefit_eur"] = 0.0
    html = _html([_zeile(qual, "Qualitative", "QUAL"),
                  _zeile(_summary_kein_fall(), "Offene", "OFFEN"),
                  _zeile(_summary({"opex_annual_eur": 100.0}), "Bezifferte", "BEZ")])
    codes = [b.attrs["data-code"] for b in baum(html).mit_klasse("massnahme")]
    assert codes == ["BEZ", "OFFEN", "QUAL"]


def test_hinweis_steht_im_block_der_massnahme():
    html = _html([
        _zeile(_summary_kein_fall() | {"stadtbaum_s_unbek_hinweis": HINWEIS}, "Stadtbaumwahl",
               "STADTBAUM"),
        _zeile(_summary({"opex_annual_eur": 100.0}), "Andere", "ANDERE"),
    ])
    blocks = {b.attrs["data-code"]: b.text() for b in baum(html).mit_klasse("massnahme")}
    assert HINWEIS in blocks["STADTBAUM"]
    assert HINWEIS not in blocks["ANDERE"]


def test_ohne_hinweisfeld_kein_hinweis():
    html = _html([_zeile(_summary_kein_fall(), "Stadtbaumwahl", "STADTBAUM")])
    assert baum(html).mit_klasse("hinweis") == []
    assert "s_unbek" not in html


def test_regeln_am_html_mit_hinweis_und_offenen_kosten():
    html = _html([
        _zeile(_summary_kein_fall() | {"stadtbaum_s_unbek_hinweis": HINWEIS}, "Stadtbaumwahl",
               "STADTBAUM"),
        _zeile(_summary_baumzahl_fehlt(), "Zweite Baumwahl", "BAUM_2"),
    ])
    wurzel = baum(html)
    for nr, regel in REGELN.items():
        assert regel(wurzel, [html_text(wurzel)]) == [], f"Regel {nr}"

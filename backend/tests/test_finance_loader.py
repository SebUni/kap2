"""Tests des finance_loader (Dashboard-Kopf: BIP Kreisebene, Kommunalhaushalt Ø 5 J.).

DB- und netzfrei: der jahressensitive ffcsv-Parser, die 5-Jahres-Mittelung und
die Payload-Assembly werden mit synthetischen GENESIS-ffcsv-Fixtures geprüft;
Netz-Zugriffe werden gemonkeypatcht. Dazu die Landkreis-Ableitung aus
Nominatim-Adressen (osm_service).

Läuft mit pytest oder direkt: ``python tests/test_finance_loader.py``.
"""

from __future__ import annotations

import pytest

from app.services import finance_loader, inkar_loader, osm_service

AGS_OSCHATZ = "14730310"   # Gemeinde (Kreis Nordsachsen = 14730)

# Reales GENESIS-Flatfile-CSV (data/tablefile, ffcsv): spaltenbenannt mit
# englischen Keys, ``value`` als Messwert, ``value_variable_code`` als Kennzahl,
# ``N_variable_attribute_code`` als Regionalschlüssel.
FLAT_HDR = (
    "statistics_code;statistics_label;time_code;time_label;time;"
    "1_variable_code;1_variable_label;1_variable_attribute_code;1_variable_attribute_label;"
    "value;value_unit;value_variable_code;value_variable_label"
)


def _row(year, region, value, *, vvc="", unit="EUR", rvcode="GEMEIND", stat="71717") -> str:
    return (f"{stat};Fin;JAHR;Jahr;{year};{rvcode};Regionalebene;{region};Label;"
            f"{value};{unit};{vvc};Kennzahl")


def _rows(*rows: str) -> str:
    return "\n".join([FLAT_HDR, *rows])


# ── parse_ffcsv_series ─────────────────────────────────────────────────────────

def test_series_gemeinde_vs_kreis_strictly_separated():
    """Kreiszeilen dürfen NIE als Gemeindewert durchgehen (und umgekehrt) —
    Regionalschlüssel wird über ``1_variable_attribute_code`` exakt gematcht."""
    text = _rows(
        _row(2021, "14730310", "12345,6", rvcode="GEMEIND"),
        _row(2021, "14730", "999999,9", rvcode="KREISE"),
        _row(2022, "14730310", "13000,0", rvcode="GEMEIND"),
    )
    gemeinde = finance_loader.parse_ffcsv_series(text, AGS_OSCHATZ)
    assert gemeinde == {2021: 12345.6, 2022: 13000.0}
    kreis = finance_loader.parse_ffcsv_series(text, AGS_OSCHATZ, kreis_level=True)
    assert kreis == {2021: 999999.9}


def test_series_selects_value_variable():
    """Mehrere Kennzahlen je Region/Jahr (BIP gesamt/je Erwerbstätigem/pro Kopf) —
    ``value_variable`` wählt die gewünschte, statt „letzte Zeile gewinnt"."""
    text = _rows(
        _row(2023, "14730", "7547730", vvc="BIP802", unit="Tsd. EUR", rvcode="KREISE"),
        _row(2023, "14730", "78862", vvc="BIP803", rvcode="KREISE"),
        _row(2023, "14730", "37785", vvc="BIP804", rvcode="KREISE"),
    )
    assert finance_loader.parse_ffcsv_series(
        text, "14730", kreis_level=True, value_variable="BIP802") == {2023: 7547730.0}
    assert finance_loader.parse_ffcsv_series(
        text, "14730", kreis_level=True, value_variable="BIP804") == {2023: 37785.0}


def test_series_matches_12_digit_ars_via_trailing_zeros():
    text = _rows(_row(2022, "147300000000", "3601,2", vvc="BIP802", rvcode="KREISE"))
    assert finance_loader.parse_ffcsv_series(
        text, AGS_OSCHATZ, kreis_level=True, value_variable="BIP802") == {2022: 3601.2}
    # Aber: Gemeinde-Suffix ist KEIN Trailing-Zero-Treffer für den Kreis.
    text2 = _rows(_row(2022, "14730310", "42,0", rvcode="GEMEIND"))
    assert finance_loader.parse_ffcsv_series(text2, "14730", kreis_level=True) == {}


def test_series_skips_missing_value_markers():
    text = _rows(
        _row(2020, "14730310", "-"),
        _row(2021, "14730310", "..."),
        _row(2022, "14730310", "13000,0"),
    )
    assert finance_loader.parse_ffcsv_series(text, AGS_OSCHATZ) == {2022: 13000.0}


def test_series_german_decimals_and_thousands():
    text = _rows(_row(2022, "14730310", "1.234.567,8"))
    assert finance_loader.parse_ffcsv_series(text, AGS_OSCHATZ) == {2022: 1234567.8}


def test_series_empty_inputs():
    assert finance_loader.parse_ffcsv_series("", AGS_OSCHATZ) == {}
    assert finance_loader.parse_ffcsv_series(FLAT_HDR, AGS_OSCHATZ) == {}
    assert finance_loader.parse_ffcsv_series("x;y;z", "") == {}


# ── average_last_n ─────────────────────────────────────────────────────────────

def test_average_last_n():
    series = {2016: 1.0, 2017: 2.0, 2018: 3.0, 2019: 4.0, 2020: 5.0, 2021: 6.0, 2022: 7.0}
    mean, years = finance_loader.average_last_n(series, 5)
    assert years == [2018, 2019, 2020, 2021, 2022]
    assert mean == pytest.approx(5.0)
    # Weniger Jahre als n vorhanden → Ø über alles Vorhandene.
    mean3, years3 = finance_loader.average_last_n({2020: 1.0, 2021: 2.0, 2022: 3.0}, 5)
    assert years3 == [2020, 2021, 2022] and mean3 == pytest.approx(2.0)
    assert finance_loader.average_last_n({}, 5) is None
    assert finance_loader.average_last_n(series, 0) is None


# ── fetch_finance-Assembly (Netz gemockt) ──────────────────────────────────────

def test_fetch_finance_gdp_only(monkeypatch):
    """fetch_finance liefert nur BIP (BIP802, Tsd.€→Mio.€); Budget kommt separat
    aus dem Bulk-Store, nicht mehr hier."""
    from app.config import settings

    gdp_text = _rows(
        _row(2021, "14730", "3456700", vvc="BIP802", unit="Tsd. EUR", rvcode="KREISE"),
        _row(2022, "14730", "3601200", vvc="BIP802", unit="Tsd. EUR", rvcode="KREISE"),
        _row(2022, "14730", "37785", vvc="BIP804", unit="EUR", rvcode="KREISE"),
    )

    def fake_ffcsv(table_code, regionalkey):
        assert table_code == settings.REGIONALSTATISTIK_TABLE_GDP
        assert regionalkey == "14730"  # Kreis-Schlüssel
        return gdp_text

    monkeypatch.setattr(finance_loader, "_genesis_table_ffcsv", fake_ffcsv)
    payload = finance_loader.fetch_finance(AGS_OSCHATZ)
    assert payload == {"gdp": {"gdp_meur": 3601.2, "gdp_per_capita_eur": 37785.0,
                               "gdp_year": 2022, "level": "kreis"}}


def test_finance_for_kommune_merges_bulk_budget(monkeypatch):
    """finance_for_kommune führt BIP (GENESIS) und Kommunalhaushalt (Bulk-Store,
    via Name) zusammen."""
    from app.services import finance_bulk

    monkeypatch.setattr(finance_loader, "_gdp_for_osm",
                        lambda d, o: ({"gdp": {"gdp_meur": 3601.2, "gdp_year": 2022, "level": "kreis"}},
                                      "14730230"))
    monkeypatch.setattr(inkar_loader, "_auth_headers", lambda: {"username": b"x", "password": b""})
    monkeypatch.setattr(finance_bulk, "budget_for_kommune",
                        lambda ags, name: {"avg_expenditure_eur": 24_000_000.0,
                                           "years": [2021, 2022, 2023], "level": "gemeinde"}
                        if name == "Oschatz" and ags == "14730230" else None)

    payload = finance_loader.finance_for_kommune("relation/535244", "Oschatz")
    assert payload["gdp"]["gdp_meur"] == 3601.2
    assert payload["budget"]["avg_expenditure_eur"] == pytest.approx(24_000_000.0)


def test_finance_for_kommune_without_credentials_returns_none(monkeypatch):
    from app.services import inkar_loader
    monkeypatch.setattr(inkar_loader, "_auth_headers", lambda: None)
    assert finance_loader.finance_for_kommune("535244") is None
    assert finance_loader.finance_for_kommune(None) is None


def test_finance_for_kommune_never_raises(monkeypatch):
    from app.services import inkar_loader
    monkeypatch.setattr(inkar_loader, "_auth_headers", lambda: {"username": "x", "password": "y"})
    monkeypatch.setattr(finance_loader, "_read_cache", lambda _: None)
    monkeypatch.setattr(finance_loader, "_write_cache", lambda *a: None)

    def boom(_osm):
        raise RuntimeError("Overpass down")

    monkeypatch.setattr(inkar_loader, "resolve_ags", boom)
    assert finance_loader.finance_for_kommune("535244") is None


# ── Landkreis-Ableitung (osm_service) ──────────────────────────────────────────

def test_landkreis_from_address():
    assert osm_service.landkreis_from_address(
        {"county": "Landkreis Nordsachsen", "state": "Sachsen"}
    ) == "Landkreis Nordsachsen"
    # Stadtstaat: city=Bundesland darf nicht als Landkreis durchgehen.
    assert osm_service.landkreis_from_address({"city": "Berlin", "state": "Berlin"}) is None
    # Kreisfreie Stadt ohne county → None (Meta-Eintrag entfällt).
    assert osm_service.landkreis_from_address({"city": "Leipzig", "state": "Sachsen"}) is None
    # Fallback district, aber Bundesland-Werte abgelehnt.
    assert osm_service.landkreis_from_address({"district": "Landkreis Fulda"}) == "Landkreis Fulda"
    assert osm_service.landkreis_from_address({"county": "Sachsen"}) is None
    assert osm_service.landkreis_from_address(None) is None


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))

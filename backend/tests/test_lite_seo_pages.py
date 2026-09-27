"""SEO-Seitenbeschreibung der Lite-Seiten (T-1290-ceo, Nachlese zu T-1195-ceo).

``_render_page`` darf in der Meta-Beschreibung keine Klimawirkungen nennen, die
nicht aus den Zeilen der Seite (``rows``) kommen — sonst ein Versprechen, das
die Seite nicht hält (A-0010/P2).
"""
from __future__ import annotations

from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.services.lite import seo_pages

AGS = "14612000"
KLASSE_A_CODE = "EXPECTED_ANNUAL_MORTALITY"


def test_beschreibung_nennt_keine_gefahren_ausserhalb_der_zeilen():
    gemeinde = Gemeinde(ags=AGS, name="Dresden", bez="Stadt", bundesland="Sachsen",
                        population=560000, area_km2=328.8)
    rows = [
        GemeindeLiteResult(ags=AGS, risk_code=KLASSE_A_CODE, index_value=61.5,
                           outcome_value=12.0, outcome_unit="Todesfälle/Jahr",
                           cost_eur=123456.0, drivers={}),
    ]
    html_seite = seo_pages._render_page(gemeinde, rows, bl_means={}, de_means={})
    beschreibung = html_seite.split('name="description" content="', 1)[1].split('"', 1)[0]

    # Die alte Beschreibung nannte pauschal "Hitze, Starkregen und Dürre", auch wenn
    # die Seite nur eine (andere) Klimawirkung zeigt — das ist ein Versprechen, das
    # die Seite nicht hält.
    assert "Hitze, Starkregen und Dürre" not in beschreibung
    for gefahr in ("Hitze", "Starkregen", "Dürre"):
        assert gefahr not in beschreibung

"""KWRA-Charakterisierungsgruppe je Klimawirkung (Konformitäts-Checkliste Zeile 7).

KWRA 2021 (Teilbericht 6, Kap. 6.2, S. 140–143, Tabelle 27) teilt Klimawirkungen mit
sehr dringenden Handlungserfordernissen in fünf Gruppen ein — Umsetzung, Entwicklung,
Entwicklung unter Unsicherheit, Innovation, Innovation unter Unsicherheit — nach zwei
Fragen: Reichen die Maßnahmen aus, um das Restrisiko auf ein gesetztes Niveau zu
senken (Anpassungspotenzial)? Und wie sicher ist die Aussage (Gewissheit)?

Das Produkt bildet beide Fragen aus Größen ab, die es selbst führt:

* **Anpassungspotenzial** = relative Risikominderung der Maßnahmen, die der Katalog
  dieser Klimawirkung quantitativ zuordnet (``catalog.MEASURES``, Schlüssel
  ``linked_risk_codes``), bei voller Abdeckung — siehe ``anpassungspotenzial``.
* **Gewissheit** = Gewissheitsstufe aus ``app.services.gewissheit`` (Zeile 8).

Abweichungen von der KWRA (Modellgrenze, bewusst ausgewiesen):

* Die KWRA misst gegen ein normativ gesetztes Restrisiko und trennt „beschlossene"
  von „weiterreichenden" Maßnahmen. Das Produkt kennt weder einen Restrisiko-Zielwert
  noch diese Trennung; es misst die relative Minderung durch die im Katalog
  hinterlegten Maßnahmen. Die Schwellen ``SCHWELLE_UMSETZUNG`` und
  ``SCHWELLE_ENTWICKLUNG`` sind deshalb eine **Abschätzung von KAP3** (siehe
  ``SCHWELLEN``), keine KWRA-Werte.
* Die KWRA zählt eine Gewissheit ab „mittel" als ausreichend, um nicht „unter
  Unsicherheit" zu fallen (TB6 S. 141, dritter Spiegelstrich); das übernimmt das
  Produkt unverändert. „Umsetzung" kennt die KWRA ohne Unsicherheitsvariante.
* Die beispielhafte Zuordnung der KWRA (Tabelle 27) beruht auf Expertenbewertungen
  und reagiert laut KWRA „in hohem Maße sensitiv" auf die gesetzten Zielwerte
  (S. 143); die hier abgeleitete Gruppe kann davon abweichen.
"""

from __future__ import annotations

from functools import lru_cache

from app.data import catalog
from app.services import gewissheit
from app.services.engine.impact.params import IMPACT_PARAM_SPECS

#: Die fünf KWRA-Charakterisierungsgruppen (TB6 Kap. 6.2, Gruppen I–V).
CHARAKTERISIERUNGSGRUPPEN = (
    "Umsetzung",
    "Entwicklung",
    "Entwicklung unter Unsicherheit",
    "Innovation",
    "Innovation unter Unsicherheit",
)

#: Gewissheitsstufen, die als ausreichend gelten (KWRA TB6 S. 141: „mittel" reicht).
AUSREICHENDE_GEWISSHEIT = ("mittel", "hoch")
UNZUREICHENDE_GEWISSHEIT = ("sehr gering", "gering")

#: Ab dieser relativen Minderung reichen die hinterlegten Maßnahmen (Gruppe I).
SCHWELLE_UMSETZUNG = 0.5
#: Ab dieser relativen Minderung gibt es einen Hebel, der sich weiterentwickeln lässt.
SCHWELLE_ENTWICKLUNG = 0.1

#: Schwellen mit Herleitung (Vorgabe P1: Abschätzung als solche ausgewiesen).
SCHWELLEN = {
    "SCHWELLE_UMSETZUNG": {
        "wert": SCHWELLE_UMSETZUNG,
        "art": "Abschätzung von KAP3",
        "herleitung": (
            "Die KWRA setzt als Ziel, das Restrisiko im pessimistischen Fall von hoch auf "
            "mittel zu senken (TB6 S. 141), also um eine von drei Stufen. Übertragen auf eine "
            "relative Minderung gilt: Senken die im Katalog hinterlegten Maßnahmen das Risiko "
            "mindestens um die Hälfte, reichen sie aus, und es geht um die Umsetzung."
        ),
        "band": (
            "0,4-0,6 (0,5 als Übertragung von „eine von drei Stufen“ auf eine relative "
            "Minderung; die Bandbreite ist eine Setzung von KAP3, nicht aus einer Quelle "
            "abgeleitet)."
        ),
        "sensitivitaet": (
            "Bestimmt, ab welcher Minderung eine Klimawirkung als „Umsetzung“ gilt statt "
            "als „Entwicklung“. Wirkt nur auf die Einordnung (Konformitätszeile 7), nicht "
            "auf Risikoindizes oder Euro-Beträge."
        ),
    },
    "SCHWELLE_ENTWICKLUNG": {
        "wert": SCHWELLE_ENTWICKLUNG,
        "art": "Abschätzung von KAP3",
        "herleitung": (
            "Unterhalb von zehn Prozent Minderung gibt es im Katalog keinen Hebel mit "
            "nennenswerter belegter oder abgeschätzter Wirkung; das Ziel ist dann nur mit "
            "tiefgreifender Anpassung erreichbar (KWRA-Gruppe Innovation). Ab zehn Prozent "
            "gibt es einen Hebel, den weiterreichende Maßnahmen ausbauen können "
            "(KWRA-Gruppe Entwicklung)."
        ),
        "band": (
            "0,05-0,2 (0,1 als runde Grenze für „nennenswerte Wirkung“; die Bandbreite ist "
            "eine Setzung von KAP3, nicht aus einer Quelle abgeleitet)."
        ),
        "sensitivitaet": (
            "Bestimmt, ab welcher Minderung eine Klimawirkung als „Entwicklung“ statt "
            "als „Innovation“ gilt. Wirkt nur auf die Einordnung (Konformitätszeile 7), "
            "nicht auf Risikoindizes oder Euro-Beträge."
        ),
    },
}

#: Entscheidungstabelle: (Untergrenze p, Obergrenze p exklusiv, Gewissheitsstufen, Gruppe).
#: Genau eine Zeile je Gruppe; die Zeilen überdecken [0, 1] × alle vier Stufen lückenlos
#: und ohne Überschneidung.
ENTSCHEIDUNGSTABELLE: tuple[tuple[float, float, tuple[str, ...], str], ...] = (
    (SCHWELLE_UMSETZUNG, float("inf"), gewissheit.GEWISSHEITSSTUFEN, "Umsetzung"),
    (SCHWELLE_ENTWICKLUNG, SCHWELLE_UMSETZUNG, AUSREICHENDE_GEWISSHEIT, "Entwicklung"),
    (SCHWELLE_ENTWICKLUNG, SCHWELLE_UMSETZUNG, UNZUREICHENDE_GEWISSHEIT,
     "Entwicklung unter Unsicherheit"),
    (float("-inf"), SCHWELLE_ENTWICKLUNG, AUSREICHENDE_GEWISSHEIT, "Innovation"),
    (float("-inf"), SCHWELLE_ENTWICKLUNG, UNZUREICHENDE_GEWISSHEIT,
     "Innovation unter Unsicherheit"),
)


def _registry_wert(risk_code: str, key: str) -> float:
    """Wert eines Impact-Parameters aus der Registry (``IMPACT_PARAM_SPECS``)."""
    for spec in IMPACT_PARAM_SPECS:
        if spec.get("risk") == risk_code and spec.get("key") == key:
            return float(spec["value"])
    raise KeyError(f"Registry-Parameter {key!r} für {risk_code!r} nicht gefunden")


@lru_cache(maxsize=None)
def a85_plus_anteil(ags: str) -> float:
    """a_85+ der Kommune: Anteil des Bands 85+ an allen verlorenen Lebensjahren (YLL) der
    Hitzemortalität, aus dem Zelllauf dieser Kommune (Bericht #95 §5 Hebel S157, Befund 183).

    a_85+ = (Todesfälle 85+ × Lebensjahre je Fall 85+) / YLL aller Bänder, summiert über alle
    Zellen der Kommune. Gerechnet wird wie im Jahresbetrag (``ergebnisbericht.beispiel``):
    Zellen aus den gepinnten Zelldaten ``backend/data/kalibrierung/golden95_zellen_<AGS>.csv.gz``
    (ohne Datenbank), je Rasterwert (Sommermittel, Hitzetage) nach Altersbändern zusammengefasst,
    Feinstruktur σ (``impact.health.SIGMA_K``, Gauß-Hermite mit ``GH_PUNKTE`` Punkten), die
    ``impact.health.mortality`` selbst rechnet. Die Rechnung läuft samt Laden der Zellen in
    ``override_context.override_scope({})``: Overrides eines laufenden Bewertungslaufs
    bleiben unberührt. Für Kommunen ohne gepinnte Zelldaten gibt es keinen Wert
    (``FileNotFoundError``); es wird keiner ersetzt.
    """
    from app.services.engine import override_context
    from app.services.engine.impact import health as H
    from app.services.engine.impact.base import CellContext
    from app.services.ergebnisbericht import beispiel
    from app.services.lite.vg250_loader import BUNDESLAND_BY_SNL

    with override_context.override_scope({}):
        gids, cis, klima = beispiel.zellen(ags)
        gruppen: dict[tuple[float, float], dict[str, float]] = {}
        for gid, ci in zip(gids, cis):
            acc = gruppen.setdefault(klima[gid], dict.fromkeys(beispiel.BANDS, 0.0))
            for b in beispiel.BANDS:
                acc[b] += float(ci["pop_age_bands"][b])

        mort_risk = catalog.RISKS_BY_CODE["EXPECTED_ANNUAL_MORTALITY"]
        regional = {"bundesland": BUNDESLAND_BY_SNL.get(ags[:2])}
        yll = deaths_a85p = 0.0
        for (t, hd), bands in gruppen.items():
            def ctx(temp, bands=bands, hd=hd):
                return CellContext(
                    ci={"pop": sum(bands.values()), "summer_temp_cell": temp, "pop_age_bands": bands},
                    hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
                    hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
                    indices={}, regional=regional)
            r = H.mortality(mort_risk, ctx(t))   # mit Feinstruktur σ (health.SIGMA_K)
            yll += r["outcome"]
            deaths_a85p += r["deaths_a85p"]
    return deaths_a85p * H.AGE_LIFE_YEARS["a85p"] / yll


def _s157_faktor(risk_code: str, ags: str | None) -> float:
    """Faktor (1 − r_S157), den die Maßnahme „Kühle Räume / Kühlzentren" (Hebel S157)
    multiplikativ zum Anpassungspotenzial beiträgt.

    r_S157 = a_85+ × h_Heim × max(s_gek − s_gek_kalib; 0) × (1 − g_S157); s_gek,
    s_gek_kalib, h_Heim und g_S157 kommen aus der Registry (Voreinstellungen, keine
    Kommunen-Eingabe), a_85+ ist ``a85_plus_anteil(ags)`` (je Kommune aus ihrem Zelllauf;
    Bericht #95 §5 Hebel S157, Log 50, Beispiel-Block ``s157_voreinstellung``:
    „r_S157 = a_85+ × h × (s_gek − 0,06) × (1 − g)"). Ohne Kommune (``ags`` ``None``) gibt es
    kein a_85+ und keinen Ersatzwert: Der Hebel S157 geht dann nicht in das Potenzial ein
    (Faktor 1).
    """
    if ags is None:
        return 1.0
    s_gek = _registry_wert(risk_code, "s_gek")
    s_gek_kalib = _registry_wert(risk_code, "s_gek_kalib")
    h_heim = _registry_wert(risk_code, "h_heim")
    g_s157 = _registry_wert(risk_code, "g_s157")
    r_s157 = a85_plus_anteil(ags) * h_heim * max(s_gek - s_gek_kalib, 0.0) * (1.0 - g_s157)
    return max(0.0, min(1.0, 1.0 - r_s157))


def anpassungspotenzial(
    risk_code: str, ags: str | None = None, *, _massnahmen: list[dict] | None = None,
) -> float:
    """Relative Risikominderung (0..1) durch die im Katalog hinterlegten Maßnahmen.

    Maßnahmen sind alle Einträge aus ``catalog.MEASURES``, deren
    ``linked_risk_codes`` den Code enthält (nur diese wirken im Rechenweg auf das
    Risiko; ``qualitative_risk_codes`` tragen keine Wirkung und zählen nicht).
    Je Maßnahme gilt bei voller Abdeckung derselbe Faktor wie in
    ``measure_service._reduction_factor``: f = (1 − r)^n mit r = ``default_reduction``
    (auf 0..1 begrenzt) und n = Zahl der ``effect_target``-Komponenten (mindestens 1).
    Ausnahme ``effect_model`` ``"s157"`` (Hebel S157, gekühlte Heimplätze): Die Maßnahme
    setzt ``default_reduction`` nicht an (wirkt nicht über eine pauschale Minderung,
    T-1410); ihr Faktor ist stattdessen ``1 − r_S157`` aus ``_s157_faktor`` (Bericht #95
    §5 Hebel S157, Log 50), mit a_85+ der Kommune ``ags`` (Gemeindeschlüssel, Zelllauf);
    ohne ``ags`` trägt S157 nichts bei. Mehrere Maßnahmen wirken multiplikativ: p = 1 − Π f. Ohne
    Maßnahme ist p = 0.
    """
    if risk_code not in catalog.RISKS_BY_CODE:
        raise KeyError(f"Unbekannter Risiko-Code: {risk_code}")
    massnahmen = catalog.MEASURES if _massnahmen is None else _massnahmen
    rest = 1.0
    for m in massnahmen:
        if risk_code not in (m.get("linked_risk_codes") or []):
            continue
        if m.get("effect_model") == "s157":
            rest *= _s157_faktor(risk_code, ags)
            continue
        r = max(0.0, min(1.0, float(m.get("default_reduction") or 0.0)))
        n = max(1, len(m.get("effect_target") or []))
        rest *= (1.0 - r) ** n
    return 1.0 - rest


def gruppe_aus(potenzial: float, gewissheitsstufe: str) -> str:
    """Wendet ``ENTSCHEIDUNGSTABELLE`` an (Tabelle siehe ``charakterisierungsgruppe``).

    Liefert genau einen Wert aus ``CHARAKTERISIERUNGSGRUPPEN``. Eine unbekannte
    Gewissheitsstufe oder eine Kombination ohne Tabellenzeile löst ``ValueError`` aus
    — nie ``None``.
    """
    if gewissheitsstufe not in gewissheit.GEWISSHEITSSTUFEN:
        raise ValueError(f"Unbekannte Gewissheitsstufe: {gewissheitsstufe!r}")
    for unten, oben, stufen, gruppe in ENTSCHEIDUNGSTABELLE:
        if unten <= potenzial < oben and gewissheitsstufe in stufen:
            return gruppe
    raise ValueError(
        f"Keine Zeile der Entscheidungstabelle für p={potenzial!r}, "
        f"Gewissheit={gewissheitsstufe!r}"
    )


def charakterisierungsgruppe(
    risk_code: str,
    *,
    _gewissheitsstufe: str | None = None,
    _massnahmen: list[dict] | None = None,
) -> str:
    """KWRA-Charakterisierungsgruppe einer Klimawirkung.

    Eingangsgrößen sind ausschließlich
    (a) das Anpassungspotenzial p = ``anpassungspotenzial(risk_code)`` (relative
        Risikominderung der im Katalog zu dieser Klimawirkung hinterlegten Maßnahmen) und
    (b) die Gewissheitsstufe g = ``gewissheit.gewissheitsstufe(risk_code)`` (Zeile 8).

    Entscheidungstabelle (``ENTSCHEIDUNGSTABELLE``; Schwellen 0,5 und 0,1 sind eine
    Abschätzung von KAP3, Herleitung in ``SCHWELLEN``; „Gewissheit ausreichend" ab
    „mittel" nach KWRA TB6 S. 141):

    | Anpassungspotenzial p | Gewissheitsstufe g            | Gruppe                         |
    |-----------------------|-------------------------------|--------------------------------|
    | p ≥ 0,5               | beliebig                      | Umsetzung                      |
    | 0,1 ≤ p < 0,5         | mittel, hoch                  | Entwicklung                    |
    | 0,1 ≤ p < 0,5         | sehr gering, gering           | Entwicklung unter Unsicherheit |
    | p < 0,1               | mittel, hoch                  | Innovation                     |
    | p < 0,1               | sehr gering, gering           | Innovation unter Unsicherheit  |

    Liefert immer genau einen Wert aus ``CHARAKTERISIERUNGSGRUPPEN``, nie ``None``;
    für dieselben Eingaben immer dasselbe Ergebnis. Unbekannte Codes → ``KeyError``.
    Die Parameter ``_gewissheitsstufe`` und ``_massnahmen`` erlauben es, bereits
    berechnete Eingaben bzw. konstruierte Maßnahmen zu übergeben (Sammelaufruf, Test).
    """
    p = anpassungspotenzial(risk_code, _massnahmen=_massnahmen)
    g = (gewissheit.gewissheitsstufe(risk_code)
         if _gewissheitsstufe is None else _gewissheitsstufe)
    return gruppe_aus(p, g)


def charakterisierungen() -> dict[str, dict]:
    """Für jeden Code aus ``catalog.RISKS_BY_CODE``: Gruppe mit ihren beiden Eingaben."""
    stufen = gewissheit.gewissheitsstufen()
    return {
        code: {
            "anpassungspotenzial": round(anpassungspotenzial(code), 4),
            "gewissheit": stufen[code],
            "gruppe": charakterisierungsgruppe(code, _gewissheitsstufe=stufen[code]),
        }
        for code in catalog.RISKS_BY_CODE
    }


def regel() -> dict:
    """Die Ableitungsregel für die API: Gruppen, Tabelle, Schwellen, Quelle, Grenzen."""
    def _grenze(x: float) -> float | None:
        return None if x in (float("inf"), float("-inf")) else x

    return {
        "gruppen": list(CHARAKTERISIERUNGSGRUPPEN),
        "entscheidungstabelle": [
            {"potenzial_ab": _grenze(u), "potenzial_unter": _grenze(o),
             "gewissheit": list(s), "gruppe": gr}
            for u, o, s, gr in ENTSCHEIDUNGSTABELLE
        ],
        "schwellen": SCHWELLEN,
        "quelle": ("UBA (Hrsg.): KWRA 2021, Teilbericht 6, Kap. 6.2 "
                   "„Charakterisierung der Handlungserfordernisse“, S. 140–143, Tabelle 27"),
        "modellgrenze": (
            "Die KWRA misst gegen ein normativ gesetztes Restrisiko und trennt beschlossene "
            "von weiterreichenden Maßnahmen; das Produkt misst die relative Minderung durch "
            "die im Katalog hinterlegten Maßnahmen. Die Gruppe kann deshalb von der "
            "beispielhaften Zuordnung der KWRA (Tabelle 27) abweichen."
        ),
    }

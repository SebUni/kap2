"""Maßnahmen-Engine (generalisiert für alle KAP3-Maßnahmen).

Eine Maßnahme reduziert ihre Zielkomponente(n) (``effect_target`` ∈ hazard/
exposure/vulnerability) in den abgedeckten Zellen, deckungs-skaliert. Da der
Risiko-Index multiplikativ in H·E·V ist, lässt sich die Wirkung auf die
verknüpften Risiken (``linked_risk_codes``) analytisch als Skalierung des Index
abbilden:

    factor = (1 - r_applied) ** n_targets
    neuer_Index = Basis-Index × factor

mit ``r_applied`` aus ``default_reduction`` und Deckungsgrad der Zelle.

Kosten je Maßnahme kommen aus den Katalog-Kostensätzen (CAPEX/OPEX). Der Nutzen ist
das **tatsächliche Delta der summierten Zellkosten** (E3): je abgedeckter Zelle und
verknüpftem Risiko ``Zellkosten · (1 − factor)``. Damit ist der ausgewiesene
Maßnahmen-Nutzen für pop-/area-skalierte Risiken exakt der Beitrag zur „Vermiedene
Schäden"-Kennzahl des Kommunen-Aggregats (dieselbe Σ-über-Zellen-Basis).
"""

from __future__ import annotations

import hashlib
import json
import logging

from geoalchemy2 import functions as func
from sqlalchemy import case, literal
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.data import catalog, sources
from app.models.models import (
    AdaptationMeasure, CellAssessment, GridCell, MeasureImpact, Kommune,
)
from app.services import aggregate_cache, parameter_registry
from app.services.engine import impact, override_context, risk_engine, tunables
from app.services.klimawirkungen import klimawirkungen

log = logging.getLogger(__name__)

# Defaults der Folgekosten-Konsolidierung (identisch zu impact/params.py IMPACT_GLOBAL_SPECS;
# override-fähig über impact.k_indirect / impact.restoration_share).
_K_INDIRECT_DEFAULT = 0.25
_RESTORATION_SHARE_DEFAULT = 0.15


def _reconsolidate_cell_folgekosten(risks: dict[str, dict]) -> None:
    """Bildet die Folgekosten einer Zelle aus ihren (ggf. maßnahmenbedingt reduzierten)
    direkten Sektorschäden neu — in-place, analog ``impact.consolidate_indirect`` (§8/B3).

    Ohne diesen Schritt bliebe nach Anwendung der Maßnahmen ``indirekt = k · Σ direkt``
    auf dem VOR-Maßnahmen-Stand stehen (die direkten Schäden sind reduziert, die daran
    gekoppelten Folgekosten aber nicht) — eine Inkonsistenz im Aggregat „mit Maßnahmen".
    Direkte Sektorschäden sind monetär (outcome == €), daher Summe über ``outcome``.
    """
    direct = sum(float(risks[c].get("outcome", 0.0))
                 for c in catalog.DIRECT_SECTOR_RISK_CODES if c in risks)
    k = float(override_context.get_override("impact.k_indirect", _K_INDIRECT_DEFAULT))
    r_share = float(override_context.get_override(
        "impact.restoration_share", _RESTORATION_SHARE_DEFAULT))
    for code, value in (("EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR", k * direct),
                        ("EXPECTED_RESTORATION_COSTS_EUR", r_share * direct)):
        if code in risks:
            risks[code] = {"index": risks[code].get("index", 0.0),
                           "outcome": value, "cost_eur": value}
    # supply/location/delayed bleiben 0 (in k_indirekt enthalten) — nichts zu tun.


def _cell_cost(risk: dict, cell_risk: dict, cell_pop: float) -> float:
    """Zellkosten eines Risikos – identische Basis wie ``risk_engine.aggregate``.

    Kosten werden LIVE aus dem gespeicherten ``outcome`` × aktuellem Kostensatz
    abgeleitet (``cost_from_outcome``), NICHT aus dem materialisierten ``cost_eur``
    gelesen — so wirken Kostensatz-Overrides ohne Neuberechnung, und die Reconciliation
    (Maßnahmen-Nutzen == Aggregat-Delta) bleibt exakt, weil ``aggregate`` dieselbe
    Ableitung nutzt (§8/B2). Für Alt-Zelldaten ohne Outcome (Kommune vor Neuberechnung)
    den Outcome über den linearen Legacy-Weg nachrechnen.
    """
    o = cell_risk.get("outcome")
    if o is None:
        idx = float(cell_risk.get("index", 0.0))
        o = impact.compute_cell_impacts(risk, idx, cell_pop)["outcome"]
    return risk_engine.cost_from_outcome(risk, float(o))


def _coverage(db: Session, measure: AdaptationMeasure) -> tuple[dict[int, float], float]:
    """Deckungsgrad (0..1) je Zelle plus abgedeckte Gesamtfläche (m²).

    Die Fläche wird als Σ (cell_size_m² · frac) über alle schneidenden Zellen
    bestimmt; die 3857-Verzerrung kürzt sich im frac-Verhältnis heraus. Sie wird
    hier zentral berechnet, weil sowohl die Kosten- als auch die Wirkungs-
    skalierung (unit_factor) die Gesamtfläche vor der Zell-Schleife brauchen.
    """
    cell_area = func.ST_Area(func.ST_Transform(GridCell.geometry, 3857))
    inter = func.ST_Area(func.ST_Transform(
        func.ST_Intersection(GridCell.geometry, measure.geometry), 3857))
    frac = case((cell_area > 0, inter / cell_area), else_=literal(0.0))
    rows = (
        db.query(GridCell.id, GridCell.cell_size_m, frac.label("frac"))
        .filter(GridCell.kommune_id == measure.kommune_id,
                func.ST_Intersects(GridCell.geometry, measure.geometry))
        .all()
    )
    frac_map: dict[int, float] = {}
    covered_area_m2 = 0.0
    for r in rows:
        f = max(0.0, min(1.0, float(r.frac)))
        frac_map[r.id] = f
        size = float(r.cell_size_m or 100)
        covered_area_m2 += (size ** 2) * f
    return frac_map, covered_area_m2


def _reduction_factor(mdef: dict, fraction: float, unit_factor: float = 1.0) -> float:
    """Kombinierter Skalierungsfaktor (0..1) für den Risiko-Index einer Zelle.

    ``unit_factor`` (0..1) skaliert die Wirkung von Stück-Maßnahmen anhand der
    Anzahl gegenüber dem Richtwert (min(1, Anzahl/Richtwert)); für Flächen-
    maßnahmen ist er 1.0 und lässt die bisherige Rechnung unverändert.
    """
    base_r = float(mdef.get("default_reduction", 0.0))
    if mdef.get("coverage_scaling") == "saturating":
        r = base_r * min(1.0, fraction * tunables.effective_measure_saturation())
    else:
        r = base_r * fraction
    r = r * unit_factor
    r = max(0.0, min(tunables.effective_measure_reduction_cap(), r))
    n = max(1, len(mdef.get("effect_target", []) or []))
    return (1.0 - r) ** n


# ── Hebel S157: gekühlte Heimplätze (Bericht #95 §5; Maßnahme COOLING_ROOMS_DRINKING_WATER) ──
# Die Wirkung ist kein default_reduction-Faktor auf den Index, sondern
# ΔD_S157 = D_85+ · h_Heim · max(s_gek − s_gek_kalib; 0) · (1 − g_S157) je Zelle, bewertet
# mit L̄_85+ (YLL); s_gek_kalib = 0,06 (Block heat.s_gek_kalib, Befund 165, Log 50).
# Im bestehenden multiplikativen Rahmen wird daraus je Zelle der Faktor
# 1 − ΔYLL_S157 / YLL_Zelle auf das Mortalitäts-Outcome — so bleiben Einzelnutzen
# und Aggregat „mit Maßnahmen“ dieselbe Rechnung.

S157_RISK_CODE = "EXPECTED_ANNUAL_MORTALITY"
# Befund 138: ohne Eingabe gilt die Voreinstellung s_gek = 0,11 (Block heat.s_gek);
# der Betrag ist dann eine begründete Abschätzung von KAP3 und wird so gekennzeichnet.
S157_ESTIMATE_NOTE = "Abschätzung von KAP3"
S157_S_GEK_DEFAULT = 0.11       # Rückfall, falls der Registry-Parameter fehlt
S157_S_GEK_KALIB_DEFAULT = 0.06  # dito, Block heat.s_gek_kalib


def _is_s157(mdef: dict) -> bool:
    return mdef.get("effect_model") == "s157"


def _s157_param(key: str, default: float) -> float:
    """Registry-Parameter der Mortalität für S157 (über override_context).

    Ohne Überschreibung gilt der Wert des Registry-Specs (``impact.params``,
    z. B. heat.s_gek 0,11, heat.s_gek_kalib 0,06); ``default`` nur, wenn es den Spec
    nicht gibt.
    """
    from app.services.engine.impact import params

    spec = next((s for s in params.IMPACT_PARAM_SPECS
                 if s.get("risk") == S157_RISK_CODE and s.get("key") == key), None)
    base = float(spec["value"]) if spec is not None and spec.get("value") is not None \
        else default
    v = override_context.get_override(f"risks.{S157_RISK_CODE}.impact.{key}", base)
    return float(v) if v is not None else base


def _s157_config_value(config: dict | None) -> float | None:
    """Eingabe s_gek der Kommune (Anteil 0..1), None ohne gültige Eingabe."""
    raw = (config or {}).get("s_gek")
    if raw is None or raw == "":
        return None
    try:
        return max(0.0, min(1.0, float(raw)))
    except (TypeError, ValueError):
        return None


def _s157_input(config: dict | None) -> float:
    """Heute gekühlter Anteil der Heimplätze s_gek (0..1) für S157.

    Die Eingabe der Kommune aus der Maßnahmen-Konfiguration; fehlt sie, gilt die
    Voreinstellung 0,11 aus dem Registry-Parameter heat.s_gek (Bericht #95 §5,
    Befund 138, Log 45). Der Wert gilt für die ganze Kommune. Den Abzug des Stands
    der Kalibrierjahre (heat.s_gek_kalib) rechnet ``_s157_cell_factor``; die
    Kommune gibt ihren heutigen Anteil ein, nicht den Zuwachs.
    """
    s = _s157_config_value(config)
    if s is not None:
        return s
    return max(0.0, min(1.0, _s157_param("s_gek", S157_S_GEK_DEFAULT)))


def _cell_q_pfl(cell_risk: dict) -> float | None:
    """Heimanteil 85+ der Zelle (``share_care_home_85p``, Ebene CARE_HOME_SHARE_85P).

    Grundlage für h_Heim,z (Bericht #95 §5, Befund 146); fehlt er, rechnet
    ``health.h_heim`` mit dem Rückfallwert 0,344.
    """
    q = cell_risk.get("share_care_home_85p")
    return float(q) if q is not None else None


def _with_cell_q_pfl(cell_risk: dict, inputs: dict | None) -> dict:
    """Risikoeintrag einer Zelle, ergänzt um ihren Heimanteil aus den Zell-Eingaben.

    Der Heimanteil steht in ``data["inputs"]`` der Zellbewertung, nicht im
    Risikoeintrag; S157 und die Schutzprogramme brauchen ihn für h_Heim,z (Befund 146).
    """
    q = (inputs or {}).get("share_care_home_85p")
    if q is None or "share_care_home_85p" in cell_risk:
        return cell_risk
    return {**cell_risk, "share_care_home_85p": q}


def _s157_cell_factor(s_gek: float | None, frac: float, cell_risk: dict,
                      delta_hap: float = 1.0) -> float:
    """Faktor (0..1) auf das Mortalitäts-Outcome (YLL) einer Zelle durch S157.

    S157 wirkt auf max(s_gek − s_gek_kalib; 0) (Befund 165, Log 50; s_gek_kalib aus
    dem Registry-Parameter heat.s_gek_kalib). ``s_gek`` gilt für die ganze Kommune,
    unabhängig von der gezeichneten Fläche (Bericht #95 §5, Modellgrenze): Der
    Deckungsgrad ``frac`` einer abgedeckten Zelle verkleinert die Wirkung deshalb
    nicht (Befund 138); nur eine Zelle ohne Deckung (``frac`` ≤ 0) bleibt unberührt.
    Zellen ohne Teil-Ausweis D_85+ (vor der Neuberechnung) bleiben unverändert.

    ``delta_hap`` (Befund 129): Faktor des Hitzeaktionsplans in dieser Zelle, wenn
    die Kommune ihn zugleich gewählt hat. Nur für den **Einzelnutzen** von S157
    setzen — im Aggregat „mit Maßnahmen“ bleibt er 1, weil dort der Faktor des
    Hitzeaktionsplans ohnehin mit diesem Faktor multipliziert wird
    (YLL · δ_HAP · (1 − ΔYLL/YLL) = YLL · δ_HAP − δ_HAP · ΔYLL); zweimal gesetzt,
    dämpfte er S157 doppelt.
    """
    from app.services.engine.impact import health

    if s_gek is None or frac <= 0.0:
        return 1.0
    yll = float(cell_risk.get("outcome") or 0.0)
    d85 = cell_risk.get("deaths_a85p")
    if yll <= 0.0 or d85 is None:
        return 1.0

    _p = _s157_param
    delta_d = health.s157_avoided_deaths(
        float(d85), s_gek,
        g_s157=_p("g_s157", health.G_S157), qbar_pfl=_p("qbar_pfl", 0.149),
        beta_pfl=_p("beta_pfl", 1.54), delta_hap=delta_hap,
        s_gek_kalib=_p("s_gek_kalib", S157_S_GEK_KALIB_DEFAULT),
        q_pfl=_cell_q_pfl(cell_risk)) or 0.0
    delta_yll = delta_d * _p("life_years_a85p", health.AGE_LIFE_YEARS["a85p"])
    return max(0.0, min(1.0, 1.0 - delta_yll / yll))


# ── Hebel S152: Schutzprogramme vulnerable Gruppen (Bericht #95 §5; VULNERABLE_GROUP_PROGRAMS) ──
# Die Wirkung ist kein default_reduction-Faktor auf alle Bänder (früher 0.22), sondern
# ΔD_VG = [D_75–84 + D_85+ · (1 − h_Heim)] · (1 − δ_VG) je Zelle, bewertet mit L̄_a (YLL),
# und dieselbe Formelzeile mit F und δ_VG,morb auf die Einweisungen. Mit dem
# Hitzeaktionsplan zusammen gilt max(δ_HAP × δ_VG; 0,794) (Kappung, Befund 126).

VG_MORB_RISK_CODE = "EXPECTED_ANNUAL_MORBIDITY"


def _is_vg(mdef: dict) -> bool:
    return mdef.get("effect_model") == "vg"


# ── Doppelzählungs-Wächter (Bericht #95 §5, Befund 150, Log 47; Block
#    heat.vg_in_kalibrierjahren) ──
# Lief das Programm (Schutzprogramme) bzw. liefen die Kühlzentren in der Kommune schon
# in den Kalibrierjahren 2012–2024, ist es keine zusätzliche Maßnahme: seine Wirkung
# steckt über c_kal im Basiswert. Dann gilt δ_VG = δ_VG,morb = 1 bzw. δ_KZ = 1. Je
# Maßnahme eine eigene Frage ja (1) / nein (0) in ``config['vg_in_kalibrierjahren']``;
# ohne Eingabe gilt der Registry-Wert 0 („nein“, Abschätzung von KAP3 aus [76]).
VG_KALIB_KEY = "vg_in_kalibrierjahren"
VG_KALIB_ESTIMATE_NOTE = "Abschätzung von KAP3"

_JA = {"1", "ja", "true", "yes", "j", "y"}
_NEIN = {"0", "nein", "false", "no", "n"}


def _vg_kalib_config_value(config: dict | None) -> int | None:
    """Eingabe der Kommune zur Wächter-Frage: 1 (ja), 0 (nein), None ohne gültige Eingabe."""
    raw = (config or {}).get(VG_KALIB_KEY)
    if raw is None or raw == "":
        return None
    if isinstance(raw, bool):
        return 1 if raw else 0
    if isinstance(raw, (int, float)):
        return 1 if float(raw) >= 0.5 else 0
    s = str(raw).strip().lower()
    if s in _JA:
        return 1
    if s in _NEIN:
        return 0
    return None


def _vg_kalib_input(config: dict | None) -> int:
    """Wächter-Frage „Lief das Programm schon 2012–2024?“: 1 = ja, 0 = nein.

    Die Eingabe der Kommune aus der Maßnahmen-Konfiguration (analog ``_s157_input``);
    fehlt sie, gilt der Registry-Parameter heat.vg_in_kalibrierjahren (0, „nein“,
    Abschätzung von KAP3; Bericht #95 §5, Befund 150, Log 47).
    """
    v = _vg_kalib_config_value(config)
    if v is not None:
        return v
    return 1 if _s157_param(VG_KALIB_KEY, 0.0) >= 0.5 else 0


def _vg_kalib_summary_fields(mdef: dict, config: dict | None) -> dict:
    """Zusatzfelder des impact_summary zur Wächter-Frage (Schutzprogramme, Kühlzentren)."""
    if not (_is_vg(mdef) or _is_s157(mdef)):
        return {}
    return {
        VG_KALIB_KEY: _vg_kalib_input(config),
        "vg_in_kalibrierjahren_is_default": _vg_kalib_config_value(config) is None,
        "vg_in_kalibrierjahren_estimate_note": VG_KALIB_ESTIMATE_NOTE,
    }


def _vg_cell_factor(code: str, frac: float, cell_risk: dict,
                    delta_hap: float = 1.0, hap_cap: float = 1.0) -> float:
    """Faktor der Schutzprogramme auf das Outcome einer Zelle (Mortalität oder Morbidität).

    ``frac`` ist der Deckungsgrad der Zelle; das Programm wirkt im abgedeckten Teil.
    ``hap_cap`` ist der Faktor des Hitzeaktionsplans in der Zelle für die Kappung
    am Paketwert (im Aggregat und im Einzelnutzen). ``delta_hap`` dämpft zusätzlich
    den Exzess — nur für den **Einzelnutzen** setzen, im Aggregat bleibt er 1, weil
    dort der Faktor des Plans ohnehin mitmultipliziert wird (wie bei S157).
    Zellen ohne Teil-Ausweis der Bänder (vor der Neuberechnung) bleiben unverändert.
    Auf die Morbidität kann der Faktor über 1 liegen (δ_VG,morb bis 1,069).
    """
    from app.services.engine.impact import health

    if frac <= 0.0:
        return 1.0
    outcome = float(cell_risk.get("outcome") or 0.0)
    if outcome <= 0.0:
        return 1.0

    def _p(risk_code: str, key: str, default: float) -> float:
        v = override_context.get_override(f"risks.{risk_code}.impact.{key}", default)
        return float(v) if v is not None else default

    f = max(0.0, min(1.0, frac))
    qbar = _p(S157_RISK_CODE, "qbar_pfl", 0.149)
    beta = _p(S157_RISK_CODE, "beta_pfl", 1.54)
    if code == S157_RISK_CODE:
        d75, d85 = cell_risk.get("deaths_a75_84"), cell_risk.get("deaths_a85p")
        if d75 is None or d85 is None:
            return 1.0
        delta = health.vg_effective_delta(
            _p(S157_RISK_CODE, "delta_vg", health.DELTA_VG), hap_cap,
            paket=_p(S157_RISK_CODE, "kappung_vg", health.VG_PAKET_DE))
        l75 = _p(S157_RISK_CODE, "life_years_a75_84", health.AGE_LIFE_YEARS["a75_84"])
        l85 = _p(S157_RISK_CODE, "life_years_a85p", health.AGE_LIFE_YEARS["a85p"])
        delta_x = health.vg_avoided(float(d75) * l75, float(d85) * l85, delta,
                                    qbar, beta, delta_hap, _cell_q_pfl(cell_risk))
        return max(0.0, min(1.0, 1.0 - f * delta_x / outcome))
    if code == VG_MORB_RISK_CODE:
        f75, f85 = cell_risk.get("cases_a75_84"), cell_risk.get("cases_a85p")
        if f75 is None or f85 is None:
            return 1.0
        delta = _p(VG_MORB_RISK_CODE, "delta_vg_morb", health.DELTA_VG_MORB)
        delta_x = health.vg_avoided(float(f75), float(f85), delta, qbar, beta, delta_hap,
                                    _cell_q_pfl(cell_risk))
        return max(0.0, 1.0 - f * delta_x / outcome)
    return 1.0


# ── Hebel öffentliche Kühlzentren (Bericht #95 §5 Z. 1203–1246, Befunde 139, 148;
#    Maßnahme COOLING_ROOMS_DRINKING_WATER, Entscheidung CEO 27.09.2026) ──
# Die Kühlzentren hängen an derselben Maßnahme wie S157, wirken aber auf andere Menschen:
# ΔD_KZ = [D_75–84 + D_85+ · (1 − h_Heim)] · (1 − δ_KZ) je Zelle, bewertet mit L̄_a (YLL),
# im abgedeckten Teil der Zelle (wie die Schutzprogramme). Mit Hitzeaktionsplan und
# Schutzprogrammen zusammen gilt max(δ_HAP × δ_VG × δ_KZ; kappung_vg). S157 (Heimbewohner
# 85+) und Kühlzentren (zu Hause) treffen getrennte Gruppen, ihre Wirkungen werden addiert.

KZ_ESTIMATE_NOTE = "Abschätzung von KAP3"


def _kz_cell_factor(frac: float, cell_risk: dict, delta_hap: float = 1.0,
                    hap_cap: float = 1.0, delta_vg: float = 1.0,
                    vg_cap: float = 1.0) -> float:
    """Faktor (0..1) der öffentlichen Kühlzentren auf das Mortalitäts-Outcome einer Zelle.

    ``frac`` ist der Deckungsgrad; der Hebel wirkt im abgedeckten Teil (Bericht Z. 1243).
    ``hap_cap`` und ``vg_cap`` sind die Faktoren von Hitzeaktionsplan und Schutzprogrammen
    in der Zelle für die Kappung ``max(δ_HAP × δ_VG × δ_KZ; kappung_vg)`` (im Aggregat und
    im Einzelnutzen). ``delta_hap`` und ``delta_vg`` dämpfen den Exzess — nur für den
    **Einzelnutzen** setzen (``delta_vg`` ist dann der Outcome-Faktor der Schutzprogramme
    in der Zelle); im Aggregat bleiben sie 1, weil dort die Faktoren ohnehin
    multipliziert werden. Zellen ohne Teil-Ausweis der Bänder bleiben unverändert.
    """
    from app.services.engine.impact import health

    if frac <= 0.0:
        return 1.0
    outcome = float(cell_risk.get("outcome") or 0.0)
    if outcome <= 0.0:
        return 1.0
    d75, d85 = cell_risk.get("deaths_a75_84"), cell_risk.get("deaths_a85p")
    if d75 is None or d85 is None:
        return 1.0

    _p = _s157_param
    f = max(0.0, min(1.0, frac))
    delta = health.kz_effective_delta(
        _p("delta_kuehlzentren", health.DELTA_KZ), float(hap_cap) * float(vg_cap),
        paket=_p("kappung_vg", health.VG_PAKET_DE))
    l75 = _p("life_years_a75_84", health.AGE_LIFE_YEARS["a75_84"])
    l85 = _p("life_years_a85p", health.AGE_LIFE_YEARS["a85p"])
    delta_x = health.kz_avoided(
        float(d75) * l75, float(d85) * l85, delta,
        _p("qbar_pfl", 0.149), _p("beta_pfl", 1.54),
        max(0.0, min(1.0, float(delta_hap))) * max(0.0, min(1.0, float(delta_vg))),
        _cell_q_pfl(cell_risk))
    return max(0.0, min(1.0, 1.0 - f * delta_x / outcome))


def _vg_kz_factors(vg_fracs: list[float], cell_risk: dict,
                   hap_cap: float = 1.0) -> tuple[float, float]:
    """Schutzprogramme in einer Zelle, gesehen von den Kühlzentren: (Dämpfung, Kappung).

    ``vg_fracs`` sind die Deckungsgrade der gewählten Schutzprogramme in der Zelle.
    Dämpfung = Outcome-Faktor der Schutzprogramme (wie im Aggregat), damit die Summe der
    Einzelnutzen das Aggregat ergibt. Kappung = wirksames δ_VG auf den Bändern, je
    Deckungsgrad gewichtet: 1 − frac · (1 − δ_VG nach Kappung).
    """
    from app.services.engine.impact import health

    damp, cap = 1.0, 1.0
    if not vg_fracs:
        return damp, cap
    d_vg_eff = health.vg_effective_delta(
        _s157_param("delta_vg", health.DELTA_VG), hap_cap,
        paket=_s157_param("kappung_vg", health.VG_PAKET_DE))
    for fr in vg_fracs:
        if fr <= 0.0:
            continue
        damp *= _vg_cell_factor(S157_RISK_CODE, fr, cell_risk, 1.0, hap_cap)
        cap *= 1.0 - min(1.0, fr) * (1.0 - d_vg_eff)
    return damp, cap


def _kz_summary_fields(mdef: dict, kz_eur: float, s157_eur: float,
                       with_vg: bool) -> dict:
    """Zusatzfelder des impact_summary: Betrag der Kühlzentren getrennt von S157.

    ``kuehlzentren_benefit_eur`` und ``s157_benefit_eur`` teilen den vermiedenen Schaden
    der Mortalität auf die beiden Hebel der Maßnahme; zusammen ergeben sie
    ``annual_benefit_damage_eur``. ``kuehlzentren_estimate_note`` kennzeichnet den Betrag
    als begründete Abschätzung von KAP3 (heat.delta_kuehlzentren, P2).
    """
    if not _is_s157(mdef):
        return {}
    from app.services.engine.impact import health

    return {
        "kuehlzentren_benefit_eur": round(kz_eur, 2),
        "s157_benefit_eur": round(s157_eur, 2),
        "delta_kuehlzentren": _s157_param("delta_kuehlzentren", health.DELTA_KZ),
        "kuehlzentren_estimate_note": KZ_ESTIMATE_NOTE,
        "kuehlzentren_with_vg": with_vg,
    }


# ── Hebel S158: Pollen-Frühwarnung (Bericht #96 §5.1; Maßnahme POLLEN_EARLY_WARNING) ──
# Sperre aus Befund 124 aufgehoben (T-1513-cto): Die Wirkung ist kein flächiger Faktor
# auf den Index, sondern ΔTage_vermieden = A_Zelle · r_S158 · Σ_g t_warn,g · ΔTage_g,Zelle
# je Zelle (health.s158_vermiedene_tage), bewertet über denselben Zellfaktor-Rahmen wie
# S157: 1 − ΔTage_vermieden / ΔTage_Zelle auf das Outcome (Symptomtage/€) der Zelle.

ALLERGY_RISK_CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
# S158-Integrationsauflage Punkt 5 (Bericht #96 §5.1 Z. 1416 f.): der Nutzen von S158
# ist eine begründete Abschätzung von KAP3 (r_S158, t_warn — beide P2), nicht eine
# belegte Effektgröße; die Kennzeichnung trägt der Ausgabetext, nicht nur die
# Herleitung im Bericht. Fehlt in einer abgedeckten Zelle mit Zusatztagen (Outcome > 0)
# die Aufteilung nach Pollengruppe (Alt-Zelle, vor der Neuberechnung), lässt sich die
# Wirkung dort nicht bestimmen — dann steht ein Vermerk statt eines (ggf. zu niedrigen,
# als 0 € lesbaren) Betrags (P2: nie 0 € wegen fehlender Eingabe).
S158_ESTIMATE_NOTE = "Abschätzung von KAP3"
S158_MISSING_SPLIT_TEXT = ("kein Betrag: Zusatztage je Pollengruppe fehlen, "
                           "Kommune neu berechnen")


def _is_s158(mdef: dict) -> bool:
    return mdef.get("effect_model") == "s158"


def _s158_cell_effect(mdef: dict, frac: float, cell_risk: dict,
                      days_factor: float = 1.0) -> tuple[float, float | None, bool]:
    """(Faktor, vermiedene Tage, fehlende Gruppenaufteilung) einer Zelle durch S158.

    Die Gruppentage ΔTage_B/G,Zelle holt der Zweig FRISCH über ``health.pollen_zelltage``
    aus den gespeicherten Roheingaben der Zelle (``betroffene``, ``delta_birke``,
    ``delta_graeser``, ``pollen_g``, ``pollen_g_bar0``) — nicht aus den gespeicherten
    Summen ``tage_birke``/``tage_graeser``. So wirkt eine spätere Vegetationsmaßnahme
    (Stadtbaumwahl, T-1483-cto), die nur Ĝ_Zelle auf Ĝ′ ändert und Ḡ₀ festhält,
    multiplikativ zusammen mit S158 (Bericht §5 „Zusammen mit S158“), statt von einer
    zuvor gespeicherten Summe überschrieben zu werden. λ (``lambda_veg``) wird nicht
    gespeichert und deshalb hier aus den Overrides gelesen, damit eine Überschreibung
    wirkt.

    ``days_factor`` (Bericht §5 „Zusammen mit S158", T-1602-cto): deckt dieselbe Zelle
    zugleich eine Stadtbaumwahl derselben Kommune ab, mindert die Frühwarnung nur die
    Tage nach der Pflanzung — der Aufrufer übergibt hier den Ĝ′-Tage-Faktor der
    Stadtbaumwahl (Verhältnis der Zusatztage NACH zu VOR der Pflanzung,
    ``_stadtbaum_cell_factor``; Standard 1,0 ohne Stadtbaumwahl). Beide Gruppentage
    skalieren mit demselben Faktor, weil er allein über P̂ wirkt (nur Ĝ ändert sich,
    B, δ_B, δ_G bleiben gleich) — Bezugsgröße für die vermiedenen Tage UND Nenner des
    Faktors sind dann die schon um die Pflanzung geminderten Tage, nicht der
    Ausgangsstand: so zählt kein vermiedener Tag doppelt.

    ``vermiedene Tage`` ist ``None``, wenn die Zelle außerhalb des Geltungsbereichs liegt
    oder die Roheingaben fehlen (Alt-Zelle vor der Neuberechnung) — dann bleibt der
    Faktor unverändert (1.0), es gibt keine pauschale Ersatzwirkung. Trägt eine solche
    Zelle bereits Zusatztage (Outcome > 0), ist die dritte Rückgabe ``True`` (Zelle mit
    Zusatztagen, aber ohne Gruppenaufteilung — der Betrag der Kommune wäre sonst zu
    niedrig, ohne dass das sichtbar würde).
    """
    from app.services.engine.impact import health

    if frac <= 0.0:
        return 1.0, None, False
    betroffene = cell_risk.get("betroffene")
    delta_b = cell_risk.get("delta_birke")
    delta_g = cell_risk.get("delta_graeser")
    g_cell = cell_risk.get("pollen_g")
    if betroffene is None or delta_b is None or delta_g is None or g_cell is None:
        outcome = float(cell_risk.get("outcome") or 0.0)
        return 1.0, None, outcome > 0.0
    g_bar0 = cell_risk.get("pollen_g_bar0")

    def _p(key: str, default: float) -> float:
        v = override_context.get_override(f"risks.{ALLERGY_RISK_CODE}.impact.{key}", default)
        return float(v) if v is not None else default

    lam = _p("lambda_veg", 0.70)
    tage_birke, tage_graeser = health.pollen_zelltage(
        float(betroffene), float(delta_b), float(delta_g), float(g_cell), g_bar0, lam)
    total = tage_birke + tage_graeser
    if total <= 0.0:
        return 1.0, 0.0, False

    df = max(0.0, float(days_factor))
    tage_birke_adj = tage_birke * df
    tage_graeser_adj = tage_graeser * df
    total_adj = tage_birke_adj + tage_graeser_adj
    if total_adj <= 0.0:
        return 1.0, 0.0, False

    r = float(mdef.get("default_reduction") or 0.0)
    t_warn = _p("t_warn_s158", 0.75)
    vermieden = health.s158_vermiedene_tage(
        tage_birke_adj, tage_graeser_adj, frac, r, t_warn, t_warn)
    factor = max(0.0, min(1.0, 1.0 - vermieden / total_adj))
    return factor, vermieden, False


def _s158_cell_factor(mdef: dict, frac: float, cell_risk: dict,
                      days_factor: float = 1.0) -> float:
    """Faktor (0..1) auf das Symptomtage-Outcome einer Zelle durch S158 (Wrapper)."""
    factor, _, _ = _s158_cell_effect(mdef, frac, cell_risk, days_factor)
    return factor


# ── Hebel Stadtbaumwahl (Bericht #96 §5, Integrationsauflage Z. 1111–1125; Maßnahme
# LOW_ALLERGEN_TREE_SELECTION) — Vorhaben T-1483-cto Teilpaket #2, setzt auf der
# Zellfunktion health.stadtbaum_g_neu (T-1599-cto) auf. Wie S158 (Sperre aus Befund 124)
# rechnet der Zweig NICHT als Faktor auf ein gespeichertes Ergebnis, sondern bildet Ĝ′
# frisch aus den in der Zelle gespeicherten Roheingaben und vergleicht ΔTage vorher/
# nachher über dieselbe Zellfunktion ``health.pollen_zelltage`` wie S158/die
# Schadensfunktion selbst.

def _is_stadtbaum(mdef: dict) -> bool:
    return mdef.get("effect_model") == "stadtbaum"


# Integrationsauflage (Stadtbaumwahl) §5 Z. 1111–1125, Punkt (4): Ausgabe der
# vermiedenen Zusatztage und Euro je Zelle und für die Kommune, gekennzeichnet als
# begründete Abschätzung von KAP3 (Δk_Birke/Δk_unbek sind keine belegten
# Effektgrößen, dieselbe Kennzeichnung wie S158 — P2), mit dem Hinweis auf die
# Richtung des Fehlers in λ (§6 Modellgrenze 7: der örtliche Quellenanteil ist über
# Gräser belegt [74], nicht über Bäume, und Ferntransport entkoppelt lokale
# Vegetation und lokalen Pollenflug teilweise — welche Richtung überwiegt, ist nicht
# bestimmbar). Fehlt ``config['anteil_ersetzt']`` (Punkt (2) der Auflage ohne
# Eingabe), entsteht kein Betrag statt eines erfundenen (P2, Muster S158
# ``benefit_missing_input``). Führt eine abgedeckte Zelle im Ausgangsstand keine
# Baumkronen (``canopy_birch_frac`` + ``canopy_unknown_frac`` ≤ 0), ist dort
# mechanisch nichts zu ersetzen; trägt am Ende KEINE Zelle einen positiven Effekt,
# stünde ein irreführendes 0 € (nicht von einer Datenlücke unterscheidbar) — dann
# steht ein Vermerk statt des Betrags (P2).
STADTBAUM_ESTIMATE_NOTE = S158_ESTIMATE_NOTE
STADTBAUM_LAMBDA_HINWEIS = (
    "Richtung des Fehlers in λ nicht bestimmbar (Modellgrenze 7): der örtliche "
    "Quellenanteil ist für Gräser belegt, nicht für Bäume, und Ferntransport "
    "entkoppelt lokale Vegetation und lokalen Pollenflug teilweise.")
STADTBAUM_MISSING_ANTEIL_TEXT = ("kein Betrag: Anteil ersetzter Kronen "
                                 "(anteil_ersetzt) fehlt, Eingabe in der Maßnahme ergänzen")
# Ü-9 (Befund 251): anteil_ersetzt ist ein Anteil in [0, 1]. Eine Eingabe über 1 (am Schema
# abgewiesen, aber ungeprüft über Excel-Import, ältere Maßnahmen und direkte Aufrufe möglich)
# erzeugt keinen Betrag: die Kappung je Term in health.stadtbaum_g_neu ließe sie bei
# Deckungsgrad 1 still wie 1 zählen und bei teilweiser Deckung mehr senken als a = 1.
STADTBAUM_ANTEIL_BEREICH_TEXT = ("kein Betrag: Anteil ersetzter Kronen (anteil_ersetzt) muss "
                                 "zwischen 0 und 1 liegen, Eingabe in der Maßnahme berichtigen")
STADTBAUM_ANTEIL_BEREICH_REASON = "anteil_ersetzt_bereich"
STADTBAUM_NO_CANOPY_TEXT = ("kein Betrag: abgedeckte Zellen führen im Ausgangsstand "
                            "keine Baumkronen, dort ist nichts zu ersetzen")


def _stadtbaum_cell_effect(config: dict | None, frac: float, cell_risk: dict
                          ) -> tuple[float, float | None, str | None]:
    """(Faktor, vermiedene Zusatztage, fehlende Eingabe) einer Zelle durch die
    Stadtbaumwahl (Integrationsauflage §5 Punkt (4)).

    Bildet dieselbe Ĝ′-Rechnung wie bisher (``_stadtbaum_cell_factor``, jetzt ein
    dünner Wrapper hierauf), zusätzlich mit der Differenz ΔTage = Tage(Ĝ) − Tage(Ĝ′)
    und einer Kennzeichnung, warum keine Zahl entsteht: ``'anteil_ersetzt'`` — die
    Maßnahme trägt kein (oder kein positives) ``config['anteil_ersetzt']``;
    ``'anteil_ersetzt_bereich'`` — ``config['anteil_ersetzt']`` liegt über 1 (Ü-9,
    Befund 251: kein Betrag, Eingabe berichtigen);
    ``'canopy'`` — die Zelle führt im Ausgangsstand keine Baumkronen
    (``canopy_birch_frac`` + ``canopy_unknown_frac`` ≤ 0), dort ist mechanisch
    nichts zu ersetzen. ``None`` als dritte Rückgabe heißt: keine dieser Lagen —
    entweder die Zelle liegt außerhalb der Deckung/hat keine Roheingaben (Alt-Zelle,
    kein eigener Grund) oder es entsteht eine reguläre Zahl.
    """
    from app.services.engine.impact import health

    if frac <= 0.0:
        return 1.0, None, None
    a = float((config or {}).get("anteil_ersetzt") or 0.0)

    betroffene = cell_risk.get("betroffene")
    delta_b = cell_risk.get("delta_birke")
    delta_g = cell_risk.get("delta_graeser")
    g_cell = cell_risk.get("pollen_g")
    k_birke = cell_risk.get("canopy_birch_frac")
    k_unbek = cell_risk.get("canopy_unknown_frac")
    gruen = cell_risk.get("green_frac")
    if None in (betroffene, delta_b, delta_g, g_cell, k_birke, k_unbek, gruen):
        return 1.0, None, None
    if a <= 0.0:
        return 1.0, None, "anteil_ersetzt"
    if a > 1.0:
        return 1.0, None, STADTBAUM_ANTEIL_BEREICH_REASON
    if (float(k_birke) + float(k_unbek)) <= 0.0:
        return 1.0, 0.0, "canopy"
    g_bar0 = cell_risk.get("pollen_g_bar0")

    def _p(key: str, default: float) -> float:
        v = override_context.get_override(f"risks.{ALLERGY_RISK_CODE}.impact.{key}", default)
        return float(v) if v is not None else default

    lam = _p("lambda_veg", 0.70)
    s_unbek = _p("birch_group_share_default", 0.12)

    dk_birke = a * frac * float(k_birke)
    dk_unbek = a * frac * float(k_unbek)
    g_neu = health.stadtbaum_g_neu(float(g_cell), float(k_birke), float(k_unbek),
                                   float(gruen), dk_birke, dk_unbek, s_unbek)

    tage_b0, tage_g0 = health.pollen_zelltage(
        float(betroffene), float(delta_b), float(delta_g), float(g_cell), g_bar0, lam)
    total0 = tage_b0 + tage_g0
    if total0 <= 0.0:
        return 1.0, 0.0, None
    tage_b1, tage_g1 = health.pollen_zelltage(
        float(betroffene), float(delta_b), float(delta_g), g_neu, g_bar0, lam)
    total1 = tage_b1 + tage_g1
    factor = max(0.0, total1 / total0)
    return factor, total0 - total1, None


def _stadtbaum_summary_fields(mdef: dict, avoided_days_total: float, avoided_days_eur: float,
                              missing_reason: str | None) -> dict:
    """Zusatzfelder des impact_summary für die Stadtbaumwahl (Integrationsauflage §5
    Punkt (4)).

    ``stadtbaum_avoided_days_total``/``stadtbaum_avoided_days_eur`` sind die
    vermiedenen Zusatztage bzw. Euro/Jahr der Kommune (Summe der Zellwerte),
    zusammen mit der Kennzeichnung als begründete Abschätzung von KAP3 und dem
    Hinweis auf die Richtung des Fehlers in λ (Modellgrenze 7). Fehlt
    ``anteil_ersetzt`` oder führt keine abgedeckte Zelle Baumkronen im
    Ausgangsstand, steht ein Vermerk statt eines (sonst als 0 € lesbaren) Betrags.
    """
    if not _is_stadtbaum(mdef):
        return {}
    if missing_reason == "anteil_ersetzt":
        return {"benefit_display": STADTBAUM_MISSING_ANTEIL_TEXT,
                "benefit_missing_input": "anteil_ersetzt"}
    if missing_reason == STADTBAUM_ANTEIL_BEREICH_REASON:
        return {"benefit_display": STADTBAUM_ANTEIL_BEREICH_TEXT,
                "benefit_missing_input": "anteil_ersetzt"}
    if missing_reason == "canopy":
        return {"benefit_display": STADTBAUM_NO_CANOPY_TEXT,
                "benefit_missing_input": "canopy"}
    return {
        "stadtbaum_avoided_days_total": round(avoided_days_total, 1),
        "stadtbaum_avoided_days_eur": round(avoided_days_eur, 2),
        "stadtbaum_estimate_note": STADTBAUM_ESTIMATE_NOTE,
        "stadtbaum_lambda_hinweis": STADTBAUM_LAMBDA_HINWEIS,
    }


# Kosten der Stadtbaumwahl (Bericht #96 §5, Absatz „Kosten der Stadtbaumwahl“, Kap. 7.1
# Block pollen.stadtbaum_kosten; Befund 253, Übernahme Ü-11 (b), (c)): je ersetztem Baum
# nach dem Fall, den die Kommune wählt (config['ersatzfall']). Ohne Fall kein CAPEX und
# keine Kosten-Nutzen-Kennzahl, beide Beträge nebeneinander; eine stille Vorgabe auf
# einen Fall gibt es nicht. Ohne Zahl der Bäume ein Vermerk statt eines Betrags.
STADTBAUM_ERSATZFAELLE = ("nachpflanzung", "vorgezogen")
STADTBAUM_FALL_WAEHLEN_TEXT = "Fall wählen: Nachpflanzung ohnehin oder vorgezogener Ersatz"
STADTBAUM_COUNT_FEHLT_TEXT = "Zahl der ersetzten Bäume eingeben"
STADTBAUM_NACHPFLANZUNG_HINWEIS = (
    "Der Nutzen je Jahr gilt erst mit voller Krone der sonst gepflanzten Bäume; "
    "Amortisation am Punktwert nach rund 24 Jahren (Bericht #96 §5)")


def _stadtbaum_kosten(mdef: dict, config: dict | None, count: int) -> tuple[dict, dict]:
    """(Definition für ``compute_costs``, Zusatzfelder des impact_summary) der Stadtbaumwahl.

    Mit gewähltem Fall und Stückzahl setzt die Funktion ``capex_per_unit`` (samt Quelle
    und Herleitung) aus dem aufgelösten Zusatzfeld ``capex_per_unit_<fall>``. Ohne Fall
    bleibt ``capex_per_unit`` None; das summary führt ``capex_je_fall`` mit beiden
    Beträgen und den Vermerk, den Fall zu wählen. Ohne Stückzahl steht der Vermerk
    ``STADTBAUM_COUNT_FEHLT_TEXT`` statt eines Betrags.
    """
    if not _is_stadtbaum(mdef) or not mdef.get("zusatz_kostenfelder"):
        return mdef, {}
    fall = (config or {}).get("ersatzfall")
    count_fehlt = mdef.get("count_pflicht") and (config or {}).get("count") is None
    felder: dict = {"ersatzfall": fall if fall in STADTBAUM_ERSATZFAELLE else None}
    if count_fehlt:
        felder["kosten_vermerk"] = STADTBAUM_COUNT_FEHLT_TEXT
        felder["kosten_nutzen_kennzahl_offen"] = True
        return mdef, felder
    if fall not in STADTBAUM_ERSATZFAELLE:
        felder["capex_je_fall"] = {
            f: round(count * float(mdef.get(f"capex_per_unit_{f}") or 0.0), 2)
            for f in STADTBAUM_ERSATZFAELLE}
        felder["kosten_vermerk"] = STADTBAUM_FALL_WAEHLEN_TEXT
        felder["kosten_nutzen_kennzahl_offen"] = True
        return mdef, felder
    quelle = f"capex_per_unit_{fall}"
    out = dict(mdef)
    out["capex_per_unit"] = mdef.get(quelle)
    for name in ("sources", "source_details", "source_refs"):
        karte = dict(mdef.get(name) or {})
        if quelle in karte:
            karte["capex_per_unit"] = karte[quelle]
        out[name] = karte
    custom = dict(mdef.get("custom_sources") or {})
    if quelle in custom:
        custom["capex_per_unit"] = custom[quelle]
    out["custom_sources"] = custom
    if fall == "nachpflanzung":
        felder["stadtbaum_kosten_hinweis"] = STADTBAUM_NACHPFLANZUNG_HINWEIS
    return out, felder


def _stadtbaum_cell_factor(config: dict | None, frac: float, cell_risk: dict) -> float:
    """Faktor (0..1) auf das Symptomtage-Outcome einer Zelle durch die Stadtbaumwahl.

    Liest ausschließlich ``config['anteil_ersetzt']`` (a, Anteil der Kommune) — kein
    eigenes Gattungsfeld der Maßnahme (Vorhabenskriterium iii, Entscheidung CEO in
    T-1431-ceo). Je Zelle mit Deckungsgrad ``frac`` sinken die Kronenterme im
    Ausgangsstand der Zelle ANTEILIG in dem Term, in dem sie stehen:
    ``dk_Birke = a · frac · k_Birke,z`` (Kronen MIT Gattungs-Tag, ``canopy_birch_frac``),
    ``dk_unbek = a · frac · k_unbek,z`` (Kronen OHNE Gattungs-Tag,
    ``canopy_unknown_frac``) — Kronen ohne Gattungs-Tag (auch neu gepflanzte
    allergenarme Bäume ohne Tag) zählen anteilig weiter, das ist eine Modellgrenze,
    keine eigene Regel.

    Ĝ′ entsteht über ``health.stadtbaum_g_neu`` (Kappung je Term, Boden
    (1 − w_B)·Grün). Ḡ₀ ist der GESPEICHERTE ``pollen_g_bar0`` der Zelle aus dem
    Ausgangsstand (``inputs.kommunale_pollen_referenz`` wird hier NICHT erneut
    aufgerufen — Ḡ₀ bleibt für jedes Maßnahmenszenario festgehalten, Bericht §5 Z.
    975–989/1115–1121). Der Faktor ist
    ``health.pollen_zelltage(Ĝ′)/health.pollen_zelltage(Ĝ)`` (Summe beider
    Pollengruppen) auf dieselben Roheingaben (``betroffene``, ``delta_birke``,
    ``delta_graeser``) — dasselbe Muster wie ``_s158_cell_effect``: eine frische
    Zellrechnung, kein Faktor auf ein gespeichertes Ergebnis (Sperre aus Befund 124).

    Ohne Deckung (``frac`` ≤ 0), ohne ``anteil_ersetzt`` (bzw. ≤ 0) oder ohne die
    nötigen Zell-Roheingaben (Alt-Zelle vor der Neuberechnung, T-1599-cto) bleibt der
    Faktor 1,0 — keine pauschale Ersatzwirkung. Wrapper um ``_stadtbaum_cell_effect``
    (T-1604-cto, Ausgabe-Integrationsauflage §5 Punkt (4)): dieselbe Rechnung, hier
    nur der Faktor.
    """
    factor, _, _ = _stadtbaum_cell_effect(config, frac, cell_risk)
    return factor


# S158 zusammen mit der Stadtbaumwahl (Bericht §5 „Zusammen mit S158", T-1602-cto): die
# Frühwarnung mindert die Tage B·δ_g·P̂′, die NACH der Pflanzung noch anfallen — kein
# vermiedener Tag zählt doppelt, weil die Frühwarnung nur auf Tage wirkt, die die
# Pflanzung nicht schon vermieden hat. Muster analog Befund 129 (δ_HAP × S157).
STADTBAUM_CODE = "LOW_ALLERGEN_TREE_SELECTION"


def _stadtbaum_measures(db: Session, measure: AdaptationMeasure) -> list[AdaptationMeasure]:
    """Stadtbaumwahl-Maßnahmen derselben Kommune (und derselben Demo-Sitzung) wie ``measure``."""
    return [m for m in kommune_measures_query(db, measure.kommune_id, measure.demo_session_id)
            .filter(AdaptationMeasure.measure_type == STADTBAUM_CODE).all()
            if m.id != measure.id]


def _stadtbaum_cell_days_factors(db: Session, measure: AdaptationMeasure) -> dict[int, float]:
    """Ĝ′-Tage-Faktor je Zelle (Zusatztage NACH zu VOR der Pflanzung) aus den
    Stadtbaumwahl-Maßnahmen derselben Kommune wie ``measure`` — für S158 (Bericht §5
    „Zusammen mit S158"). Mehrere Stadtbaumwahl-Maßnahmen wirken multiplikativ (Muster
    δ_HAP, Befund 129). Ohne eine solche Maßnahme, ohne ihre Deckung der Zelle oder ohne
    die nötigen Zell-Roheingaben bleibt der Faktor 1,0 (``_stadtbaum_cell_factor``).
    """
    out: dict[int, float] = {}
    stadtbaum_measures = _stadtbaum_measures(db, measure)
    if not stadtbaum_measures:
        return out
    cell_ids: set[int] = set()
    coverage_by_measure: list[tuple[AdaptationMeasure, dict[int, float]]] = []
    for m in stadtbaum_measures:
        frac_map, _ = _coverage(db, m)
        coverage_by_measure.append((m, frac_map))
        cell_ids.update(frac_map.keys())
    if not cell_ids:
        return out
    assessments = {
        ca.grid_cell_id: ca for ca in
        db.query(CellAssessment).filter(CellAssessment.grid_cell_id.in_(cell_ids)).all()
    }
    for m, frac_map in coverage_by_measure:
        for cid, frac in frac_map.items():
            ca = assessments.get(cid)
            if not ca:
                continue
            cell_risk = ((ca.data or {}).get("risks", {}) or {}).get(ALLERGY_RISK_CODE, {})
            factor = _stadtbaum_cell_factor(m.config, frac, cell_risk)
            out[cid] = out.get(cid, 1.0) * factor
    return out


def _measure_cell_factor(mdef: dict, config: dict | None, code: str, frac: float,
                         unit_factor: float, cell_risk: dict,
                         delta_hap: float = 1.0, hap_cap: float = 1.0,
                         s158_days_factor: float = 1.0, delta_vg: float = 1.0,
                         vg_cap: float = 1.0) -> float:
    """Faktor einer Maßnahme auf ein verknüpftes Risiko in einer Zelle.

    ``delta_hap`` wirkt nur auf S157, die Schutzprogramme und die Kühlzentren
    (Einzelnutzen), ``hap_cap`` nur auf die Kappung der Schutzprogramme und der
    Kühlzentren; ``delta_vg`` (Einzelnutzen) und ``vg_cap`` (Kappung) nur auf die
    Kühlzentren; ``s158_days_factor`` nur auf S158 (Ĝ′-Tage-Faktor einer gleichzeitigen
    Stadtbaumwahl derselben Kommune); sonst ohne Belang.

    COOLING_ROOMS_DRINKING_WATER rechnet zwei Hebel auf getrennte Gruppen: S157
    (Heimbewohner 85+) und öffentliche Kühlzentren (75+ zu Hause); die vermiedenen
    YLL werden addiert: 1 − (1 − f_S157) − (1 − f_KZ).
    """
    if _is_s157(mdef):
        if code != S157_RISK_CODE:
            return 1.0
        f_s157 = _s157_cell_factor(_s157_input(config), frac, cell_risk, delta_hap)
        # Wächter (Befund 150): liefen die Kühlzentren schon 2012–2024, gilt δ_KZ = 1;
        # S157 bleibt davon unberührt (eigener Abzug über heat.s_gek_kalib).
        f_kz = 1.0 if _vg_kalib_input(config) else _kz_cell_factor(
            frac, cell_risk, delta_hap, hap_cap, delta_vg, vg_cap)
        return max(0.0, f_s157 + f_kz - 1.0)
    if _is_vg(mdef):
        # Wächter (Befund 150): lief das Programm schon 2012–2024, gilt δ_VG = δ_VG,morb = 1.
        if _vg_kalib_input(config):
            return 1.0
        return _vg_cell_factor(code, frac, cell_risk, delta_hap, hap_cap)
    if _is_s158(mdef):
        if code != ALLERGY_RISK_CODE:
            return 1.0
        return _s158_cell_factor(mdef, frac, cell_risk, s158_days_factor)
    if _is_stadtbaum(mdef):
        if code != ALLERGY_RISK_CODE:
            return 1.0
        return _stadtbaum_cell_factor(config, frac, cell_risk)
    return _reduction_factor(mdef, frac, unit_factor)


# Befund 129: Hitzeaktionsplan und S157 zusammen — Faktoren multiplizieren.
S157_HAP_CODE = "HEAT_ACTION_PLANS"


def _hap_measures(db: Session, measure: AdaptationMeasure) -> list[AdaptationMeasure]:
    """Hitzeaktionspläne derselben Kommune (und derselben Demo-Sitzung) wie ``measure``."""
    return [m for m in kommune_measures_query(db, measure.kommune_id, measure.demo_session_id)
            .filter(AdaptationMeasure.measure_type == S157_HAP_CODE).all()
            if m.id != measure.id]


def _vg_measures(db: Session, measure: AdaptationMeasure) -> list[AdaptationMeasure]:
    """Schutzprogramme (effect_model ``vg``) derselben Kommune und Demo-Sitzung wie ``measure``.

    Grundlage der Kappung der Kühlzentren ``max(δ_HAP × δ_VG × δ_KZ; kappung_vg)``.
    Programme, die schon in den Kalibrierjahren liefen (Wächter, Befund 150), haben
    δ_VG = 1 und zählen deshalb weder zur Dämpfung noch zur Kappung.
    """
    return [m for m in kommune_measures_query(db, measure.kommune_id, measure.demo_session_id)
            .all()
            if m.id != measure.id
            and catalog.MEASURES_BY_CODE.get(m.measure_type, {}).get("effect_model") == "vg"
            and not _vg_kalib_input(m.config)]


def _vg_cell_fracs(db: Session, measures: list[AdaptationMeasure]) -> dict[int, list[float]]:
    """Deckungsgrade der Schutzprogramme je Zelle (für ``_vg_kz_factors``)."""
    out: dict[int, list[float]] = {}
    for m in measures:
        frac_map, _ = _coverage(db, m)
        for cid, frac in frac_map.items():
            out.setdefault(cid, []).append(frac)
    return out


def _hap_cell_factors(db: Session, measure: AdaptationMeasure,
                      overrides: dict) -> dict[int, float]:
    """δ_HAP je Zelle aus den gewählten Hitzeaktionsplänen der Kommune.

    Derselbe Faktor wie im Aggregat „mit Maßnahmen“ (``_reduction_factor`` mit
    Deckungsgrad und Stückfaktor); mehrere Pläne wirken wie dort multiplikativ.
    """
    mbase = catalog.MEASURES_BY_CODE.get(S157_HAP_CODE)
    if not mbase or S157_RISK_CODE not in (mbase.get("linked_risk_codes") or []):
        return {}
    mdef = parameter_registry.resolve_measure_def(mbase, overrides)
    out: dict[int, float] = {}
    for m in _hap_measures(db, measure):
        frac_map, covered_area_m2 = _coverage(db, m)
        count, _, recommended = _resolve_count(mdef, m.config, covered_area_m2)
        unit_factor = _unit_effect_factor(count, recommended)
        for cid, frac in frac_map.items():
            out[cid] = out.get(cid, 1.0) * _reduction_factor(mdef, frac, unit_factor)
    return out


def _s157_summary_fields(mdef: dict, config: dict | None) -> dict:
    """Zusatzfelder des impact_summary für S157.

    ``s_gek`` ist der gerechnete Anteil (Eingabe oder Voreinstellung 0,11),
    ``s_gek_is_default`` sagt, ob die Voreinstellung gilt, ``s_gek_kalib`` ist der
    abgezogene Stand der Kalibrierjahre. ``s157_estimate_note`` kennzeichnet den
    Betrag als begründete Abschätzung von KAP3 (P2: heat.s_gek, heat.s_gek_kalib und
    heat.g_s157 sind Abschätzungen, keine belegten Effektgrößen).
    """
    if not _is_s157(mdef):
        return {}
    return {
        "s_gek": _s157_input(config),
        "s_gek_is_default": _s157_config_value(config) is None,
        "s_gek_kalib": _s157_param("s_gek_kalib", S157_S_GEK_KALIB_DEFAULT),
        "s157_estimate_note": S157_ESTIMATE_NOTE,
    }


def _s158_summary_fields(mdef: dict, avoided_days_total: float,
                         avoided_days_eur: float, missing_split: bool) -> dict:
    """Zusatzfelder des impact_summary für S158 (Integrationsauflage Punkt 5).

    ``s158_avoided_days_total``/``s158_avoided_days_eur`` sind die vermiedenen
    Symptomtage bzw. Euro/Jahr der Kommune (Summe der Zellwerte), zusammen mit der
    Kennzeichnung ``s158_estimate_note`` als begründete Abschätzung von KAP3 (P2:
    ``r_S158``, ``t_warn`` sind keine belegten Effektgrößen). Fehlt in einer
    abgedeckten Zelle mit Zusatztagen die Gruppenaufteilung, wäre die Kommunensumme
    zu niedrig, ohne dass das sichtbar würde — dann steht der Vermerk statt eines
    Betrags (``benefit_display``), und die Zahlenfelder entstehen nicht (kein 0 €).
    """
    if not _is_s158(mdef):
        return {}
    if missing_split:
        return {
            "benefit_display": S158_MISSING_SPLIT_TEXT,
            "benefit_missing_input": "pollen_group_split",
        }
    return {
        "s158_avoided_days_total": round(avoided_days_total, 1),
        "s158_avoided_days_eur": round(avoided_days_eur, 2),
        "s158_estimate_note": S158_ESTIMATE_NOTE,
    }


def _resolve_count(
    mdef: dict, config: dict | None, covered_area_m2: float
) -> tuple[int, bool, int]:
    """Stückzahl, Default-Flag und Richtwert-Anzahl einer Maßnahme.

    Flächenmaßnahmen (``unit_label`` is None) haben keine Stück-Logik ⇒
    (0, False, 0). Fehlt ``config["count"]``, greift die Richtwert-Anzahl aus der
    Dichte als Default (``is_default=True``), damit Bestandsmaßnahmen ohne
    Frontend-Eingabe weiter sinnvoll rechnen.
    """
    if mdef.get("unit_label") is None:
        return 0, False, 0
    raw = (config or {}).get("count")
    if mdef.get("count_pflicht") and mdef.get("unit_density_per_ha") is None:
        # Pflichteingabe ohne Richtwert (Stadtbaumwahl, Bericht #96 §5, Ü-11 (c)): ohne
        # Eingabe keine Richtwert-Anzahl, sondern (0, False, 0) und ein Vermerk statt
        # der Kosten; die Stückzahl skaliert die Wirkung nicht (Richtwert 0).
        if raw is None:
            return 0, False, 0
        return max(0, int(round(float(raw)))), False, 0
    density = float(mdef.get("unit_density_per_ha") or 0.0)
    recommended = max(1, round(density * covered_area_m2 / 10_000))
    if raw is None:
        return recommended, True, recommended
    return max(0, int(round(float(raw)))), False, recommended


def _unit_effect_factor(count: int, recommended_count: int) -> float:
    """Wirkungs-Skalierung 0..1 aus Anzahl vs. Richtwert (1.0 ohne Stück-Logik)."""
    if recommended_count > 0:
        return min(1.0, count / recommended_count)
    return 1.0


# Kostenkomponenten je Block (CAPEX einmalig / OPEX jährlich). quantity_kind:
# fixed = mengenunabhängige Pauschale (Menge 1), unit = Stückzahl (Einheit = unit_label),
# area = Fläche (Einheit m²).
_CAPEX_COMPONENTS: tuple[tuple[str, str, str], ...] = (
    ("capex_fixed", "Grundkosten (Planung/Konzept)", "fixed"),
    ("capex_per_unit", "Investition je {unit}", "unit"),
    ("capex_per_m2", "Investition je m²", "area"),
)
_OPEX_COMPONENTS: tuple[tuple[str, str, str], ...] = (
    ("opex_fixed_year", "Feste Betriebskosten/Jahr", "fixed"),
    ("opex_per_unit_year", "Betrieb & Unterhalt je {unit}/Jahr", "unit"),
    ("opex_per_m2_year", "Betrieb & Unterhalt je m²/Jahr", "area"),
)


def _component_source(mdef: dict, field: str) -> tuple[str, str, bool]:
    """(Quelle, Herleitung/Detail, overridden) einer Kostenkomponente.

    ``source`` ist das kurze Inline-Label (z. B. "Berliner Wasserbetriebe"),
    ``detail`` die ausführliche Herleitung/Volltext-Quelle für den Hover-Tooltip:
    woher der Zahlenwert stammt bzw. – wenn er nicht direkt einer Quelle entnommen
    ist – wie er hergeleitet/plausibilisiert wurde. Ein kommunaler
    ``custom_source``-Override hat beim Kurz-Label Vorrang.
    """
    custom = (mdef.get("custom_sources") or {}).get(field)
    detail = (mdef.get("source_details") or {}).get(field) or ""
    if custom:
        return custom, detail, True
    source = (mdef.get("sources") or {}).get(field) or mdef.get("source") or ""
    return source, detail, False


def compute_costs(mdef: dict, count: int, area_m2: float) -> dict:
    """Kosten-Rohdaten (capex + opex) mit Komponenten-Breakdown.

    CAPEX  = capex_fixed + count·capex_per_unit + area·capex_per_m2,
    OPEX/a = opex_fixed_year + count·opex_per_unit_year + area·opex_per_m2_year.
    Nur Komponenten, deren Katalogfeld ``is not None`` ist, tauchen auf; ``0.0``
    gilt als anwendbar (z. B. kostenlose Bauverbote). Jede Komponente trägt
    Einzelpreis, Menge, Betrag und Quelle inkl. Override-Flag.
    """
    unit_label = mdef.get("unit_label") or "Einheit"

    def _block(specs: tuple[tuple[str, str, str], ...]) -> dict:
        components: list[dict] = []
        total = 0.0
        for field, label_tpl, kind in specs:
            unit_price = mdef.get(field)
            if unit_price is None:
                continue
            unit_price = float(unit_price)
            if kind == "unit":
                quantity, quantity_unit = count, unit_label
            elif kind == "area":
                quantity, quantity_unit = round(float(area_m2), 2), "m²"
            else:  # fixed
                quantity, quantity_unit = 1, "pauschal"
            amount = round(unit_price * quantity, 2)
            total += amount
            source, source_detail, overridden = _component_source(mdef, field)
            refs = sources.resolve((mdef.get("source_refs") or {}).get(field))
            components.append({
                "param": field,
                "label": label_tpl.format(unit=unit_label),
                "unit_price": unit_price,
                "quantity": quantity,
                "quantity_unit": quantity_unit,
                "amount_eur": amount,
                "source": source,
                "source_detail": source_detail,
                "references": refs,
                "overridden": overridden,
            })
        return {"total_eur": round(total, 2), "components": components}

    return {
        "capex": _block(_CAPEX_COMPONENTS),
        "opex": _block(_OPEX_COMPONENTS),
    }


# ── Verwechslungssperre Klasse A/B im Maßnahmen-Nutzen (T-0838) ──────────────────
# Klasse-B-Wirkungen (``"euro_layer": False``, reines Screening) tragen keinen
# Euro-Betrag — auch dann nicht, wenn ihr Katalogeintrag einen Kostensatz > 0 führt.
# ``catalog.risk_contributes_to_total`` prüft die Euro-Schicht nicht (sie trägt Summe
# und Untergrenze, T-0515) und bleibt unverändert; der Maßnahmen-Nutzen und sein
# Deckel sind deshalb zusätzlich an ``catalog.risk_has_euro_layer`` gebunden.


def _risk_counts_for_euro_benefit(risk: dict | None) -> bool:
    """True, wenn eine verknüpfte Wirkung einen Euro-Nutzen tragen darf.

    Bedingung: sie trägt zur Gesamtschadenssumme bei **und** führt eine
    Euro-Schicht (Klasse A). Klasse B liefert weder Zell-/flat-Nutzen noch
    einen Beitrag zum Deckel.
    """
    return bool(risk) and catalog.risk_contributes_to_total(risk) \
        and catalog.risk_has_euro_layer(risk)


def _benefit_cap(linked: list[str], base_risks: dict, k_indirect: float) -> float:
    """Deckel des Schadens-Nutzens: Basisschaden der verknüpften pop-/area-Wirkungen
    mit Euro-Schicht (inkl. gekoppelter Folgekosten direkter Sektorschäden).

    Liest ``cost_eur`` des Basis-Aggregats nur für Klasse A — ein Klasse-B-Betrag
    geht nie in den Deckel ein, auch wenn das Aggregat dort (noch) eine Zahl führt.
    """
    cap = 0.0
    for code in linked:
        risk = catalog.RISKS_BY_CODE.get(code)
        entry = (base_risks or {}).get(code)
        if not entry or not _risk_counts_for_euro_benefit(risk):
            continue
        if risk.get("scale", "pop") in ("pop", "area"):
            cost = float(entry.get("cost_eur") or 0.0)
            cap += cost
            if code in catalog.DIRECT_SECTOR_RISK_CODES:
                cap += k_indirect * cost  # gekoppelte Folgekosten zählen zum Nutzen dazu
    return cap


def _benefit_euro_layer_fields(linked: list[str], direct_benefit_eur: float = 0.0) -> dict:
    """Vermerkfelder zur Euro-Schicht des Maßnahmen-Nutzens (Entscheidung CEO, T-0563).

    - ``benefit_has_euro_layer``: False, wenn alle verknüpften (im Katalog bekannten)
      Wirkungen Klasse B sind. Dann gibt es keinen Euro-Nutzen aus vermiedenen Schäden
      — auch keine 0 (P2) —, kein Nutzen-Kosten-Verhältnis und keinen Rangplatz nach Euro.
    - ``benefit_display``: bei einer reinen Klasse-B-Maßnahme
      ``catalog.NO_EURO_LAYER_TEXT`` statt eines Betrags, sonst None (Betrag gilt).
      Hat die reine Screening-Maßnahme einen direkten Zusatznutzen > 0
      (``direct_benefit_eur``; eigener, mit Quelle geführter Parameter), gilt der Betrag:
      ``benefit_display`` None, dazu der Zusatz in ``benefit_note``.
      ``benefit_has_euro_layer`` bleibt False (kein Nutzen aus vermiedenen Schäden).
    - ``benefit_note``: bei einer gemischten Maßnahme der Zusatz
      „ohne x Wirkungen im Screening“ zum Euro-Nutzen aus den Klasse-A-Wirkungen.
    - ``benefit_screening_risk_codes``: die verknüpften Klasse-B-Wirkungen.
    """
    known = [c for c in linked if c in catalog.RISKS_BY_CODE]
    screening = [c for c in known
                 if not catalog.risk_has_euro_layer(catalog.RISKS_BY_CODE[c])]
    pure_screening = bool(known) and len(screening) == len(known)
    note = None
    show_direct = pure_screening and float(direct_benefit_eur or 0.0) > 0.0
    if screening and (not pure_screening or show_direct):
        n = len(screening)
        note = f"ohne {n} {'Wirkung' if n == 1 else 'Wirkungen'} im Screening"
    return {
        "benefit_has_euro_layer": not pure_screening,
        "benefit_display": (catalog.NO_EURO_LAYER_TEXT
                            if pure_screening and not show_direct else None),
        "benefit_note": note,
        "benefit_screening_risk_codes": screening,
    }


# Kosten-/nutzenrelevante Felder der (aufgelösten) Maßnahmendefinition: ändert sich
# eines davon (Katalog-Rekalibrierung oder Override), ist ein gespeichertes
# impact_summary veraltet und muss neu gerechnet werden.
_FINGERPRINT_MDEF_FIELDS = (
    "capex_fixed", "capex_per_unit", "capex_per_m2",
    "opex_fixed_year", "opex_per_unit_year", "opex_per_m2_year",
    "benefit_per_m2_year", "default_reduction", "coverage_scaling",
    "effect_target", "linked_risk_codes", "unit_density_per_ha", "unit_label",
)


def _params_fingerprint(db: Session, measure: AdaptationMeasure, mdef: dict,
                        overrides: dict) -> str:
    """Fingerprint der Rechengrundlage eines impact_summary (Staleness-Erkennung).

    Deckt ab: (a) Katalog-/Override-Änderungen an den kosten-/nutzenrelevanten
    mdef-Feldern, (b) alle übrigen Kommune-Overrides (k_indirekt, Kostensätze,
    Sättigung/Kappung wirken in _cell_cost/_reduction_factor), (c) Modellversion,
    (d) Zelldaten-Stand (assessment_task baut Zellen neu, rechnet Impacts aber
    nicht neu) und (e) die Maßnahmen-Konfiguration (Stückzahl).
    """
    cells_marker = db.query(sa_func.max(CellAssessment.calculated_at)).filter(
        CellAssessment.kommune_id == measure.kommune_id).scalar()
    payload = {
        "mdef": {k: mdef.get(k) for k in _FINGERPRINT_MDEF_FIELDS
                 + tuple(f for f, _, _ in (mdef.get("zusatz_kostenfelder") or ()))},
        "overrides": sorted((str(k), str(v)) for k, v in (overrides or {}).items()),
        "config": measure.config or {},
        "model_version": catalog.MODEL_VERSION,
        "cells": str(cells_marker),
        # Euro-Schicht der verknüpften Wirkungen (T-0838): wird eine Wirkung im
        # Katalog zu Klasse B, ist ein gespeicherter Euro-Nutzen veraltet.
        "euro_layer": {
            c: catalog.risk_has_euro_layer(catalog.RISKS_BY_CODE[c])
            for c in (mdef.get("linked_risk_codes") or [])
            if c in catalog.RISKS_BY_CODE
        },
    }
    if _is_s157(mdef) or _is_vg(mdef):
        # Befund 129: der Nutzen von S157 hängt an den Hitzeaktionsplänen der Kommune
        # (Schutzprogramme ebenso, Kappung mit δ_HAP, Befund 126);
        # kommt einer hinzu, ändert sich oder fällt weg, ist das Summary veraltet.
        payload["hap"] = sorted(
            (m.id, json.dumps(m.config or {}, sort_keys=True, default=str), str(m.geometry))
            for m in _hap_measures(db, measure))
    if _is_s157(mdef):
        # Kühlzentren (Bericht #95 §5 Z. 1234–1238): Kappung und Dämpfung hängen an den
        # Schutzprogrammen der Kommune; ändern sie sich, ist das Summary veraltet.
        payload["vg"] = sorted(
            (m.id, json.dumps(m.config or {}, sort_keys=True, default=str), str(m.geometry))
            for m in _vg_measures(db, measure))
    if _is_s158(mdef):
        # Bericht §5 „Zusammen mit S158" (T-1602-cto): der Nutzen von S158 hängt an
        # der Stadtbaumwahl derselben Kommune (kein vermiedener Tag zählt doppelt);
        # kommt eine hinzu, ändert sich oder fällt weg, ist das Summary veraltet.
        payload["stadtbaum"] = sorted(
            (m.id, json.dumps(m.config or {}, sort_keys=True, default=str), str(m.geometry))
            for m in _stadtbaum_measures(db, measure))
    return hashlib.sha1(
        json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def ensure_fresh_impact_summary(db: Session, measure: AdaptationMeasure) -> dict:
    """Liefert das impact_summary der Maßnahme, bei veralteter Rechengrundlage
    (Fingerprint-Mismatch) wird es zuerst per ``compute_impact`` neu berechnet.

    Zentrale Absicherung aller Lesepfade (cost-summary, Export, Maßnahmenliste):
    ohne sie reichte z. B. eine Katalog-Rekalibrierung (benefit_per_m2_year
    1,5 → 0,02 €/m²) aus, um Nutzen-Zahlen um Größenordnungen zu verfälschen,
    weil nur der manuelle calculate-impact-Endpunkt neu rechnet.
    """
    summary = measure.impact_summary or {}
    mbase = catalog.MEASURES_BY_CODE.get(measure.measure_type)
    if mbase is None:
        return summary
    db_overrides = parameter_registry.load_db_overrides(db, measure.kommune_id)
    overrides = parameter_registry.overrides_map(db_overrides)
    mdef = parameter_registry.resolve_measure_def(mbase, overrides)
    fp = _params_fingerprint(db, measure, mdef, overrides)
    if summary.get("params_fingerprint") == fp:
        return summary
    log.info("Impact-Summary von Maßnahme %s (%s) veraltet — wird neu berechnet.",
             measure.id, measure.measure_type)
    try:
        # Kein aggregate_cache.invalidate nötig: die Aggregate rechnen die Maßnahmen-
        # Faktoren live aus der Definition und lesen impact_summary nicht.
        return compute_impact(db, measure.id)
    except ValueError:
        return summary


def _measure_custom_sources(db_overrides: list[dict], measure_code: str) -> dict[str, str]:
    """Per-Feld ``custom_source``-Overrides einer Maßnahme (measures.<code>.<field>)."""
    prefix = f"measures.{measure_code}."
    out: dict[str, str] = {}
    for o in db_overrides:
        pid = o.get("parameter_id") or ""
        cs = o.get("custom_source")
        if cs and pid.startswith(prefix):
            out[pid[len(prefix):]] = cs
    return out


def compute_impact(db: Session, measure_id: int) -> dict:
    """Berechnet die Wirkung einer Maßnahme, speichert MeasureImpact und gibt
    eine Zusammenfassung (Index-Reduktion, Kosten, Nutzen) zurück."""
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise ValueError(f"Maßnahme {measure_id} nicht gefunden")

    mdef = catalog.MEASURES_BY_CODE.get(measure.measure_type)
    if not mdef:
        # M0-Verschlankung: Alt-Maßnahmen geparkter Typen bleiben in der DB,
        # sind aber bis zur Re-Expansion (Stage 1+) nicht berechenbar.
        raise ValueError(
            f"Maßnahmentyp {measure.measure_type} ist derzeit nicht im aktiven "
            "Katalog (M0-Verschlankung; kehrt mit einer späteren Roadmap-Stufe zurück)"
        )

    db_overrides = parameter_registry.load_db_overrides(db, measure.kommune_id)
    overrides = parameter_registry.overrides_map(db_overrides)
    mdef = parameter_registry.resolve_measure_def(mdef, overrides)
    mdef = {**mdef, "custom_sources": _measure_custom_sources(db_overrides, measure.measure_type)}
    fingerprint = _params_fingerprint(db, measure, mdef, overrides)

    # Kommune-Overrides für alle Live-Reads dieses Laufs installieren (k_indirekt,
    # Kostensätze in _cell_cost, Sättigung/Kappung in _reduction_factor): ohne Scope
    # läse dieser Request-Pfad die Overrides der zuletzt gerechneten Kommune
    # (Cross-Kommune-Leak, MODELL_KRITIK §8/B2).
    with override_context.override_scope(overrides):
        return _compute_impact_scoped(db, measure, mdef, fingerprint)


def _compute_impact_scoped(db: Session, measure: AdaptationMeasure, mdef: dict,
                           fingerprint: str) -> dict:
    """Kern von ``compute_impact`` — läuft innerhalb des Override-Scopes der Kommune."""
    measure_id = measure.id
    coverage, covered_area_m2 = _coverage(db, measure)
    if not coverage:
        db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()
        no_coverage = {"measure_id": measure_id, "affected_cells": 0,
                       "message": "Keine überlappenden Zellen",
                       "params_fingerprint": fingerprint}
        measure.impact_summary = no_coverage
        db.commit()
        return no_coverage

    # Anzahl/Wirkungsskalierung brauchen die Gesamtfläche vor der Zell-Schleife.
    count, count_is_default, recommended_count = _resolve_count(mdef, measure.config, covered_area_m2)
    unit_factor = _unit_effect_factor(count, recommended_count)

    linked = mdef.get("linked_risk_codes", [])
    cell_ids = list(coverage.keys())
    assessments = {
        ca.grid_cell_id: ca for ca in
        db.query(CellAssessment).filter(CellAssessment.grid_cell_id.in_(cell_ids)).all()
    }

    db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()

    # Nutzen = tatsächliches Delta der summierten Zellkosten (E3): je abgedeckter Zelle
    # und verknüpftem Risiko  Zellkosten · (1 − factor). Für pop-/area-skalierte Risiken
    # ist das exakt der Beitrag dieser Maßnahme zu „Vermiedene Schäden" (Σ-über-Zellen im
    # Aggregat), weil dieselbe Zellkosten-Basis (``_cell_cost`` = Aggregat-Basis) und
    # derselbe multiplikative Zell-Faktor benutzt werden. Flache Ausfall-Risiken
    # (kommunenweiter P90-Einzelwert) sind nicht zell-additiv — ihr Nutzen wird unten
    # separat als Delta der kommunenweiten P90-Outcome-Kosten gerechnet.
    covered_base_index: dict[str, float] = {}
    covered_new_index: dict[str, float] = {}
    annual_benefit_damage = 0.0
    # Vermeidet eine Maßnahme direkte Sektorschäden, sinken auch die daran gekoppelten
    # Folgekosten (indirekt = k · Σ direkte Schäden). Dieser Anteil wird im Kommunen-
    # Aggregat „mit Maßnahmen" über die Rekonsolidierung (siehe _adjusted_cell_data)
    # mitreduziert; damit der Einzelmaßnahmen-Nutzen dazu passt, wird er hier ergänzt (§8/B3).
    k_indirect = float(override_context.get_override("impact.k_indirect", _K_INDIRECT_DEFAULT))

    # Befund 129: Hat die Kommune zugleich einen Hitzeaktionsplan, rechnet S157 seinen
    # Nutzen aus dem schon mit δ_HAP gedämpften Heim-Exzess (Faktoren multipliziert).
    # So ergibt die Summe der Einzelnutzen genau das Aggregat „mit Maßnahmen“.
    # Die Schutzprogramme ebenso, dazu Kappung max(δ_HAP × δ_VG; 0,794) (Befund 126).
    hap_by_cell: dict[int, float] = {}
    if _is_s157(mdef) or _is_vg(mdef):
        hap_by_cell = _hap_cell_factors(db, measure, parameter_registry.overrides_map(
            parameter_registry.load_db_overrides(db, measure.kommune_id)))

    # Kühlzentren (Bericht #95 §5 Z. 1234–1238): Schutzprogramme derselben Kommune je
    # Zelle — sie dämpfen den Einzelnutzen der Kühlzentren und gehen in die Kappung
    # max(δ_HAP × δ_VG × δ_KZ; kappung_vg) ein. Der Betrag der Kühlzentren wird getrennt
    # von S157 gezählt (Befunde 139, 148).
    vg_fracs_by_cell: dict[int, list[float]] = {}
    kz_benefit = 0.0
    if _is_s157(mdef):
        vg_fracs_by_cell = _vg_cell_fracs(db, _vg_measures(db, measure))

    # Bericht §5 „Zusammen mit S158" (T-1602-cto): deckt zugleich eine Stadtbaumwahl
    # derselben Kommune dieselbe Zelle ab, rechnet S158 seinen Nutzen aus den schon um
    # die Pflanzung geminderten Tagen (Faktoren multipliziert) — kein vermiedener Tag
    # zählt doppelt.
    stadtbaum_by_cell: dict[int, float] = {}
    if _is_s158(mdef):
        stadtbaum_by_cell = _stadtbaum_cell_days_factors(db, measure)

    # S158-Integrationsauflage Punkt 5: vermiedene Symptomtage der Kommune (Summe der
    # Zellwerte, identisch zur Summe der MeasureImpact-Zeilen) und ihr Euro-Gegenwert
    # (Anteil #96 an ``annual_benefit_damage_eur`` — dieselbe Maßnahme verknüpft nur
    # ALLERGY_RISK_CODE, deshalb ist der Anteil die gesamte Zellkosten-Reduktion).
    s158_avoided_days_total = 0.0
    s158_missing_split = False

    # Integrationsauflage (Stadtbaumwahl) §5 Punkt (4): vermiedene Zusatztage der
    # Kommune (Summe der Zellwerte) und ihr Euro-Gegenwert. Fehlt ``anteil_ersetzt``
    # (Punkt 2 der Auflage), lässt sich die Wirkung ohne Eingabe nicht bestimmen —
    # das gilt für die ganze Maßnahme, nicht je Zelle, deshalb hier vorab geprüft.
    stadtbaum_avoided_days_total = 0.0
    stadtbaum_missing_reason: str | None = None
    stadtbaum_saw_canopy_missing = False
    stadtbaum_saw_effect = False
    if _is_stadtbaum(mdef):
        _a_ersetzt = float((measure.config or {}).get("anteil_ersetzt") or 0.0)
        if _a_ersetzt <= 0.0:
            stadtbaum_missing_reason = "anteil_ersetzt"
        elif _a_ersetzt > 1.0:
            stadtbaum_missing_reason = STADTBAUM_ANTEIL_BEREICH_REASON

    for cid, frac in coverage.items():
        ca = assessments.get(cid)
        if not ca:
            continue
        data = ca.data or {}
        cell_pop = float(data.get("inputs", {}).get("pop", 0.0) or 0.0)
        cell_risks = data.get("risks", {})
        deltas = {}
        cell_savings: dict[str, float | str] = {}
        for code in linked:
            r = _with_cell_q_pfl(cell_risks.get(code, {}), data.get("inputs"))
            d_hap = hap_by_cell.get(cid, 1.0)
            s158_days_factor = stadtbaum_by_cell.get(cid, 1.0)
            d_vg, vg_cap = 1.0, 1.0
            if _is_s157(mdef) and code == S157_RISK_CODE:
                d_vg, vg_cap = _vg_kz_factors(vg_fracs_by_cell.get(cid, []), r, d_hap)
            factor = _measure_cell_factor(mdef, measure.config, code, frac, unit_factor, r,
                                          d_hap, d_hap, s158_days_factor, d_vg, vg_cap)
            if _is_s158(mdef) and s158_days_factor != 1.0:
                # Doppelzähler (Befund 240, Ü-7): Der S158-Faktor ist ein Anteil an den Tagen
                # NACH der Pflanzung (Nenner total_adj). Auf Index und Kosten des Ausgangsstands
                # angewandt, würde er auch Tage mindern, die die Stadtbaumwahl schon vermieden
                # hat. Deshalb Minderung = Index/Kosten × days_factor × (1 − factor).
                factor = 1.0 - max(0.0, float(s158_days_factor)) * (1.0 - factor)
            base_idx = float(r.get("index", 0.0))
            new_idx = base_idx * factor
            deltas[code] = round(new_idx - base_idx, 3)
            covered_base_index[code] = covered_base_index.get(code, 0.0) + base_idx
            covered_new_index[code] = covered_new_index.get(code, 0.0) + new_idx
            if _is_s158(mdef) and code == ALLERGY_RISK_CODE:
                _, avoided_days, missing = _s158_cell_effect(mdef, frac, r, s158_days_factor)
                if missing:
                    s158_missing_split = True
                elif avoided_days is not None:
                    cell_savings["s158_avoided_days"] = round(avoided_days, 3)
                    # Euro je Zelle (Befund 237, Ü-4): vermiedene Tage × c_Tag des
                    # Risikos (Katalog-Kostensatz pollen.c_tag, mit Override wie die
                    # Zellkosten), gerundet auf 0,01 €.
                    cell_savings["s158_avoided_eur"] = round(risk_engine.cost_from_outcome(
                        catalog.RISKS_BY_CODE[code], avoided_days), 2)
                    s158_avoided_days_total += avoided_days
            if (_is_stadtbaum(mdef) and code == ALLERGY_RISK_CODE
                    and stadtbaum_missing_reason is None):
                _, avoided_days, reason = _stadtbaum_cell_effect(measure.config, frac, r)
                if reason == "canopy":
                    # Zellweiser Vermerk (Befund Prüfer, Runde 1): Eine kronenlose Zelle
                    # bekommt einen Grund statt still zu verschwinden — auch bei
                    # gemischter Deckung, wo die Kommunensumme insgesamt positiv bleibt
                    # (dann bleibt ``stadtbaum_missing_reason`` auf Kommunenebene leer,
                    # s. unten).
                    stadtbaum_saw_canopy_missing = True
                    cell_savings["stadtbaum_missing_reason"] = "canopy"
                elif avoided_days is not None:
                    cell_savings["stadtbaum_avoided_days"] = round(avoided_days, 3)
                    # Euro je Zelle (Befund 237, Ü-4), Rechnung wie bei S158.
                    cell_savings["stadtbaum_avoided_eur"] = round(risk_engine.cost_from_outcome(
                        catalog.RISKS_BY_CODE[code], avoided_days), 2)
                    stadtbaum_avoided_days_total += avoided_days
                    if avoided_days > 0.0:
                        stadtbaum_saw_effect = True
            risk = catalog.RISKS_BY_CODE.get(code)
            if (_risk_counts_for_euro_benefit(risk)
                    and risk.get("scale", "pop") in ("pop", "area")):
                reduced = _cell_cost(risk, r, cell_pop) * (1.0 - factor)
                annual_benefit_damage += reduced
                if _is_s157(mdef) and code == S157_RISK_CODE:
                    f_kz = 1.0 if _vg_kalib_input(measure.config) else _kz_cell_factor(
                        frac, r, d_hap, d_hap, d_vg, vg_cap)
                    kz_benefit += min(reduced, _cell_cost(risk, r, cell_pop) * (1.0 - f_kz))
                # gekoppelte Folgekosten (nur direkte Sektorschäden treiben k_indirekt)
                if code in catalog.DIRECT_SECTOR_RISK_CODES:
                    annual_benefit_damage += k_indirect * reduced
        db.add(MeasureImpact(measure_id=measure_id, grid_cell_id=cid, indicator_deltas=deltas,
                              savings=cell_savings))

    # Flat-skalierte verknüpfte Risiken (z. B. Ausfallstunden bei Netzverstärkung):
    # Das Aggregat rechnet sie als kommunenweiten P90-Outcome — der Nutzen dieser
    # Maßnahme ist die Differenz der P90-Outcome-Kosten ohne/mit ihrem Zell-Faktor
    # (identische Logik wie ``_adjusted_cell_data``/``aggregate``, inkl. Pop-Skalierung
    # der flat-€-Bewertung). Vorher zeigten solche Maßnahmen hier 0 € Nutzen trotz
    # CAPEX. Deckt die Maßnahme zu wenige Zellen ab, um das P90 zu bewegen, bleibt der
    # Nutzen ehrlich 0 (konsistent: auch das Aggregat würde sich nicht ändern).
    annual_benefit_flat = 0.0
    flat_linked = [
        catalog.RISKS_BY_CODE[c] for c in linked
        if c in catalog.RISKS_BY_CODE
        and catalog.RISKS_BY_CODE[c].get("scale", "pop") not in ("pop", "area")
        and _risk_counts_for_euro_benefit(catalog.RISKS_BY_CODE[c])
    ]
    if flat_linked:
        kommune = db.query(Kommune).filter(Kommune.id == measure.kommune_id).first()
        total_pop = float(kommune.population or 0) if kommune else 0.0
        kommune_area_km2 = float(kommune.area_km2 or 0) if kommune else 0.0
        all_rows = db.query(CellAssessment).filter(
            CellAssessment.kommune_id == measure.kommune_id).all()
        for risk in flat_linked:
            rcode = risk["code"]
            base_indices: list[float] = []
            adj_indices: list[float] = []
            for ca in all_rows:
                idx = float((ca.data or {}).get("risks", {}).get(rcode, {}).get("index", 0.0))
                base_indices.append(idx)
                frac = coverage.get(ca.grid_cell_id)
                if frac:
                    idx *= _reduction_factor(mdef, frac, unit_factor)
                adj_indices.append(idx)
            base_p90 = risk_engine._percentile(base_indices)
            adj_p90 = risk_engine._percentile(adj_indices)
            if adj_p90 >= base_p90:
                continue
            base_cost = risk_engine.estimate_outcome_and_cost(
                risk, base_p90, total_pop, kommune_area_km2)["cost_eur"]
            adj_cost = risk_engine.estimate_outcome_and_cost(
                risk, adj_p90, total_pop, kommune_area_km2)["cost_eur"]
            annual_benefit_flat += max(0.0, base_cost - adj_cost)

    # Defense-in-depth: Der Schadens-Nutzen einer Maßnahme kann strukturell nicht über
    # dem Gesamt-Basisschaden ihrer verknüpften Risiken liegen (Zell-Deltas ⊆ Zellsumme).
    # Die Kappung fängt künftige Fehlkalibrierungen/Inkonsistenzen ab, statt sie als
    # Millionen-Nutzen ins Dashboard durchzureichen.
    benefit_capped = False
    benefit_damage_uncapped = annual_benefit_damage
    if annual_benefit_damage > 0.0:
        base_agg = get_risk_aggregate(db, measure.kommune_id, apply_measures=False)
        k = float(override_context.get_override("impact.k_indirect", _K_INDIRECT_DEFAULT))
        cap = _benefit_cap(linked, base_agg.get("risks", {}), k)
        if cap > 0.0 and annual_benefit_damage > cap:
            log.warning(
                "Maßnahme %s: Schadens-Nutzen %.0f € über Gesamtschaden der verknüpften "
                "Risiken (%.0f €) — gekappt (Parameter prüfen).",
                measure_id, annual_benefit_damage, cap)
            annual_benefit_damage = cap
            benefit_capped = True

    # S158 verknüpft ausschließlich ALLERGY_RISK_CODE (#96) — ihr Euro-Anteil an
    # ``annual_benefit_damage_eur`` ist deshalb der ganze (ggf. gekappte) Betrag.
    s158_avoided_days_eur = annual_benefit_damage if _is_s158(mdef) else 0.0

    # Kühlzentren und S157 getrennt (COOLING_ROOMS_DRINKING_WATER verknüpft nur die
    # Mortalität): Bei einer Kappung schrumpfen beide Anteile im selben Verhältnis.
    kz_benefit_eur = 0.0
    if _is_s157(mdef) and benefit_damage_uncapped > 0.0:
        kz_benefit_eur = kz_benefit * annual_benefit_damage / benefit_damage_uncapped
    s157_benefit_eur = max(0.0, annual_benefit_damage - kz_benefit_eur) if _is_s157(mdef) else 0.0

    # Trägt am Ende KEINE abgedeckte Zelle einen positiven Effekt und lag zumindest
    # eine ohne Baumkronen im Ausgangsstand, wäre 0 € nicht von einer Datenlücke
    # unterscheidbar (P2) — dann steht der Vermerk statt des (korrekten, aber
    # irreführenden) Betrags. Die Stadtbaumwahl verknüpft ebenfalls ausschließlich
    # ALLERGY_RISK_CODE, ihr Euro-Anteil ist deshalb ebenso der ganze Betrag.
    if (stadtbaum_missing_reason is None and stadtbaum_saw_canopy_missing
            and not stadtbaum_saw_effect):
        stadtbaum_missing_reason = "canopy"
    stadtbaum_avoided_days_eur = annual_benefit_damage if _is_stadtbaum(mdef) else 0.0

    # Kosten (CAPEX + OPEX, je fix/Stück/Fläche; None-Felder erzeugen keine Komponente).
    # Stadtbaumwahl: capex_per_unit aus dem Zusatzfeld des gewählten Falls (Ü-11 (b)).
    cost_mdef, stadtbaum_kosten_felder = _stadtbaum_kosten(mdef, measure.config, count)
    cost_breakdown = compute_costs(cost_mdef, count, covered_area_m2)
    capex = cost_breakdown["capex"]["total_eur"]
    opex_annual = cost_breakdown["opex"]["total_eur"]
    annual_benefit_direct = float(mdef.get("benefit_per_m2_year") or 0.0) * covered_area_m2

    avg_reduction = 0.0
    if covered_base_index:
        tot_b = sum(covered_base_index.values())
        tot_n = sum(covered_new_index.values())
        avg_reduction = round((tot_b - tot_n) / tot_b * 100.0, 1) if tot_b > 0 else 0.0

    summary = {
        "measure_id": measure_id,
        "measure_type": measure.measure_type,
        "affected_cells": len(coverage),
        "affected_area_m2": round(covered_area_m2, 1),
        "linked_risk_codes": linked,
        "avg_index_reduction_pct": avg_reduction,
        "capex_eur": round(capex, 2),
        "opex_annual_eur": round(opex_annual, 2),
        "annual_benefit_eur": round(
            annual_benefit_direct + annual_benefit_damage + annual_benefit_flat, 2),
        # Transparente Aufschlüsselung: vermiedene Zellschäden (inkl. gekoppelter
        # Folgekosten), flat-Anteil (kommunenweite P90-Risiken) und direkter
        # Zusatznutzen (benefit_per_m2_year · Fläche, z. B. Mehrertrag/Erlöse) —
        # zwei konzeptionell verschiedene Dinge: nicht eintretender Schaden vs.
        # zusätzlich erwirtschafteter Nutzen.
        "annual_benefit_damage_eur": round(annual_benefit_damage, 2),
        "annual_benefit_flat_eur": round(annual_benefit_flat, 2),
        "annual_benefit_direct_eur": round(annual_benefit_direct, 2),
        "benefit_capped": benefit_capped,
        # Verwechslungssperre Klasse A/B (T-0838, T-0872): Vermerk statt Betrag für reine
        # Screening-Maßnahmen ohne direkten Zusatznutzen. Hat eine reine Screening-
        # Maßnahme einen direkten Zusatznutzen > 0, gilt dieser Betrag mit dem Zusatz
        # „ohne x Wirkungen im Screening“ — derselbe Zusatz wie für gemischte Maßnahmen.
        # ``annual_benefit_eur`` bleibt eine Zahl (Klasse-A-Anteil + direkter Nutzen),
        # weil Export und Maßnahmentabelle sie als Zahl lesen.
        **_benefit_euro_layer_fields(linked, annual_benefit_direct),
        # S157: gerechneter Anteil s_gek (ohne Eingabe Voreinstellung 0,11, Befund 138)
        # und Kennzeichnung als Abschätzung von KAP3.
        **_s157_summary_fields(mdef, measure.config),
        **_vg_kalib_summary_fields(mdef, measure.config),
        # Befund 129: S157 zusammen mit dem Hitzeaktionsplan gerechnet (Faktoren multipliziert)
        **({"s157_with_hap": bool(hap_by_cell)} if _is_s157(mdef) else {}),
        # Befunde 139, 148: Betrag der öffentlichen Kühlzentren getrennt von S157,
        # gekennzeichnet als Abschätzung von KAP3 (heat.delta_kuehlzentren).
        **_kz_summary_fields(mdef, kz_benefit_eur, s157_benefit_eur, bool(vg_fracs_by_cell)),
        # S158-Integrationsauflage Punkt 5: vermiedene Symptomtage/Euro der Kommune als
        # Abschätzung von KAP3 gekennzeichnet, oder Vermerk statt Betrag ohne Gruppenaufteilung.
        **_s158_summary_fields(mdef, s158_avoided_days_total, s158_avoided_days_eur,
                               s158_missing_split),
        # Integrationsauflage (Stadtbaumwahl) §5 Punkt (4): vermiedene Zusatztage/Euro
        # der Kommune als Abschätzung von KAP3 gekennzeichnet, mit Hinweis auf die
        # Richtung des Fehlers in λ (Modellgrenze 7), oder Vermerk statt Betrag ohne
        # anteil_ersetzt bzw. ohne Baumkronen in den abgedeckten Zellen.
        **_stadtbaum_summary_fields(mdef, stadtbaum_avoided_days_total,
                                    stadtbaum_avoided_days_eur, stadtbaum_missing_reason),
        # Kosten der Stadtbaumwahl (Ü-11): gewählter Fall, ohne Fall beide Beträge
        # nebeneinander (capex_je_fall) und Vermerk, ohne Stückzahl Vermerk statt Betrag.
        **stadtbaum_kosten_felder,
        # Befund 126: Schutzprogramme zusammen mit dem Hitzeaktionsplan (mit Kappung 0,794)
        **({"vg_with_hap": bool(hap_by_cell)} if _is_vg(mdef) else {}),
        "params_fingerprint": fingerprint,
        "count": count,
        "count_is_default": count_is_default,
        "recommended_count": recommended_count,
        "unit_label": mdef.get("unit_label"),
        "unit_factor": round(unit_factor, 4),
        "cost_breakdown": cost_breakdown,
    }

    # Persistiert am Maßnahmen-Objekt (bereits in der Session geladen) statt an
    # einer per Nachfrage-Query gesuchten MeasureImpact-Zelle - so unabhängig von
    # Flush-Reihenfolge/Autoflush-Konfiguration die einzige Quelle der Wahrheit
    # für Export/cost-summary, ohne dass diese neu rechnen müssen.
    measure.impact_summary = summary
    db.commit()

    return summary


def kommune_measures_query(db: Session, kommune_id: int, demo_session_id: str | None = None):
    """Maßnahmen einer Kommune, session-korrekt gefiltert.

    Produktpfad (``demo_session_id=None``): nur echte Maßnahmen
    (``demo_session_id IS NULL``) — Demo-Sitzungen verschmutzen nie Aggregate,
    Exporte oder Fingerprints. Demo-Pfad: nur die Maßnahmen DIESER Sitzung.
    """
    q = db.query(AdaptationMeasure).filter(AdaptationMeasure.kommune_id == kommune_id)
    if demo_session_id:
        return q.filter(AdaptationMeasure.demo_session_id == demo_session_id)
    return q.filter(AdaptationMeasure.demo_session_id.is_(None))


def _adjusted_cell_data(db: Session, kommune_id: int, apply_measures: bool,
                        demo_session_id: str | None = None) -> list[dict]:
    """Liefert Per-Zell-Daten (ggf. mit angewandten Maßnahmen) für Aggregation."""
    # Streaming (yield_per): nur die data-Blobs behalten, nicht zusätzlich
    # zehntausende ORM-Instanzen — halbiert grob den RAM-Peak der Aggregation.
    base: dict[int, dict] = {}
    for ca in db.query(CellAssessment).filter(
            CellAssessment.kommune_id == kommune_id).yield_per(500):
        base[ca.grid_cell_id] = ca.data or {}

    if not apply_measures:
        return [dict(d) for d in base.values()]

    # Maßnahmen-Faktoren je Zelle/Risiko (multiplikativ kombiniert). Fläche, Anzahl
    # und unit_factor werden pro Maßnahme genauso bestimmt wie in compute_impact,
    # damit Dashboard ("mit Maßnahmen") und Sidebar nicht divergieren.
    factors: dict[int, dict[str, float]] = {}
    measures = kommune_measures_query(db, kommune_id, demo_session_id).all()
    overrides = parameter_registry.overrides_map(
        parameter_registry.load_db_overrides(db, kommune_id)
    )
    # Befund 126: δ_HAP je Zelle vorab, damit die Schutzprogramme am Paketwert kappen
    # (max(δ_HAP × δ_VG; 0,794)); gedämpft wird hier nicht, das macht die Multiplikation.
    # Kühlzentren (S157-Maßnahme) kappen ebenso: max(δ_HAP × δ_VG × δ_KZ; kappung_vg).
    hap_cap: dict[int, float] = {}
    has_kz = any(catalog.MEASURES_BY_CODE.get(m.measure_type, {}).get("effect_model") == "s157"
                 for m in measures)
    vg_fracs_by_cell: dict[int, list[float]] = {}
    if has_kz:
        vg_fracs_by_cell = _vg_cell_fracs(db, [
            m for m in measures
            if catalog.MEASURES_BY_CODE.get(m.measure_type, {}).get("effect_model") == "vg"
            and not _vg_kalib_input(m.config)])   # Wächter: δ_VG = 1 (Befund 150)
    if has_kz or any(catalog.MEASURES_BY_CODE.get(m.measure_type, {}).get("effect_model") == "vg"
                     for m in measures):
        hap_base = catalog.MEASURES_BY_CODE.get(S157_HAP_CODE)
        if hap_base:
            hap_def = parameter_registry.resolve_measure_def(hap_base, overrides)
            for m in measures:
                if m.measure_type != S157_HAP_CODE:
                    continue
                frac_map, covered_area_m2 = _coverage(db, m)
                count, _, recommended = _resolve_count(hap_def, m.config, covered_area_m2)
                uf = _unit_effect_factor(count, recommended)
                for cid, frac in frac_map.items():
                    hap_cap[cid] = hap_cap.get(cid, 1.0) * _reduction_factor(hap_def, frac, uf)
    # Bericht §5 „Zusammen mit S158" (T-1602-cto): Ĝ′-Tage-Faktor je Zelle aus den
    # Stadtbaumwahl-Maßnahmen vorab, damit S158 seinen Nutzen aus den schon um die
    # Pflanzung geminderten Tagen rechnet (kein vermiedener Tag zählt doppelt) —
    # dieselbe Basis wie ``_stadtbaum_cell_factor`` selbst: die ungeänderten Roheingaben
    # in ``base`` (keine erneute DB-Abfrage nötig, anders als in compute_impact).
    stadtbaum_days_by_cell: dict[int, float] = {}
    if any(catalog.MEASURES_BY_CODE.get(m.measure_type, {}).get("effect_model") == "s158"
           for m in measures):
        for m in measures:
            if catalog.MEASURES_BY_CODE.get(m.measure_type, {}).get("effect_model") != "stadtbaum":
                continue
            frac_map, _ = _coverage(db, m)
            for cid, frac in frac_map.items():
                cell_risk = ((base.get(cid) or {}).get("risks", {}) or {}).get(
                    ALLERGY_RISK_CODE, {})
                factor = _stadtbaum_cell_factor(m.config, frac, cell_risk)
                stadtbaum_days_by_cell[cid] = stadtbaum_days_by_cell.get(cid, 1.0) * factor
    for m in measures:
        mbase = catalog.MEASURES_BY_CODE.get(m.measure_type)
        if not mbase:
            continue
        mdef = parameter_registry.resolve_measure_def(mbase, overrides)
        frac_map, covered_area_m2 = _coverage(db, m)
        count, _, recommended = _resolve_count(mdef, m.config, covered_area_m2)
        unit_factor = _unit_effect_factor(count, recommended)
        for cid, frac in frac_map.items():
            cell_factors = factors.setdefault(cid, {})
            cell_risks = (base.get(cid) or {}).get("risks", {})
            cell_inputs = (base.get(cid) or {}).get("inputs")
            for code in mdef.get("linked_risk_codes", []):
                cell_risk = _with_cell_q_pfl(cell_risks.get(code, {}), cell_inputs)
                vg_cap = 1.0
                if _is_s157(mdef) and code == S157_RISK_CODE:
                    # im Aggregat nur die Kappung, gedämpft wird über die Multiplikation
                    _, vg_cap = _vg_kz_factors(vg_fracs_by_cell.get(cid, []), cell_risk,
                                               hap_cap.get(cid, 1.0))
                factor = _measure_cell_factor(mdef, m.config, code, frac, unit_factor,
                                              cell_risk,
                                              hap_cap=hap_cap.get(cid, 1.0),
                                              s158_days_factor=stadtbaum_days_by_cell.get(cid, 1.0),
                                              vg_cap=vg_cap)
                cell_factors[code] = cell_factors.get(code, 1.0) * factor

    out = []
    for cid, data in base.items():
        cell_pop = float(data.get("inputs", {}).get("pop", 0.0) or 0.0)
        new_data = {"risks": {}, "inputs": {"pop": cell_pop}}
        # Expositions-Gate des Belastungs-P90 (risk_engine._cell_is_exposed) braucht
        # die Zell-Expositionen auch im With-Measures-Aggregat — Maßnahmen ändern
        # Indizes/Outcomes, nicht die Exposition selbst (Referenzkopie genügt).
        if "exposures" in data:
            new_data["exposures"] = data["exposures"]
        risks = data.get("risks", {})
        cell_factors = factors.get(cid, {})
        for code, r in risks.items():
            factor = cell_factors.get(code, 1.0)
            entry = {"index": float(r.get("index", 0.0)) * factor}
            # Der Maßnahmen-Faktor mindert den Screening-Index; die Schicht-B-Outcomes
            # hängen zwar an der Hazard-Intensität (nicht direkt am Index), werden hier
            # aber bewusst PROPORTIONAL zum Index-Faktor skaliert — die pragmatische
            # Brücke zwischen index-basierter Maßnahmenwirkung und der Kostenschicht
            # (bewusste Vereinfachung, keine „lineare Legacy-Rechnung"). aggregate()
            # summiert die Zell-Werte und leitet die Kosten live aus dem Outcome ab.
            if "outcome" in r:
                entry["outcome"] = float(r["outcome"]) * factor
            if "cost_eur" in r:
                entry["cost_eur"] = float(r["cost_eur"]) * factor
            new_data["risks"][code] = entry
        # Folgekosten (indirekt/Restaurierung) aus den NEUEN direkten Sektorschäden neu
        # bilden, sonst bliebe indirekt = k·Σ direkt VOR den Maßnahmen stehen (§8/B3).
        _reconsolidate_cell_folgekosten(new_data["risks"])
        out.append(new_data)
    return out


def _compute_risk_aggregate(db: Session, kommune_id: int, apply_measures: bool,
                            demo_session_id: str | None = None) -> dict:
    """Rechnet das Aggregat aus der DB (ohne Cache) — die eigentliche Arbeit."""
    kommune = db.query(Kommune).filter_by(id=kommune_id).first()
    total_pop = float(kommune.population or 0) if kommune else 0.0
    area_km2 = float(kommune.area_km2 or 0) if kommune else 0.0
    overrides = parameter_registry.overrides_map(
        parameter_registry.load_db_overrides(db, kommune_id))
    with override_context.override_scope(overrides):
        cell_data = _adjusted_cell_data(db, kommune_id, apply_measures, demo_session_id)
        return risk_engine.aggregate(cell_data, total_pop, area_km2)


def get_risk_aggregate(db: Session, kommune_id: int, apply_measures: bool = False,
                       demo_session_id: str | None = None) -> dict:
    """Aggregiertes Risiko (mit/ohne Maßnahmen) inkl. Kosten — mit Datei-Cache.

    Das Aggregat lädt alle CellAssessment-Zeilen und aggregiert darüber; pro
    Dashboard-Load geschieht das mehrfach mit identischen Eingaben. Der
    ``aggregate_cache`` materialisiert das Ergebnis je ``(kommune_id,
    apply_measures)`` und wird an allen Mutationspunkten explizit invalidiert.

    Die Kommune-Overrides werden für die Dauer der Aggregation als aktiver Engine-Scope
    gesetzt (``override_scope``) — sonst läsen Kostensatz-/Legacy-Fallback-Pfade die
    Overrides der zuletzt gerechneten Kommune (Cross-Kommune-Leak, §8/B2). So wirken
    Kostensatz-Overrides zudem live auf die Aggregatsumme (``aggregate`` monetarisiert
    aus dem gespeicherten Outcome).

    Demo-Sessions (``demo_session_id``) umgehen den geteilten Cache vollständig:
    ihre Maßnahmen sind sitzungsprivat, ein gemeinsames Artefakt würde fremde
    Sitzungen (oder das Produkt) verunreinigen. Die Basis-Variante (ohne
    Maßnahmen) ist für Demo und Produkt identisch und darf den Cache nutzen.
    """
    if demo_session_id and apply_measures:
        return _compute_risk_aggregate(db, kommune_id, apply_measures, demo_session_id)
    cached = aggregate_cache.load(kommune_id, apply_measures)
    if cached is not None:
        return cached
    result = _compute_risk_aggregate(db, kommune_id, apply_measures)
    aggregate_cache.store(kommune_id, apply_measures, result)
    return result


def build_cost_summary(db: Session, kommune_id: int, demo_session_id: str | None = None) -> dict:
    """Kostenübersicht: Schäden (mit/ohne Maßnahmen) + Maßnahmen-CAPEX/OPEX/Nutzen.

    ``damage_reduction_eur`` (Aggregat-Differenz ohne/mit Maßnahmen, inkl. flat-Risiken
    und rekonsolidierter Folgekosten) ist die belastbare Kennzahl „vermiedene Schäden";
    ``total_benefit_direct_eur`` (benefit_per_m2_year · Fläche) ist echter Zusatznutzen
    (Erträge/Erlöse) und dazu additiv. Die Pro-Maßnahmen-Schadens-/flat-Nutzen sind
    Diagnostik — weicht ihre Summe grob von der Aggregat-Differenz ab, meldet
    ``benefit_consistency_warning`` das, statt es zu verstecken.

    Wird von ``dashboard_cache`` als Datei vorgebaut; der Endpoint liefert nur
    noch die gzip-Datei aus.
    """
    base = get_risk_aggregate(db, kommune_id, apply_measures=False)
    withm = get_risk_aggregate(db, kommune_id, apply_measures=True,
                               demo_session_id=demo_session_id)

    measures = kommune_measures_query(db, kommune_id, demo_session_id).all()
    total_capex = total_opex = total_benefit = 0.0
    total_ben_damage = total_ben_flat = total_ben_direct = 0.0
    measure_rows = []
    for m in measures:
        summary = ensure_fresh_impact_summary(db, m)
        capex = summary.get("capex_eur", 0.0)
        opex = summary.get("opex_annual_eur", 0.0)
        ben = summary.get("annual_benefit_eur", 0.0)
        ben_damage = summary.get("annual_benefit_damage_eur", 0.0) or 0.0
        ben_flat = summary.get("annual_benefit_flat_eur", 0.0) or 0.0
        ben_direct = summary.get("annual_benefit_direct_eur", 0.0) or 0.0
        total_capex += capex
        total_opex += opex
        total_benefit += ben
        total_ben_damage += ben_damage
        total_ben_flat += ben_flat
        total_ben_direct += ben_direct
        measure_rows.append({"id": m.id, "name": m.name, "measure_type": m.measure_type,
                             "capex_eur": round(capex, 2), "opex_annual_eur": round(opex, 2),
                             "annual_benefit_eur": round(ben, 2),
                             "annual_benefit_damage_eur": round(ben_damage, 2),
                             "annual_benefit_flat_eur": round(ben_flat, 2),
                             "annual_benefit_direct_eur": round(ben_direct, 2),
                             "benefit_capped": bool(summary.get("benefit_capped", False)),
                             # Verwechslungssperre (T-0838); ältere Summaries ohne die
                             # Felder gelten als Klasse A (bisheriger Bestand).
                             "benefit_has_euro_layer": bool(
                                 summary.get("benefit_has_euro_layer", True)),
                             "benefit_display": summary.get("benefit_display"),
                             "benefit_note": summary.get("benefit_note")})

    damages_base = base["cost"]["total_eur"]
    damages_with = withm["cost"]["total_eur"]
    damage_reduction = round(damages_base - damages_with, 2)
    per_measure_damage_ben = total_ben_damage + total_ben_flat
    consistency_warning = (
        abs(per_measure_damage_ben - damage_reduction)
        / max(abs(damage_reduction), 1.0) > 0.25
        if (per_measure_damage_ben or damage_reduction) else False
    )
    # Untergrenzen-Kennzeichnung (UBA MK 4.0, Anforderung 25): dieselben Kategorien
    # wie in der Basissumme — fehlt dort ein belegter Kostensatz, sind auch die
    # Schadenssummen dieser Übersicht konservative Untergrenzen.
    lb = base["cost"].get("lower_bound")

    out = {
        "damages_base_eur": damages_base,
        "damages_with_measures_eur": damages_with,
        "damage_reduction_eur": damage_reduction,
        "by_risk": withm["cost"]["by_risk"],
        # Aus einem Aggregat, das vor T-1470-cto im aggregate_cache abgelegt wurde
        # (der Cache leert sich nur bei einer Änderung von catalog.MODEL_VERSION,
        # nicht bei dieser Änderung), fehlt "klimawirkungen" noch — dann hier aus
        # by_risk nachbauen statt mit KeyError abzubrechen.
        "klimawirkungen": withm["cost"].get("klimawirkungen")
        or klimawirkungen(withm["cost"]["by_risk"]),
        "measures": {
            "total_capex_eur": round(total_capex, 2),
            "total_opex_annual_eur": round(total_opex, 2),
            "total_annual_benefit_eur": round(total_benefit, 2),
            "total_benefit_damage_eur": round(total_ben_damage, 2),
            "total_benefit_flat_eur": round(total_ben_flat, 2),
            "total_benefit_direct_eur": round(total_ben_direct, 2),
            "benefit_consistency_warning": consistency_warning,
            "rows": measure_rows,
        },
    }
    if lb is not None:
        out["lower_bound"] = lb
    return out

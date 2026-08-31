"""Gesundheits-Schadensfunktionen (Schicht B, Stufe 4 — MODELL_KRITIK §6.1).

Zwei verschiedene Bauarten, weil die Gefahren verschieden funktionieren:

**Hitze — chronisch und flächig.** Die Mortalität folgt der publizierten
Expositions-Wirkungs-Kurve des RKI (Winklmayr u. a. 2022): relatives Sterberisiko
über der **Wochenmitteltemperatur**, geschichtet nach vier Altersbändern und drei
Regionen mit eigenen Wirkschwellen (19,7/20,2/20,8 °C). Entscheidend ist, dass die
Kurve **über die Verteilung** der Sommerwochen integriert wird und nicht am
Mittelwert ausgewertet: Das deutsche Sommermittel liegt bei rund 18,5 °C und damit
*unter* der Wirkschwelle — am Mittelwert ausgewertet käme fast überall null heraus.
Die Todesfälle entstehen in den wenigen heißen Wochen.

Stand: **Methodik-Bericht #95 Rev. 8** (docs/methodik/95_hitzebelastung.md;
Rev. 7 abgenommen + integriert, Rev. 8 = Fortschreibung: L̄_85+ exakt 4,16,
Ressourcen-Regel, Datenebenen-Spezifikation). Kernpunkte: empirische
intra-saisonale Wochenquantile je Region statt Gauß-Annahme (§3.2); native
Ergebnisgröße **YLL** (verlorene Lebensjahre) mit Todesfällen als Teil-Ausweis
(§3.3/§3.5); mittelwertzentrierte, bandweise v_vers-Modifikatoren (β_iso 65+,
β_pfl 85+; nur D-Pfad); ein nationaler Kalibrierskalar c_kal = 0,581 auf
bevölkerungsgewichteter Kalibrierbasis (§4); Morbidität als altersgeschichtete
Baseline × HD-Term (§3.4).

**Flut und Sturm — selten, geclustert, tail-lastig.** Zu wenige Ereignisse für eine
gefittete Kurve; Struktur daher ``Exposition × bedingte Letalität``, wobei die
Letalität aus der Loss-of-Life-Literatur kommt und nur ein Skalierungsfaktor
kalibriert wird. Der wichtigste Unterscheider bei Flut ist das **Regime**
(Sturzflut vs. langsamer Anstieg) — Ahr 2021 (>180 Tote) gegen Elbe 2002 (~21) bei
weit größerer überfluteter Fläche.

Alle Raten/Koeffizienten sind editierbare Registry-Parameter
(``impact/params.py``); nationale Kalibrier- und Validierungsanker stehen in
``app/data/germany_health_reference.py``.

Registrierung am Modulende: die Funktionen werden in ``impact.IMPACT_FUNCTIONS``
eingetragen; ``compute_all_cell_impacts`` verteilt darauf, sonst auf
``legacy_cell_impact``.
"""

from __future__ import annotations

from math import exp

from app.services.engine import risk_engine
from app.services.engine.impact.base import CellContext, attributable_fraction


def _result(risk: dict, outcome: float) -> dict:
    outcome = max(0.0, outcome)
    return {"outcome": outcome, "cost_eur": risk_engine.cost_from_outcome(risk, outcome)}


def _heat_af(ctx: CellContext, code: str, beta_default: float, thr_default: float) -> float:
    """Attributable Fraktion aus den Zell-Hitzetagen (HEAT_WAVE absolut)."""
    hd = ctx.haz("HEAT_WAVE")
    beta = ctx.p(code, "beta_per_hotday", beta_default)
    thr = ctx.p(code, "hotday_threshold", thr_default)
    return attributable_fraction(hd, beta, thr)


# ── Expositions-Wirkungs-Kurve Hitze (RKI / Winklmayr u. a. 2022) ─────────────

# Regionszuschnitt exakt wie in Winklmayr u. a. 2022.
REGION_BY_BUNDESLAND: dict[str, str] = {
    "Bremen": "nord", "Hamburg": "nord", "Mecklenburg-Vorpommern": "nord",
    "Niedersachsen": "nord", "Schleswig-Holstein": "nord",
    "Berlin": "mitte", "Brandenburg": "mitte", "Nordrhein-Westfalen": "mitte",
    "Rheinland-Pfalz": "mitte", "Saarland": "mitte", "Hessen": "mitte",
    "Sachsen": "mitte", "Sachsen-Anhalt": "mitte", "Thüringen": "mitte",
    "Baden-Württemberg": "sued", "Bayern": "sued",
}

# Wirkschwellen der Wochenmitteltemperatur je Region (°C), Winklmayr Abb. 3.
REGION_THRESHOLD: dict[str, float] = {"nord": 19.7, "mitte": 20.2, "sued": 20.8}

# Steigung der Kurve für das Band 85+ je Region (1/K). Nord/Mitte: Ablesekette aus
# den publizierten Kurven 2012–2021 (RR ≈ 1,4/1,35 bei 25 °C über der Schwelle).
# Süd: Ablesewert 0,0531 × Nachschätzungs-Skalar 1,65 aus dem Rev.-7-Holdout-Fit
# (Bericht #95 §4, Anker #beta-sued) — modellinterner Kompensationsparameter.
REGION_BETA_85P: dict[str, float] = {"nord": 0.0634, "mitte": 0.0625, "sued": 0.0876}

# Steigung der übrigen Altersbänder relativ zu 85+. NICHT frei gewählt, sondern
# aus der publizierten Altersverteilung der hitzebedingten Sterbefälle
# zurückgerechnet: Für kleine β·Δ gilt Todesfälle_a ∝ pop_a · m_a · β_a, also
# β_a ∝ Anteil_a / (pop_a · m_a). Mit den RKI-Anteilen 2026 (6,5/12,9/25,2/55,5 %)
# und den Sterbefällen 2023 je Band (Bericht #95 §3.3a, Golden-Test
# beispiel_95_fa_rueckrechnung).
AGE_BETA_FACTOR: dict[str, float] = {
    "u65": 0.357, "a65_74": 0.588, "a75_84": 0.631, "a85p": 1.0,
}

AGE_BANDS: tuple[str, ...] = ("u65", "a65_74", "a75_84", "a85p")

# Restlebenserwartung je Band (Jahre je Sterbefall) — YLL-Bewertung nach
# UBA MK 4.0 (Bericht #95 §3.5, Anker #l-a; Sterbetafeln 2022/2024; 85+ exakt
# sterbefallgewichtet, Rev. 8 — Skript l85_sterbefallgewichtung.py).
AGE_LIFE_YEARS: dict[str, float] = {
    "u65": 23.39, "a65_74": 15.59, "a75_84": 8.90, "a85p": 4.16,
}

# ── #96 Aeroallergene (Methodik-Bericht Rev. 1) ───────────────────────────────
# Altersbänder der AR-Prävalenz: u20 und 20–64 kommen aus der Zensus-
# Binnenaufteilung der u65-Menge (zensus_loader), 65+ wie bei #95.
POLLEN_AGE_BANDS: tuple[str, ...] = ("u20", "a20_64", "a65_74", "a75_84", "a85p")

# 12-Monats-Prävalenz allergische Rhinitis je Band (DEGS1/KiGGS, §3.2).
POLLEN_PREVALENCE: dict[str, float] = {
    "u20": 0.088, "a20_64": 0.132, "a65_74": 0.067, "a75_84": 0.050, "a85p": 0.050,
}

# Saisonlängen nach EAACI-Kriterium (Tage; §3.5, gekennzeichnete Abschätzung).
POLLEN_SAISON_LAENGE: dict[str, float] = {"birke": 30.0, "graeser": 60.0}

# d_Saison der DEFAULT-Parameter: 0,70 · (0,55·30 + 0,75·60) = 43,05 Tage.
# Bezugswert der Kostensatz-Kopplung: Der Katalog-Kostensatz c_Tag (Default
# 6,20 €₂₀₂₄) gilt für GENAU diese Kette. Der Jahres-Anker des Berichts folgt
# implizit: c_Jahr,direkt = c_Tag · d_Saison_ref = 6,20 · 43,05 = 266,91 €₂₀₂₄
# gegenüber 266,90 € im Bericht (§3.5) — die Differenz von 1 Cent stammt
# ausschließlich daraus, dass der Produkt-Kostensatz auf Cent gerundet ist
# (+3,7·10⁻⁵ relativ, testgebunden). Editiert ein Nutzer den Kostensatz, ist
# das gleichbedeutend mit einem anderen c_Jahr,direkt — die Kette bleibt
# konsistent (Ledger #96 Befund 137).
POLLEN_D_SAISON_REF: float = 43.05

# Gemessene Saison-Spreizung je Region (Tage; DWD-Phänologie, §3.1).
POLLEN_DELTA_S_BIRKE: dict[str, float] = {"nord": 3.96, "mitte": 4.20, "sued": 5.94}
POLLEN_DELTA_S_GRAESER: dict[str, float] = {"nord": 4.78, "mitte": 4.08, "sued": 3.70}

# Baseline-Einweisungsraten je Band (Fälle/100.000·Jahr) — Morbiditätspfad
# (Bericht #95 §3.4, Anker #r0-a; bevölkerungsgewichtete Summe 3,54).
AGE_MORBIDITY_R0: dict[str, float] = {
    "u65": 1.9, "a65_74": 6.3, "a75_84": 10.8, "a85p": 15.6,
}


def region_for(bundesland: str | None) -> str:
    return REGION_BY_BUNDESLAND.get(bundesland or "", "mitte")


# ── Wochenverteilung: empirische intra-saisonale Anomalie-Quantile (Rev. 7) ──
# Gemessen aus 7 DWD-Stationen je Region × 30 Sommer (1991–2020), Quantile an
# p_w = (w−0,5)/13 (Bericht #95 §3.2; Skript dwd_wochenquantile.py). Die
# Konstanten sind die Berichtstabelle; liegt die gepinnte Anlage
# ``wochenquantile_region.csv`` vor, werden deren (feiner aufgelöste) Werte
# geladen — Kalibriermodell = Produktionsmodell (§3.4).
_WEEK_ANOMALIES_REPORT: dict[str, tuple[float, ...]] = {
    "nord": (-4.17, -2.81, -2.00, -1.45, -0.99, -0.50, 0.00,
             0.42, 0.89, 1.54, 2.10, 2.83, 4.22),
    "mitte": (-4.59, -3.04, -2.27, -1.64, -1.12, -0.57, -0.04,
              0.51, 1.05, 1.65, 2.32, 3.16, 4.60),
    "sued": (-4.67, -2.99, -2.23, -1.65, -1.11, -0.57, -0.03,
             0.51, 1.12, 1.75, 2.36, 3.18, 4.46),
}


def _load_week_anomalies() -> dict[str, tuple[float, ...]]:
    import csv
    import os

    path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                        "data", "kalibrierung", "wochenquantile_region.csv")
    try:
        rows: dict[str, dict[int, float]] = {}
        with open(os.path.abspath(path), newline="") as fh:
            for row in csv.DictReader(fh):
                rows.setdefault(row["region"], {})[int(row["w"])] = float(row["q_w_emp"])
        loaded = {r: tuple(v[w] for w in sorted(v)) for r, v in rows.items()}
        if all(len(loaded.get(r, ())) == 13 for r in _WEEK_ANOMALIES_REPORT):
            return loaded
    except OSError:
        pass
    return _WEEK_ANOMALIES_REPORT


REGION_WEEK_ANOMALIES: dict[str, tuple[float, ...]] = _load_week_anomalies()


def weekly_temperatures(mean_temp: float, region: str) -> list[float]:
    """Wochenmitteltemperaturen der 13 Sommerwochen: T_w = T̄ + q_w,Region.

    Deterministisch und reproduzierbar (keine Simulation); die oberen Quantile
    bilden genau die heißen Wochen ab, aus denen die Sterbefälle stammen.
    """
    return [mean_temp + q for q in
            REGION_WEEK_ANOMALIES.get(region, REGION_WEEK_ANOMALIES["mitte"])]


def heat_excess_weeks(mean_temp: float, region: str, threshold: float) -> float:
    """Übertemperatur-Wochen (K·Wochen) über der Wirkschwelle."""
    return sum(max(0.0, t - threshold) for t in weekly_temperatures(mean_temp, region))


def cell_summer_temp(ctx: CellContext) -> float:
    """Sommermitteltemperatur der Zelle (°C) mit dokumentierten Rückfällen."""
    t = ctx.ci.get("summer_temp_cell")
    if t is not None:
        return float(t)
    t = ctx.regional.get("summer_temp_mean")
    if t is not None:
        # Ohne zellscharfes Raster wenigstens den Wärmeinsel-Zuschlag ansetzen.
        return float(t) + float(ctx.ci.get("uhi_delta_mean") or 0.0)
    from app.services.engine.inputs import SUMMER_MAX_TO_MEAN_OFFSET_K
    return float(ctx.regional.get("summer_temp", 24.0)) - SUMMER_MAX_TO_MEAN_OFFSET_K


def _age_bands(ctx: CellContext) -> dict[str, float]:
    """Bevölkerung je Altersband; Rückfall über den 65+-Anteil der Zelle."""
    bands = ctx.ci.get("pop_age_bands")
    if isinstance(bands, dict) and bands:
        return {b: float(bands.get(b) or 0.0) for b in AGE_BANDS}
    from app.services.zensus_loader import NATIONAL_SENIOR_SPLIT
    pop = ctx.pop
    share_o = ctx.ci.get("share_over_65")
    if share_o is None:
        share_o = ctx.regional.get("demographics", {}).get("share_over_65", 22.0)
    pop_65p = pop * float(share_o) / 100.0
    return {
        "u65": max(0.0, pop - pop_65p),
        **{b: pop_65p * f for b, f in NATIONAL_SENIOR_SPLIT.items()},
    }


# ── 1. Hitzemortalität (Bericht #95 §3.3/§3.5 — nativer Ausweis YLL) ──────────

def _v_vers(ctx: CellContext, code: str, band: str) -> float:
    """Bandweiser Versorgungs-/Isolations-Modifikator v_vers,a (§3.3, nur D-Pfad).

    ``v = [1 + 1_{a≥65}·β_iso·(q_1P − q̄_1P)] · [1 + 1_{85+}·β_pfl·(q_pfl − q̄_pfl)]``

    Mittelwertzentriert (Bundesmittel ⇒ Faktor 1, kalibrierneutral). Zellgrößen
    (Bericht §3.6, Rev. 8): ``share_care_home_85p`` liefert die Ebene
    CARE_HOME_SHARE_85P (OSM-Pflegeeinrichtungen, kommunen-erwartungstreu auf q̄
    normiert — ``inputs.apply_care_home_share``); ``share_single_65p`` ist als
    Ebene GEPARKT (keine offene Zellquelle, Watchlist). Fehlt der ci-Wert
    (q_1P immer; q_pfl in Kommunen ohne OSM-Heim), rechnet die Zelle mit dem
    Bundesmittel (Faktor exakt 1).
    """
    v = 1.0
    if band != "u65":
        b_iso = ctx.p(code, "beta_iso", 0.90)
        qbar = ctx.p(code, "qbar_1p", 0.346)
        q = ctx.ci.get("share_single_65p")
        v *= 1.0 + b_iso * ((float(q) if q is not None else qbar) - qbar)
    if band == "a85p":
        b_pfl = ctx.p(code, "beta_pfl", 1.54)
        qbar = ctx.p(code, "qbar_pfl", 0.149)
        q = ctx.ci.get("share_care_home_85p")
        v *= 1.0 + b_pfl * ((float(q) if q is not None else qbar) - qbar)
    return max(0.0, v)


def mortality(risk: dict, ctx: CellContext) -> dict:
    """Verlorene Lebensjahre (YLL) je Zelle und Jahr; Todesfälle als Teil-Ausweis.

    ``D_a = c_kal · v_vers,a · pop_a · m_a/100k · (1/52) · Σ_w (e^{β_a(T_w−T_0)⁺} − 1)``
    ``YLL = Σ_a D_a · L̄_a`` — Bewertung €: YLL × VOLY (Kostensatz des Risikos).
    """
    from app.data.germany_health_reference import BASELINE_MORTALITY_PER_100K

    code = risk["code"]
    region = region_for(ctx.regional.get("bundesland"))

    thr = ctx.p(code, f"threshold_{region}", REGION_THRESHOLD[region])
    beta85 = ctx.p(code, f"beta_85p_{region}", REGION_BETA_85P[region])
    # ACHTUNG: Defaults müssen mit den Registry-Specs in impact/params.py
    # übereinstimmen — die Registry verdrahtet sie NICHT automatisch hierher.
    calib = ctx.p(code, "calibration", 0.581)
    # Distanz-Effekt: Sensitivitätsband, Basiswert 0 (Bericht #95, Log 20);
    # wirkt nur, wenn ein Nutzer ihn setzt UND die Zelle eine KH-Distanz trägt.
    beta_d = ctx.p(code, "beta_dist_km", 0.0)
    dist_km = float(ctx.ci.get("hospital_distance_km") or 0.0)

    temps = weekly_temperatures(cell_summer_temp(ctx), region)
    bands = _age_bands(ctx)

    deaths = 0.0
    yll = 0.0
    for band in AGE_BANDS:
        pop_a = bands.get(band, 0.0)
        if pop_a <= 0.0:
            continue
        m_a = ctx.p(code, f"baseline_mort_{band}", BASELINE_MORTALITY_PER_100K[band])
        beta_a = beta85 * ctx.p(code, f"beta_factor_{band}", AGE_BETA_FACTOR[band])
        excess = sum(exp(beta_a * max(0.0, t - thr)) - 1.0 for t in temps)
        d_a = (calib * _v_vers(ctx, code, band) * pop_a
               * (m_a / 100_000.0) * (1.0 / 52.0) * excess)
        deaths += d_a
        yll += d_a * ctx.p(code, f"life_years_{band}", AGE_LIFE_YEARS[band])

    if beta_d > 0.0 and dist_km > 0.0:
        factor = 1.0 + beta_d * dist_km
        deaths *= factor
        yll *= factor

    out = _result(risk, yll)
    out["deaths"] = max(0.0, deaths)
    return out


# ── 2. Hitzemorbidität (Bericht #95 §3.4 — Einweisungen) ──────────────────────

def morbidity(risk: dict, ctx: CellContext) -> dict:
    """Hitzeassoziierte Erkrankungsfälle je Zelle und Jahr.

    ``F = Σ_a pop_a · r_0,a/100k · max(0, 1 + e_HD·(HD − HD_ref))``

    HD-Term zweiseitig linear, bei 0 gedeckelt (Befund 59): Zellen unter der
    Referenzlast reduzieren die Baseline anteilig — bevölkerungsgewichtet
    erwartungstreu um die Referenz, keine Doppelzählung des in r_0 enthaltenen
    Durchschnittseffekts. Keine Modifikatoren im F-Pfad (Gegen-/fehlende
    Evidenz; Bericht §3.4). Dokumentierte Grenze: der nicht-wetterliche
    Baseline-Sockel ist bevölkerungsproportional (§3.1-Lackmustest gilt für die
    Mortalität).
    """
    code = risk["code"]
    hd = ctx.haz("HEAT_WAVE")
    e_hd = ctx.p(code, "excess_per_hotday", 0.024)
    hd_ref = ctx.p(code, "hotday_ref_days", 7.2)
    factor = max(0.0, 1.0 + e_hd * (hd - hd_ref))

    bands = _age_bands(ctx)
    outcome = sum(
        bands.get(band, 0.0) * (ctx.p(code, f"r0_{band}", AGE_MORBIDITY_R0[band])
                                / 100_000.0) * factor
        for band in AGE_BANDS
    )
    return _result(risk, outcome)


# ── 2b. Aeroallergene: klimaattribuierte Symptomtage (#96) ────────────────────

def pollen_age_bands(ci: dict) -> dict[str, float]:
    """Bevölkerung je #96-Band aus den Zell-Eingaben (mit dokumentiertem Rückfall).

    Wird von der Schadensfunktion UND von der kommunalen Referenzbildung
    (``inputs.kommunale_pollen_referenz``) genutzt — beide müssen dieselben
    Gewichte sehen, sonst ist die Zentrierung Σ B·P̂ = Σ B nicht exakt
    (Ledger #96 Befund 126).
    """
    from app.services.zensus_loader import NATIONAL_U20_SHARE_OF_U65

    bands = ci.get("pop_age_bands")
    if isinstance(bands, dict) and bands.get("u20") is not None:
        return {b: float(bands.get(b) or 0.0) for b in POLLEN_AGE_BANDS}
    # Alt-Zellen ohne u20-Aufteilung: u65 mit dem amtlichen Bundesanteil in
    # u20/20–64 trennen (Fallback wie bei den Senioren-Bändern).
    u65 = float((bands or {}).get("u65") or 0.0)
    if not u65:
        pop = float(ci.get("pop") or 0.0)
        share_o = ci.get("share_over_65")
        u65 = max(0.0, pop - pop * float(share_o or 0.0) / 100.0)
    return {
        "u20": u65 * NATIONAL_U20_SHARE_OF_U65,
        "a20_64": u65 * (1.0 - NATIONAL_U20_SHARE_OF_U65),
        "a65_74": float((bands or {}).get("a65_74") or 0.0),
        "a75_84": float((bands or {}).get("a75_84") or 0.0),
        "a85p": float((bands or {}).get("a85p") or 0.0),
    }


def _pollen_age_bands(ctx: CellContext) -> dict[str, float]:
    """Bänder aus dem CellContext (Wrapper um ``pollen_age_bands``)."""
    return pollen_age_bands(ctx.ci)


def allergy_symptom_days(risk: dict, ctx: CellContext) -> dict:
    """Zusätzliche Symptomtage durch die klimabedingt längere Pollensaison.

    ``B_z    = Σ_a pop_a · p_AR,a``                                    (§3.2)
    ``δ_R    = f · (p_B·ΔS_B,R + p_G·ΔS_G,R) · a_attr``                (§3.3)
    ``P̂_z    = 1 + λ · (Ĝ_z/Ḡ − 1)``   (mittelwertzentriert, §3.3)
    ``ΔTage_z = B_z · δ_R · P̂_z``      (nativ; € = ΔTage × c_Tag)

    P̂ steht in BEIDEN Pfaden — nativer Ausweis und €-Wert bleiben strikt
    proportional (Rev.-5-Befund 12). Der Kostensatz c_Tag = c_Jahr/d_Saison
    hängt am Registry-Kostensatz des Risikos (Herleitung dort; Golden-Test
    beispiel_96_kostenkette).
    """
    code = risk["code"]
    region = region_for(ctx.regional.get("bundesland"))

    bands = _pollen_age_bands(ctx)
    betroffene = sum(
        pop * ctx.p(code, f"p_ar_{band}", POLLEN_PREVALENCE[band])
        for band, pop in bands.items()
    )

    f = ctx.p(code, "f_symptomtage", 0.70)
    p_b = ctx.p(code, "p_sens_birke", 0.55)
    p_g = ctx.p(code, "p_sens_graeser", 0.75)
    a_attr = ctx.p(code, "a_attr", 0.50)
    ds_b = ctx.p(code, f"delta_s_birke_{region}", POLLEN_DELTA_S_BIRKE[region])
    ds_g = ctx.p(code, f"delta_s_graeser_{region}", POLLEN_DELTA_S_GRAESER[region])
    delta = f * (p_b * ds_b + p_g * ds_g) * a_attr

    # Vegetations-Modulation, zentriert auf die REFERENZ DER EIGENEN KOMMUNE
    # (Aufgabe §3.2 „geschlossene Betrachtungsebene", Bericht #96 §3.3): Ḡ ist das
    # betroffenengewichtete Mittel von Ĝ über die Zellen dieser Kommune —
    # dadurch ist Σ_z B_z·P̂_z = Σ_z B_z exakt und das Ergebnis hängt an keiner
    # Größe außerhalb der Kommune. Liegt keine Referenz vor (Zelle ohne
    # Kommunen-Kontext, Alt-Daten), bleibt P̂ NEUTRAL — kein Ersatz-Bundeswert.
    lam = ctx.p(code, "lambda_veg", 0.70)
    g_bar = ctx.regional.get("pollen_g_bar")
    g_cell = ctx.haz("POLLEN_LOAD")
    p_hat = 1.0
    if g_bar:
        p_hat = max(0.0, 1.0 + lam * (g_cell / float(g_bar) - 1.0))

    tage = betroffene * delta * p_hat
    out = _result(risk, tage)

    # Kostensatz-Kopplung (Bericht #96 §3.5, Ledger-Befund 133): Der Ausweis
    # rechnet € = ΔTage · c_Tag mit c_Tag = c_Jahr,direkt / d_Saison und
    # d_Saison = f·(p_B·L_B + p_G·L_G). Der Katalog-Kostensatz IST c_Tag im
    # Default (6,20 €₂₀₂₄ = 266,90/43,05) und bleibt editierbar; ändert der
    # Nutzer aber f, p_B, p_G oder eine Saisonlänge, muss c_Tag mitlaufen —
    # sonst bräche die im Bericht tragende f-Kürzung (f steht in ΔTage UND in
    # d_Saison und kürzt sich im €-Pfad vollständig heraus).
    l_b = ctx.p(code, "l_saison_birke", POLLEN_SAISON_LAENGE["birke"])
    l_g = ctx.p(code, "l_saison_graeser", POLLEN_SAISON_LAENGE["graeser"])
    d_saison = f * (p_b * l_b + p_g * l_g)
    if d_saison > 0.0:
        out["cost_eur"] *= POLLEN_D_SAISON_REF / d_saison
    out["betroffene"] = max(0.0, betroffene)
    return out


# ── 2c. UV-Schädigungen (Bericht #98 §3.2–3.4 — nativer Ausweis YLL) ─────────

# Roh-Neuerkrankungsraten je 100.000 und Jahr, Bänder wie #96 §3.2 (Bericht §3.3,
# Ablesekette aus KID 2025 Abb. 3.13.2/3.14.3, Anlage kid2025_ablesewerte.csv).
# Defaults MÜSSEN mit den Registry-Specs in impact/params.py übereinstimmen —
# die Registry verdrahtet sie nicht automatisch hierher.
UV_INCIDENCE_MM = {"u20": 0.5, "a20_64": 24.7, "a65_74": 64.0,
                   "a75_84": 94.9, "a85p": 88.5}
UV_INCIDENCE_C44 = {"u20": 2.0, "a20_64": 125.9, "a65_74": 617.6,
                    "a75_84": 1267.2, "a85p": 1479.5}


def uv_delta_dosis(ctx: CellContext, code: str) -> float:
    """Relative klimaattribuierte UV-Dosisänderung der Zelle (Bericht §3.2).

    ``ΔDosis = (SSD_1991–2020 − SSD_1961–1990)/SSD_1961–1990 · k_UV · a_attr · v_verh``

    Die beiden Normalperioden-Mittel stehen als Zellgrößen ``ssd_ref``/``ssd_neu``
    bereit (Ebene UV_RADIATION, ``inputs.apply_ssd_normalperioden``). Fehlen sie,
    rechnet die Zelle mit dem Bundesland-Gebietsmittel — die im Bericht §3.6
    dokumentierte Fallback-Kette, kein stiller Null-Wert.
    """
    ref = ctx.ci.get("ssd_ref")
    neu = ctx.ci.get("ssd_neu")
    if ref is None or neu is None or float(ref) <= 0.0:
        from app.services.climate import ssd_normalperioden
        ref, neu = ssd_normalperioden.ssd_for_bundesland(
            ctx.regional.get("bundesland"))
    d_ssd = (float(neu) - float(ref)) / float(ref)
    # v_verh ist Sensitivitätsband (Default 1, Bericht §3.4): der
    # Tages-Multiplikator der persönlichen Dosis an Komforttagen. Er steht
    # bewusst NICHT im Basiswert — die Jahreswirkung hängt am Komforttag-Anteil,
    # der in M0 keine Zellgröße ist.
    return (d_ssd * ctx.p(code, "k_uv", 0.84) * ctx.p(code, "a_attr", 0.75)
            * ctx.p(code, "v_verh", 1.0))


def _uv_r_out(ctx: CellContext, code: str) -> float:
    """Außenberufs-Modifikator auf den SCC-Anteil am C44-Zusatz (Bericht §3.4).

    ``w^Z = w_SCC·2,5/BAF_C44``, ``r_out = (1−w^Z) + w^Z·[1+q(OR−1)]/[1+q̄(OR−1)]``

    Mittelwertzentriert (Bundesmittel ⇒ 1). Die Ebene „Außenbeschäftigten-Anteil"
    ist **geparkt** (Bericht §3.6/§3.8: INKAR/SVB liefern keine keyless
    Zellgröße; Beschaffungs-Watchlist) — deshalb ist der Schalter
    ``r_out_enabled`` im Basiswert 0 und der Modifikator exakt neutral. Er wird
    erst wirksam, wenn die Ebene angebunden ist UND der Schalter gesetzt wird.
    """
    if ctx.p(code, "r_out_enabled", 0.0) <= 0.0:
        return 1.0
    q = ctx.ci.get("share_outdoor_workers")
    qbar = ctx.p(code, "qbar_out", 0.070)
    if q is None:
        return 1.0
    or_out = ctx.p(code, "or_out", 1.77)
    w_scc = ctx.p(code, "w_scc", 0.25)
    baf_c44 = ctx.p(code, "baf_c44", 1.675)
    if baf_c44 <= 0.0:
        return 1.0
    w_z = w_scc * 2.5 / baf_c44
    den = 1.0 + qbar * (or_out - 1.0)
    if den <= 0.0:
        return 1.0
    return max(0.0, (1.0 - w_z)
               + w_z * (1.0 + float(q) * (or_out - 1.0)) / den)


def uv_yll(risk: dict, ctx: CellContext) -> dict:
    """Verlorene Lebensjahre durch klimabedingte Hautkrebs-Zusatzfälle (§3.3/§3.4).

    ``F_e   = c_kal,e · Σ_a pop_a · I_e,a/100.000``          (Baseline-Fälle)
    ``ΔF_e  = F_e · BAF_e · ΔDosis``                          (Teil-Ausweis)
    ``YLL   = Σ_e ΔF_e · λ_e · L̄_e``                          (nativ)
    ``€     = Σ_e ΔF_e · c_e + YLL · VOLY``                    (Teil-Ausweis)

    Der €-Ausweis ist damit **nicht** allein outcome × Katalog-Kostensatz: zum
    VOLY-bewerteten Mortalitätsanteil kommen die Behandlungskosten der
    Zusatzfälle (Bericht §3.4). Beide Bestandteile sind golden-test-gebunden.
    """
    code = risk["code"]
    dd = uv_delta_dosis(ctx, code)
    # Bänderung wie #96 §3.2 (Bericht §3.5, Zeile ``a``) — dieselbe Herleitung
    # inkl. u20-Rückfall, damit beide Risiken dieselbe Bevölkerung sehen.
    bands = _pollen_age_bands(ctx)

    f_mm = ctx.p(code, "c_kal_mm", 1.022) * sum(
        pop * ctx.p(code, f"i_mm_{b}", UV_INCIDENCE_MM[b]) / 100_000.0
        for b, pop in bands.items())
    f_c44 = ctx.p(code, "c_kal_c44", 0.999) * sum(
        pop * ctx.p(code, f"i_c44_{b}", UV_INCIDENCE_C44[b]) / 100_000.0
        for b, pop in bands.items())

    d_mm = max(0.0, f_mm * ctx.p(code, "baf_mm", 0.60) * dd)
    d_c44 = max(0.0, f_c44 * ctx.p(code, "baf_c44", 1.675) * dd
                * _uv_r_out(ctx, code))

    yll = (d_mm * ctx.p(code, "lambda_mm", 0.1155) * ctx.p(code, "l_rest_mm", 10.58)
           + d_c44 * ctx.p(code, "lambda_c44", 0.00549)
           * ctx.p(code, "l_rest_c44", 5.30))

    out = _result(risk, yll)
    out["cost_eur"] += (d_mm * ctx.p(code, "c_fall_mm", 6724.0)
                        + d_c44 * ctx.p(code, "c_fall_c44", 5883.0))
    out["cases_melanoma"] = d_mm
    out["cases_c44"] = d_c44
    return out


# ── 3. Todesfälle durch Hochwasser/Sturzfluten ────────────────────────────────

def flood_regime(ctx: CellContext) -> float:
    """Sturzflut-Anteil der Zelle (0 = langsamer Anstieg, 1 = Sturzflut).

    Ohne Hydraulik (keine Tiefe, keine Fließgeschwindigkeit) ist das Gelände der
    einzige belastbare Unterscheider — und zugleich der wichtigste: Enge Steiltäler
    erzeugen schnelle, tödliche Fluten, flache Auen langsame. Genau das trennt
    Ahr 2021 von Elbe 2002.
    """
    slope = float(ctx.ci.get("slope_factor", ctx.ci.get("slope_proxy", 0.0)) or 0.0)
    depression = float(ctx.ci.get("depression_factor", ctx.ci.get("depression_proxy", 0.0)) or 0.0)
    return max(0.0, min(1.0, slope * (0.5 + 0.5 * depression)))


def _warning_modifier(ctx: CellContext, code: str) -> float:
    """Warnzeit/Notfallmanagement — der Hebel, den eine Kommune bedienen kann."""
    span = ctx.p(code, "warning_modifier_span", 0.6)
    vn = ctx.hev_norm.get("vulnerabilities", {})
    v = max(float(vn.get("EARLY_WARNING_SYSTEMS", 0.5) or 0.0),
            float(vn.get("EMERGENCY_MANAGEMENT", 0.5) or 0.0))
    return max(0.0, 1.0 - span / 2.0 + span * v)


def _elderly_share(ctx: CellContext) -> float:
    bands = _age_bands(ctx)
    total = sum(bands.values())
    return (total - bands.get("u65", 0.0)) / total if total > 0 else 0.0


def mortality_flood(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    intensity = ctx.haz_intensity("HEAVY_RAIN_FLOOD")
    if intensity <= 0.0 or ctx.pop <= 0.0:
        return _result(risk, 0.0)

    rate_flash = ctx.p(code, "fatality_rate_flash_per_100k", 9.0)
    rate_slow = ctx.p(code, "fatality_rate_slow_per_100k", 0.15)
    regime = flood_regime(ctx)
    rate = rate_slow + regime * (rate_flash - rate_slow)

    # Flutopfer sind überproportional alt und mobilitätseingeschränkt.
    age_span = ctx.p(code, "elderly_weight", 1.5)
    age_mod = 1.0 + age_span * (_elderly_share(ctx) - 0.22)

    outcome = (ctx.pop * (rate / 100_000.0) * intensity
               * _warning_modifier(ctx, code) * max(0.0, age_mod)
               * ctx.p(code, "calibration", 1.0))
    return _result(risk, outcome)


# ── 4. Todesfälle durch Stürme ────────────────────────────────────────────────

def mortality_storm(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    intensity = ctx.haz_intensity("EXTRATROPICAL_STORM")
    if intensity <= 0.0 or ctx.pop <= 0.0:
        return _result(risk, 0.0)

    rate = ctx.p(code, "fatality_rate_per_100k", 0.35)
    # Sturmtote fallen draußen und unterwegs: umstürzende Bäume an Straßen sind
    # der dominierende Mechanismus. Deshalb die Interaktion Kronen×Straße —
    # keine der beiden Größen allein bildet ihn ab.
    canopy = float(ctx.ci.get("canopy_frac", 0.0) or 0.0) + float(ctx.ci.get("forest_frac", 0.0) or 0.0)
    road = float(ctx.ci.get("road_cov", 0.0) or 0.0)
    tree_road = max(0.0, min(1.0, canopy * road * ctx.p(code, "tree_road_scale", 8.0)))

    bldg_vuln = float(ctx.hev_norm.get("vulnerabilities", {}).get("BUILDING_STABILITY", 0.5) or 0.0)

    w_base = ctx.p(code, "base_share", 0.4)
    w_tree = ctx.p(code, "tree_share", 0.4)
    w_bldg = ctx.p(code, "building_share", 0.2)
    exposure = w_base + w_tree * tree_road + w_bldg * bldg_vuln

    outcome = (ctx.pop * (rate / 100_000.0) * intensity * exposure
               * ctx.p(code, "calibration", 1.0))
    return _result(risk, outcome)


# ── 5. Verletzte — je Gefahr getrennt ─────────────────────────────────────────
# Bis Modellversion 6 lief das über EIN Risiko mit ``max()`` über drei Gefahren.
# Das war nicht nur unsauber, sondern falsch: Flut- und Sturmverletzte sind
# additive Ereignisse; eine Kommune, die beidem ausgesetzt ist, bekommt Verletzte
# aus beidem. Das Maximum behauptete, sie bekomme nur die schlimmere von beiden,
# und die ``alternate_hazard``-Ketten trugen zum absoluten Outcome gar nichts bei.
# Die Raten zählen ausschließlich **nicht-tödliche** Verletzte (die Todesfälle
# stehen in eigenen Kanälen), damit nichts doppelt bewertet wird.

def _injuries(risk: dict, ctx: CellContext, hazard: str, default_rate: float) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", default_rate)
    outcome = ctx.pop * (rate / 100_000.0) * ctx.haz_intensity(hazard) * ctx.g(risk)
    return _result(risk, outcome)


def injuries_flood(risk: dict, ctx: CellContext) -> dict:
    return _injuries(risk, ctx, "HEAVY_RAIN_FLOOD", 90.0)


def injuries_storm(risk: dict, ctx: CellContext) -> dict:
    return _injuries(risk, ctx, "EXTRATROPICAL_STORM", 55.0)


def injuries_landslide(risk: dict, ctx: CellContext) -> dict:
    return _injuries(risk, ctx, "LANDSLIDE", 5.0)


# ── 6. Psychische Gesundheit ───────────────────────────────────────────────────

def mental_health(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 1500.0)
    af = _heat_af(ctx, code, 0.0012, 10.0)
    # zusätzlicher Ereignisanteil (Extremereignisse/Kaskaden/Dürre); fixe Katalog-
    # Referenzgrenzen (haz_intensity, §3.3-Restlücke).
    event = max(ctx.haz_intensity("COMPOUND_EVENT"), ctx.haz_intensity("CASCADE_EVENT"),
                ctx.haz_intensity("DROUGHT"))
    driver = min(1.0, af + ctx.p(code, "event_share", 0.3) * event)
    outcome = ctx.pop * (rate / 100_000.0) * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 7. Betroffene / Evakuierte (Flut/Sturmflut/Feuer) ──────────────────────────

def affected_evacuated(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 2500.0)
    driver = max(ctx.haz_intensity("HEAVY_RAIN_FLOOD"),
                 ctx.haz_intensity("STORM_SURGE"),
                 ctx.haz_intensity("WILDFIRE"))
    outcome = ctx.pop * (rate / 100_000.0) * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 8. Wärmebelastungsstunden ──────────────────────────────────────────────────

def thermal_stress_hours(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    hours_ref = ctx.p(code, "hours_ref_per_100k", 400.0)
    ref_hd = ctx.p(code, "reference_hotdays", 20.0)
    hd = ctx.haz("HEAT_WAVE")
    driver = hd / ref_hd if ref_hd > 0 else 0.0
    outcome = (ctx.pop / 100_000.0) * hours_ref * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 9. Schadstoff-Belastungsstunden ────────────────────────────────────────────

def pollutant_exposure_hours(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    hours_ref = ctx.p(code, "hours_ref_per_100k", 250.0)
    ref_hd = ctx.p(code, "reference_hotdays", 20.0)
    hd = ctx.haz("HEAT_WAVE")   # bodennahes Ozon/Feinstaub korreliert mit Hitze
    driver = hd / ref_hd if ref_hd > 0 else 0.0
    outcome = (ctx.pop / 100_000.0) * hours_ref * driver * ctx.g(risk)
    return _result(risk, outcome)


HEALTH_IMPACTS = {
    "EXPECTED_ANNUAL_MORTALITY": mortality,
    "EXPECTED_ANNUAL_MORTALITY_FLOOD": mortality_flood,
    "EXPECTED_ANNUAL_MORTALITY_STORM": mortality_storm,
    "EXPECTED_ANNUAL_MORBIDITY": morbidity,
    "EXPECTED_ANNUAL_ALLERGY_DAYS": allergy_symptom_days,
    "EXPECTED_ANNUAL_UV_YLL": uv_yll,
    "EXPECTED_ANNUAL_INJURIES": injuries_flood,
    "EXPECTED_ANNUAL_INJURIES_STORM": injuries_storm,
    "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": injuries_landslide,
    "EXPECTED_ANNUAL_MENTAL_HEALTH": mental_health,
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": affected_evacuated,
    "EXPECTED_THERMAL_STRESS_HOURS": thermal_stress_hours,
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": pollutant_exposure_hours,
}


# ── Lineage-Spezifikation (Wirkungsdiagramm) ───────────────────────────────────
# Deklariert je Risiko, was die Funktion oben rechnet, damit ``lineage_graph`` den
# Schicht-B-Zweig des Wirkungsdiagramms exakt aus der tatsächlichen Rechnung baut.
# Muss die Funktionskörper spiegeln (Key-Gleichheit wird in
# tests/test_lineage_graph.py geprüft).
LINEAGE_SPECS: dict[str, dict] = {
    "EXPECTED_ANNUAL_MORTALITY": {
        "rate_param": "baseline_mort_a85p",
        # Basis ist NICHT die Gesamtbevölkerung: die Kurve läuft je Altersband.
        "basis_key": "pop_age_bands",
        "basis_label": "Bevölkerung je Altersband (Zelle)",
        # Rev. 7: empirische Wochenquantile je Region (REGION_WEEK_ANOMALIES)
        # statt Gauß-Streuung; YLL-Bewertung über life_years_* × VOLY-Kostensatz.
        "driver": {"kind": "erf", "hazard": "HEAT_WAVE",
                   "params": ["calibration", "life_years_a85p"]},
        # Kein g(V̂): mit expliziten Altersbändern zählte es die Demografie ein
        # zweites und drittes Mal; stattdessen die bandweisen, mittelwert-
        # zentrierten v_vers-Faktoren (Bericht #95 §3.3).
        "modifier": {
            "term": "v_vers-Modifikator",
            "label": "Isolation & Pflegeheim je Band",
            # Keine Schicht-A-Vulnerabilität mehr im D-Pfad: v_vers liest
            # ausschließlich Zellanteile (mit Bundesmittel-Fallback) + Parameter.
            "vulnerabilities": [],
            "cell_keys": ["share_single_65p", "share_care_home_85p"],
            "params": ["beta_iso", "beta_pfl", "qbar_1p", "qbar_pfl"],
            "note": ("Bandweiser, mittelwertzentrierter Versorgungs-/Isolations-"
                     "Modifikator (Bundesmittel = 1, kalibrierneutral; nur D-Pfad — "
                     "β_iso: Bänder 65+, β_pfl: nur 85+). Die Demografie steckt genau "
                     "einmal in den Altersbändern.\n"
                     r"$$v_{vers,a} = [1 + \mathbb{1}_{a\ge 65}\,\beta_{iso}"
                     r"(q_{1P}-\bar q_{1P})]\,[1 + \mathbb{1}_{85+}\,\beta_{pfl}"
                     r"(q_{pfl}-\bar q_{pfl})]$$"),
        },
    },
    "EXPECTED_ANNUAL_MORTALITY_FLOOD": {
        "rate_param": "fatality_rate_flash_per_100k",
        "driver": {"kind": "intensity", "hazards": ["HEAVY_RAIN_FLOOD"]},
        "modifier": {
            "term": "Warnung · Altersgewicht",
            "label": "Warnzeit & Altersgewicht",
            "vulnerabilities": ["EARLY_WARNING_SYSTEMS", "EMERGENCY_MANAGEMENT"],
            "params": ["warning_modifier_span", "elderly_weight", "calibration"],
            "note": ("Kein g(V̂), sondern die beiden Größen, die bei Fluttoten tatsächlich "
                     "entscheiden: die Vorwarnzeit — am Ahr 2021 der ausschlaggebende "
                     "Faktor und der Hebel, den eine Kommune bedienen kann — und der "
                     "Altersüberhang der Opfer.\n"
                     r"$$m = \bigl(1 - \tfrac{s}{2} + s\,\hat{V}_{\mathrm{Warn}}\bigr)"
                     r"\cdot \bigl(1 + a\,(\text{Anteil}_{65+} - 0{,}22)\bigr)$$"),
        },
    },
    "EXPECTED_ANNUAL_MORTALITY_STORM": {
        "rate_param": "fatality_rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["EXTRATROPICAL_STORM"]},
        "modifier": {
            "term": "Expositionsterm",
            "label": "Bäume × Straßen, Bausubstanz",
            "vulnerabilities": ["BUILDING_STABILITY"],
            "params": ["tree_road_scale", "base_share", "tree_share", "building_share",
                       "calibration"],
            "cell_keys": ["canopy_frac", "forest_frac", "road_cov"],
            "note": ("Sturmtote fallen draußen und unterwegs, nicht in der Wohnung. "
                     "Umstürzende Bäume an Straßen sind der dominierende Mechanismus — "
                     "deshalb die INTERAKTION Kronen×Straße: keine der beiden Größen "
                     "allein bildet ihn ab.\n"
                     r"$$e = w_{0} + w_{B}\,(\text{Kronen}\cdot\text{Straße})"
                     r" + w_{G}\,\hat{V}_{\mathrm{Bausubstanz}}$$"),
        },
    },
    "EXPECTED_ANNUAL_MORBIDITY": {
        "rate_param": "r0_a85p",
        "basis_key": "pop_age_bands",
        "basis_label": "Bevölkerung je Altersband (Zelle)",
        # Rev. 7: altersgeschichtete Baseline × zweiseitig linearer HD-Term
        # (bei 0 gedeckelt) statt AF-Exponentialform; F-Pfad bewusst OHNE
        # Modifikatoren (Gegen-/fehlende Evidenz, Bericht #95 §3.4/Log 28) —
        # no_modifier verhindert, dass das Diagramm ein g(V̂) erfindet.
        "no_modifier": True,
        "driver": {"kind": "hd_linear", "hazard": "HEAT_WAVE",
                   "params": ["excess_per_hotday", "hotday_ref_days"]},
    },
    "EXPECTED_ANNUAL_ALLERGY_DAYS": {
        # Rate = Prävalenz des größten Bandes (20–64); Basis = Altersbänder.
        "rate_param": "p_ar_a20_64",
        "basis_key": "pop_age_bands",
        "basis_label": "Bevölkerung je Altersband (Zelle)",
        "driver": {"kind": "season_spread", "hazard": "POLLEN_LOAD",
                   "params": ["f_symptomtage", "p_sens_birke", "p_sens_graeser",
                              "delta_s_birke_mitte", "delta_s_graeser_mitte",
                              "a_attr"]},
        "modifier": {
            "term": "P̂ (Vegetation)",
            "label": "Lokale Vegetationslast",
            "vulnerabilities": [],
            "params": ["lambda_veg"],
            "note": ("Mittelwertzentrierte Modulation über die lokale Pollenlast: "
                     "P̂ = 1 + λ(Ĝ/Ḡ − 1). Das Referenzmittel Ḡ ist das "
                     "betroffenengewichtete Mittel der EIGENEN KOMMUNE — die "
                     "Betrachtungsebene bleibt geschlossen (Aufgabe §3.2), und "
                     "Σ B·P̂ = Σ B gilt exakt: P̂ verteilt nur innerhalb der "
                     "Kommune um. Steht in BEIDEN Pfaden — Symptomtage und Euro "
                     "bleiben strikt proportional.\n"
                     r"$$\hat P_{z} = 1 + \lambda\,\bigl(\hat G_{z}/\bar G - 1\bigr)$$"),
        },
    },
    "EXPECTED_ANNUAL_UV_YLL": {
        # Rate = Inzidenz des tragenden Bandes (C44 75–84); Basis = Altersbänder.
        "rate_param": "i_c44_a75_84",
        "basis_key": "pop_age_bands",
        "basis_label": "Bevölkerung je Altersband (Zelle)",
        "driver": {"kind": "dose_change", "hazard": "UV_RADIATION",
                   "params": ["k_uv", "a_attr", "baf_mm", "baf_c44",
                              "c_kal_c44", "lambda_c44", "l_rest_c44"]},
        # Kein g(V̂): die Demografie steckt genau einmal in den Altersbändern,
        # und der einzige echte Modifikator (Außenberufe) ist geparkt.
        "no_modifier": True,
    },
    "EXPECTED_ANNUAL_INJURIES": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["HEAVY_RAIN_FLOOD"]},
    },
    "EXPECTED_ANNUAL_INJURIES_STORM": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["EXTRATROPICAL_STORM"]},
    },
    "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["LANDSLIDE"]},
    },
    "EXPECTED_ANNUAL_MENTAL_HEALTH": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "af_plus_event", "hazard": "HEAT_WAVE",
                   "params": ["beta_per_hotday", "hotday_threshold"],
                   "event_hazards": ["COMPOUND_EVENT", "CASCADE_EVENT", "DROUGHT"],
                   # editierbarer Registry-Parameter (risks.….impact.event_share)
                   "event_share_param": "event_share"},
    },
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity",
                   "hazards": ["HEAVY_RAIN_FLOOD", "STORM_SURGE", "WILDFIRE"]},
    },
    "EXPECTED_THERMAL_STRESS_HOURS": {
        "rate_param": "hours_ref_per_100k",
        "driver": {"kind": "ratio", "hazard": "HEAT_WAVE",
                   "params": ["reference_hotdays"]},
    },
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": {
        "rate_param": "hours_ref_per_100k",
        "driver": {"kind": "ratio", "hazard": "HEAT_WAVE",
                   "params": ["reference_hotdays"]},
    },
}

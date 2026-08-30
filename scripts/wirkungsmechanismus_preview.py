#!/usr/bin/env python3
"""Wirkungsmechanismus-Vorschau eines Methodik-Berichts im Produkt-Look (KAP3).

Erzeugt je Risiko eine eigenständige HTML-Datei neben dem Methodik-PDF
(docs/methodik/<nr>_wirkungsmechanismus.html), die das ECHTE
Produkt-Wirkungsdiagramm rendert (Frontend-Komponente LineageFlowDiagram,
gebaut als Standalone-Bundle via `frontend/vite.preview.config.ts`).

Die Vorschau speist sich aus der NEU AUSGEARBEITETEN METHODIK: Haupt-Tab ist
immer das Ziel-Modell laut Methodik-Bericht (LineageBuilder + dieselbe
Finalisierung wie das Produkt) — sie zeigt, was künftig implementiert wird.
Ist das Risiko bereits (teilweise) im Produkt, kommen zusätzlich
Vergleichstabs mit dem Ist-Stand aus Backend/Registry dazu (Divergenzen sind
Ledger-Befunde, #95: Befund 76).

Aufruf: scripts/wirkungsmechanismus_preview.py <risiko-nr>
Wird von scripts/export_methodik_pdf.sh nach dem PDF-Export aufgerufen.
"""
from __future__ import annotations

import base64
import datetime
import json
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.services import lineage_graph, parameter_registry  # noqa: E402
from app.services.lineage_graph import LineageBuilder, _prune_lineage  # noqa: E402

DIST = ROOT / "frontend" / "preview-dist"
OUT_DIR = ROOT / "docs" / "methodik"


# ── Hilfen ────────────────────────────────────────────────────────────────────

def _param(b: LineageBuilder, pid: str, label: str, value, unit: str,
           source: str, target: str, note: str = "") -> None:
    """Parameterknoten im Produkt-Schema (Kachel mit Wert/Einheit + Tooltip)."""
    nid = f"param:{pid}"
    b.add_node(
        nid, "parameter", label, column=1, collapse_group="parameters",
        meta={"parameter_id": pid, "value": value, "unit": unit,
              "source": source, **({"note": note} if note else {})},
    )
    b.add_edge(nid, target)


def _op(b: LineageBuilder, oid: str, kind: str, label: str, note: str) -> str:
    b.add_node(oid, "operator", label, column=2, collapse_group="operators",
               meta={"op_kind": kind, "note": note})
    return oid


def _mp(pid: str, label: str, value, unit: str, source: str) -> dict:
    """ModelParameter-Eintrag für die Parameter-Kacheln der Vorschau."""
    return {
        "id": pid, "layer_code": "preview", "layer_category": "risks",
        "label": label, "value": value, "default_value": value,
        "unit": unit, "source": source,
    }


# ── #96 Aeroallergene (geplantes Modell laut Bericht Rev. 1) ─────────────────

def _graph_96() -> tuple[dict, list[dict]]:
    b = LineageBuilder()
    params: list[dict] = []

    def P(pid, label, value, unit, source, target, note=""):
        _param(b, pid, label, value, unit, source, target, note)
        params.append(_mp(pid, label, value, unit, source))

    # Schicht A (Screening-Index, zusammengefasst)
    b.add_node("ind:POLLEN_LOAD", "hazard", "Pollenbelastung (POLLEN_LOAD — neu)",
               column=2, collapse_group="indicators",
               meta={"note": "Neue Kartenebene: mittelwertnormierter Anteil allergener "
                             "Vegetation Ĝ/Ḡ (OSM-Gehölz-/Grünstruktur), Bericht §3.3."})
    b.add_node("ind:POP", "exposure", "Bevölkerungsdichte", column=2,
               collapse_group="indicators")
    b.add_node("ind:EWS", "vulnerability", "Frühwarnsysteme / Versorgungszugang",
               column=2, collapse_group="indicators",
               meta={"note": "EARLY_WARNING_SYSTEMS (Pollen-Gefahrenindex) und "
                             "HEALTHCARE_ACCESS — nur Schicht A (Bericht Kap. 1)."})
    b.add_node("src:osm", "source", "OSM", column=0, collapse_group="sources",
               meta={"description": "OpenStreetMap (Vegetation/Gehölze)", "prov": "osm"})
    b.add_node("src:zensus", "source", "Zensus", column=0, collapse_group="sources",
               meta={"description": "Zensus 2022, 100-m-Gitter (inkl. neuer Ebene u20)",
                     "prov": "zensus"})
    b.add_node("src:dwd", "source", "DWD", column=0, collapse_group="sources",
               meta={"description": "DWD-CDC Phänologie-Jahresmelder (Blüte Beginn/Vollblüte)",
                     "prov": "dwd"})
    b.add_edge("src:osm", "ind:POLLEN_LOAD")
    b.add_edge("src:zensus", "ind:POP")
    mul_path = _op(b, "op:mul:path", "multiply", "×",
                   "Wirkungskette Schicht A: Ĥ(POLLEN_LOAD) × Ê(Bevölkerung) × V̂ "
                   "(Worst-Pathway, Bericht §3.7).")
    b.add_node("pathway:0", "pathway",
               "Pollenbelastung trifft Bevölkerung (Frühwarnung/Zugang dämpfen)",
               column=3, collapse_group="pathways",
               meta={"chain_label": "POLLEN_LOAD × Bevölkerung × Frühwarnung"})
    for nid in ("ind:POLLEN_LOAD", "ind:POP", "ind:EWS"):
        b.add_edge(nid, mul_path)
    b.add_edge(mul_path, "pathway:0")
    b.add_node("out:index", "outcome", "KWRA-Index", column=4,
               collapse_group="outcome",
               meta={"result_kind": "index", "unit": "0–100", "is_outcome": True,
                     "note": "Screening-Index (Schicht A) — nie auf €-Pfaden."})
    b.add_edge("pathway:0", "out:index")

    # Schicht B — Betroffene
    b.add_node("int:pop_bands", "intermediate", "Bevölkerung je Altersband",
               column=1, collapse_group="intermediates",
               meta={"note": "u20 (neu) · 20–64 · 65–74 · 75–84 · 85+ (Bericht §3.2)."})
    b.add_edge("src:zensus", "int:pop_bands")
    mul_b = _op(b, "op:mul:betroffene", "multiply", "×",
                "Betroffene = Σ Band-Bevölkerung × altersspezifische AR-Prävalenz.\n"
                r"$$B_{z} = \sum_a \mathrm{pop}_a \cdot p_{\mathrm{AR},a}$$")
    b.add_edge("int:pop_bands", mul_b)
    P("pollen.p_ar", "AR-Prävalenz je Band",
      "8,8 / 13,2 / 6,7 / 5,0 / 5,0", "%", "DEGS1/KiGGS (RKI)", mul_b,
      "12-Monats-Prävalenz, bevölkerungsgewichtet auf Produktbänder (Bericht §3.2).")
    b.add_node("int:betroffene", "intermediate", "Betroffene (aktive Pollenallergie)",
               column=2, collapse_group="intermediates",
               meta={"unit": "Personen", "note": "Bundessumme ≈ 8,96 Mio (Bericht §3.2)."})
    b.add_edge(mul_b, "int:betroffene")

    # Schicht B — Klimasignal
    b.add_node("int:delta_s", "intermediate", "Saison-Spreizung ΔS (Region)",
               column=1, collapse_group="intermediates",
               meta={"unit": "Tage",
                     "note": "Gemessen aus gepaarten DWD-Phänologie-Stationen "
                             "(1961–90 → 1991–2020): Birkengruppe +4,0/+4,2/+5,9, "
                             "Gräser +4,8/+4,1/+3,7 Tage (N/M/S) — Bericht §3.1, "
                             "Anlage pollensaison_region.csv."})
    b.add_edge("src:dwd", "int:delta_s")
    mul_d = _op(b, "op:mul:delta", "multiply", "×",
                "Zusatz-Symptomtage je Betroffenem und Jahr.\n"
                r"$$\delta_R = f\,\bigl(p_B\,\Delta S_{B,R} + p_G\,\Delta S_{G,R}\bigr)\,a_{\mathrm{attr}}$$")
    b.add_edge("int:delta_s", mul_d)
    P("pollen.p_sens_gruppen", "Sensibilisierungsprofil p_B/p_G", "0,55 / 0,75", "—",
      "Haftenberger 2013 (Stütze)", mul_d,
      "Anteil der Patienten mit Birkengruppen-/Gräser-Saison (gekennzeichnete "
      "Abschätzung, Bericht §3.4).")
    P("pollen.f_symptomtage", "Symptomtage-Anteil f", 0.70, "—",
      "Modellannahme (Band 0,50–0,85)", mul_d,
      "Kürzt sich im €-Pfad vollständig heraus (Bericht §3.5).")
    P("pollen.a_attr", "Klima-Attribution a_attr", 0.50, "—",
      "Anderegg 2021 (IQR 0,19–0,84)", mul_d)
    b.add_node("int:delta_pp", "intermediate", "Zusatztage je Betroffenem (δ)",
               column=2, collapse_group="intermediates",
               meta={"unit": "Tage/Jahr",
                     "note": "2,02 / 1,88 / 2,12 Tage (Nord/Mitte/Süd) — Bericht §3.3."})
    b.add_edge(mul_d, "int:delta_pp")

    # Schicht B — lokale Modulation
    b.add_node("int:g_allergen", "intermediate", "Allergene Vegetation Ĝ/Ḡ",
               column=1, collapse_group="intermediates",
               meta={"note": "Ebene POLLEN_LOAD (neu): betroffenengewichtetes "
                             "Bundesmittel = 1 (Referenzzustand fixiert, Bericht §3.3)."})
    b.add_edge("src:osm", "int:g_allergen")
    mul_p = _op(b, "op:mul:phat", "multiply", "×",
                "Lokaler Pollen-Faktor (zentriert, Bundessumme invariant).\n"
                r"$$\hat P_z = 1 + \lambda\,\bigl(\hat G_z/\bar G - 1\bigr)$$")
    b.add_edge("int:g_allergen", mul_p)
    P("pollen.lambda_veg", "Vegetations-Gewicht λ", 0.7, "—",
      "Werchan 2017/Bogawski 2019 (Band 0,3–1,0)", mul_p,
      "Kette Bericht §3.4 (#lambda-veg); wirkt in ΔTage UND €.")
    b.add_node("int:p_hat", "intermediate", "Lokaler Pollen-Faktor P̂",
               column=2, collapse_group="intermediates",
               meta={"unit": "0,65–1,35", "note": "Spanne bei Ĝ/Ḡ = 0,5…1,5."})
    b.add_edge(mul_p, "int:p_hat")

    # Natives Ergebnis + €
    mul_t = _op(b, "op:mul:tage", "multiply", "×",
                "Nativer Ausweis (klimaattribuiert, kein Sockel).\n"
                r"$$\Delta\mathrm{Tage}_z = B_z \cdot \delta_R \cdot \hat P_z$$")
    for nid in ("int:betroffene", "int:delta_pp", "int:p_hat"):
        b.add_edge(nid, mul_t)
    b.add_node("out:native", "outcome", "Zusätzliche Symptomtage",
               column=4, collapse_group="outcome",
               meta={"result_kind": "native", "unit": "Tage/Jahr", "is_outcome": True,
                     "note": "Nativer Ausweis; Rate: ΔTage je 1.000 EW·Jahr. "
                             "Bundessumme ≈ 17,8 Mio Tage/Jahr (Bericht §4)."})
    b.add_edge(mul_t, "out:native")
    cost = _op(b, "op:cost", "cost_rate", "Kostensatz",
               "Behandlungskostensatz je Symptomtag (populationsbasiert, TOTALL).\n"
               r"$$€_z = \Delta\mathrm{Tage}_z \cdot c_{\mathrm{Tag}}$$")
    b.add_edge("out:native", cost)
    P("pollen.c_tag", "Kostensatz je Symptomtag", 6.20, "€₂₀₂₄/Tag",
      "Cardell 2016 (TOTALL) / Schramm 2003 (Band 6,20–23,66)", cost,
      "= c_Jahr,direkt 266,90 € ÷ d_Saison 43,05 Tage (Bericht §3.5).")
    b.add_node("out:eur", "outcome", "Bewerteter Schaden — Konto K1 (Allergene)",
               column=5, collapse_group="outcome",
               meta={"result_kind": "eur", "unit": "€/Jahr", "is_outcome": True,
                     "note": "Bundessumme ≈ 110 Mio €₂₀₂₄/Jahr (Band 42–186; "
                             "Bericht §4). Untergrenze (nur K1; Intensität/Herbst/"
                             "Ambrosia nicht angesetzt)."})
    b.add_edge(cost, "out:eur")

    return _prune_lineage(b.build()), params


# ── #98 UV-Schädigungen (geplantes Modell laut Bericht Rev. 1) ───────────────

def _graph_98() -> tuple[dict, list[dict]]:
    b = LineageBuilder()
    params: list[dict] = []

    def P(pid, label, value, unit, source, target, note=""):
        _param(b, pid, label, value, unit, source, target, note)
        params.append(_mp(pid, label, value, unit, source))

    # Schicht A
    b.add_node("ind:UV", "hazard", "UV-Strahlung / Sonnenscheindauer (Ebene neu)",
               column=2, collapse_group="indicators",
               meta={"note": "DWD-CDC sunshine_duration (1 km), Normalperioden-Mittel "
                             "(Bericht §3.2/§3.6)."})
    b.add_node("ind:POP", "exposure", "Bevölkerungsdichte / Altersstruktur",
               column=2, collapse_group="indicators")
    b.add_node("ind:VERH", "vulnerability", "Verhalten / Bewusstsein / Screening",
               column=2, collapse_group="indicators",
               meta={"note": "S154/S155/S158 — Schicht A und Maßnahmen (Bericht Kap. 1/§5)."})
    b.add_node("src:dwd", "source", "DWD", column=0, collapse_group="sources",
               meta={"description": "DWD-CDC Sonnenscheindauer (Raster + Gebietsmittel)",
                     "prov": "dwd"})
    b.add_node("src:zensus", "source", "Zensus", column=0, collapse_group="sources",
               meta={"description": "Zensus 2022, 100-m-Gitter (inkl. Ebene u20)",
                     "prov": "zensus"})
    b.add_node("src:zfkd", "source", "ZfKD/RKI", column=0, collapse_group="sources",
               meta={"description": "Krebs in Deutschland 2025 (Inzidenz C43/C44; "
                                    "Ablesekette mit amtlicher Normierung)",
                     "prov": "computed"})
    b.add_edge("src:dwd", "ind:UV")
    b.add_edge("src:zensus", "ind:POP")
    mul_path = _op(b, "op:mul:path", "multiply", "×",
                   "Wirkungskette Schicht A: Ĥ(UV/SSD) × Ê(Bevölkerung/Alter) × V̂ "
                   "(Worst-Pathway, Bericht §3.7).")
    b.add_node("pathway:0", "pathway",
               "Steigende UV-Dosis trifft exponierte Bevölkerung",
               column=3, collapse_group="pathways",
               meta={"chain_label": "UV_RADIATION × Bevölkerung × Verhalten/Screening"})
    for nid in ("ind:UV", "ind:POP", "ind:VERH"):
        b.add_edge(nid, mul_path)
    b.add_edge(mul_path, "pathway:0")
    b.add_node("out:index", "outcome", "KWRA-Index", column=4,
               collapse_group="outcome",
               meta={"result_kind": "index", "unit": "0–100", "is_outcome": True})
    b.add_edge("pathway:0", "out:index")

    # Schicht B — Klimasignal
    b.add_node("int:ssd", "intermediate", "SSD-Änderung (Normalperioden)",
               column=1, collapse_group="intermediates",
               meta={"unit": "%",
                     "note": "SSD 1991–2020 vs. 1961–1990 je Zelle; DE +7,82 % "
                             "(N +6,3 / M +8,4 / S +7,5) — Bericht §3.2, Anlage "
                             "ssd_trend_region.csv."})
    b.add_edge("src:dwd", "int:ssd")
    mul_dd = _op(b, "op:mul:dosis", "multiply", "×",
                 "Klimaattribuierte Dosisänderung.\n"
                 r"$$\Delta\mathrm{Dosis}_z = \Delta\mathrm{SSD}_z \cdot k_{\mathrm{UV}} \cdot a_{\mathrm{attr}}$$")
    b.add_edge("int:ssd", mul_dd)
    P("uv.k_uv", "SSD→Dosis-Übersetzung k_UV", 0.84, "—",
      "Lorenz 2024 ÷ eigener NRW-SSD-Trend (Band 0,4–1,0)", mul_dd,
      "= Dosistrend 4,9 %/Dek. ÷ SSD-Trend 5,81 %/Dek., gleiches Fenster 1997–2022 "
      "(Bericht §3.2).")
    P("uv.a_attr", "Klima-Attribution a_attr", 0.75, "—",
      "gekennzeichnete Abschätzung (Band 0,5–1,0)", mul_dd)
    b.add_node("int:dosis", "intermediate", "Dosisänderung ΔDosis",
               column=2, collapse_group="intermediates",
               meta={"unit": "%", "note": "DE 4,95 % (N 3,96 / M 5,33 / S 4,76) — §3.2."})
    b.add_edge(mul_dd, "int:dosis")

    # Schicht B — Baseline
    b.add_node("int:pop_bands", "intermediate", "Bevölkerung je Altersband",
               column=1, collapse_group="intermediates")
    b.add_edge("src:zensus", "int:pop_bands")
    mul_base = _op(b, "op:mul:base", "multiply", "×",
                   "Baseline-Neuerkrankungen je Entität (MM, C44).\n"
                   r"$$F_{e,z} = c_{\mathrm{kal},e}\sum_a \mathrm{pop}_a\,\frac{I^{roh}_{e,a}}{10^5}$$")
    b.add_edge("int:pop_bands", mul_base)
    b.add_edge("src:zfkd", mul_base)
    P("uv.i_raten_roh", "Inzidenz je Band (roh)", "MM 0,5–94,9 · C44 2–1.480",
      "1/100.000·a", "ZfKD KID 2025 (Ablesekette, Anlage-CSV)", mul_base,
      "Normierung über c_kal je Entität (1,022 / 0,999) auf die amtlichen "
      "Fallzahlen 2023 (Bericht §3.3).")
    b.add_node("int:faelle", "intermediate", "Baseline-Fälle je Entität",
               column=2, collapse_group="intermediates",
               meta={"unit": "1/Jahr", "note": "reproduziert amtlich: 27.430 MM · "
                                               "242.820 C44 (2023)."})
    b.add_edge(mul_base, "int:faelle")

    # Zusatzfälle
    mul_df = _op(b, "op:mul:delta", "multiply", "×",
                 "Klimaattribuierte Zusatzfälle (gekennzeichnete Approximation, §3.4).\n"
                 r"$$\Delta F_{e,z} = F_{e,z} \cdot \mathrm{BAF}_e \cdot \Delta\mathrm{Dosis}_z$$")
    b.add_edge("int:faelle", mul_df)
    b.add_edge("int:dosis", mul_df)
    P("uv.baf", "Verstärkungsfaktor BAF", "MM 0,6 · C44 1,675", "—",
      "Slaper 1996 / RIVM 2023 / Madronich 2021", mul_df,
      "C44 = 0,75·1,4 + 0,25·2,5 (SCC-Anteil 0,25, KID 2025; Bericht §3.1).")
    P("uv.r_out_sensitivitaet", "Außenberufe r_out (Sensitivität)", 1.0, "—",
      "Schmitt 2011 (OR 1,77); Default 1", mul_df,
      "Kein Knoten der W186-Kette — Sensitivitätsband, Basiswert-Default 1 "
      "(Bericht Kap. 1/§3.4).")
    b.add_node("int:delta_f", "intermediate", "Zusatzfälle ΔF (Teil-Ausweis)",
               column=3, collapse_group="intermediates",
               meta={"unit": "1/Jahr",
                     "note": "Bundessumme ≈ 814 MM + 20.118 C44 (Bericht §4)."})
    b.add_edge(mul_df, "int:delta_f")

    # Mortalität → YLL (nativ)
    mul_yll = _op(b, "op:mul:yll", "multiply", "×",
                  "Mortalitätspfad (YLL × VOLY, MK 4.0/P52).\n"
                  r"$$\mathrm{YLL}_z = \sum_e \Delta F_{e,z}\,\lambda_e\,\bar L_e$$")
    b.add_edge("int:delta_f", mul_yll)
    P("uv.lambda", "Letalität λ", "MM 0,1155 · C44 0,0055", "—",
      "ZfKD 2023 (Perioden-Approximation)", mul_yll)
    P("uv.l_rest", "Restlebenserwartung L̄", "MM 10,58 · C44 5,30", "Jahre",
      "Sterbetafel 2022/2024 (Median-Approximation)", mul_yll)
    b.add_node("out:native", "outcome", "Verlorene Lebensjahre (YLL)",
               column=4, collapse_group="outcome",
               meta={"result_kind": "native", "unit": "Jahre/Jahr", "is_outcome": True,
                     "note": "Nativer Ausweis; Rate: YLL je 1.000 EW·Jahr. "
                             "Bundessumme ≈ 1.580 YLL/Jahr (Bericht §4)."})
    b.add_edge(mul_yll, "out:native")

    # €
    cost = _op(b, "op:cost", "cost_rate", "Kostensatz",
               "Monetarisierung K1 (Ursache UV).\n"
               r"$$€_z = \sum_e \Delta F_{e,z}\,c_e + \mathrm{YLL}_z \cdot \mathrm{VOLY}$$")
    b.add_edge("int:delta_f", cost)
    b.add_edge("out:native", cost)
    P("uv.c_fall", "Erstjahreskosten je Fall", "MM 6.724 · C44 5.883", "€₂₀₂₄",
      "Speckemeier 2022 (SCS-detektiert; Proxy)", cost)
    P("uv.voly", "VOLY", 160800, "€₂₀₂₄/Jahr", "UBA MK 4.0 / Amann 2020a", cost)
    b.add_node("out:eur", "outcome", "Bewerteter Schaden — Konto K1 (UV)",
               column=5, collapse_group="outcome",
               meta={"result_kind": "eur", "unit": "€/Jahr", "is_outcome": True,
                     "note": "Bundessumme ≈ 378 Mio €₂₀₂₄/Jahr (Band 119–653; "
                             "Bericht §4). Untergrenze; Latenz-Infokasten Pflicht."})
    b.add_edge(cost, "out:eur")

    return _prune_lineage(b.build()), params



# ── #95 Hitzebelastung (Ziel-Modell laut Bericht Rev. 7) ─────────────────────

def _graph_95_plan() -> tuple[dict, list[dict]]:
    b = LineageBuilder()
    params: list[dict] = []

    def P(pid, label, value, unit, source, target, note=""):
        _param(b, pid, label, value, unit, source, target, note)
        params.append(_mp(pid, label, value, unit, source))

    # Schicht A (zusammengefasst)
    b.add_node("ind:HEAT", "hazard", "Hitzewellen (HEAT_WAVE)", column=2,
               collapse_group="indicators")
    b.add_node("ind:POP", "exposure", "Bevölkerungsdichte / Altersstruktur",
               column=2, collapse_group="indicators")
    b.add_node("ind:VULN", "vulnerability", "Hitzesensitivität / Versorgungszugang",
               column=2, collapse_group="indicators")
    for sid, desc, prov in (("src:dwd", "DWD-CDC Klimaraster (Sommertemperatur, hot_days) "
                             "+ Tages-/Phänologie-Stationsdaten", "dwd"),
                            ("src:zensus", "Zensus 2022, 100-m-Gitter (Altersbänder, "
                             "Haushaltsgitter)", "zensus"),
                            ("src:osm", "OpenStreetMap (Stadtmodell/UHI, "
                             "Pflegeeinrichtungen)", "osm")):
        b.add_node(sid, "source", {"src:dwd": "DWD", "src:zensus": "Zensus",
                                   "src:osm": "OSM"}[sid], column=0,
                   collapse_group="sources", meta={"description": desc, "prov": prov})
    b.add_edge("src:dwd", "ind:HEAT")
    b.add_edge("src:zensus", "ind:POP")
    mul_path = _op(b, "op:mul:path", "multiply", "×",
                   "Wirkungskette Schicht A (Worst-Pathway, Bericht §3.7) — "
                   "nie auf €-Pfaden.")
    b.add_node("pathway:0", "pathway",
               "Hitzewellen treffen ältere, alleinlebende Bevölkerung",
               column=3, collapse_group="pathways",
               meta={"chain_label": "HEAT_WAVE × Bevölkerung/Alter × Sensitivität"})
    for nid in ("ind:HEAT", "ind:POP", "ind:VULN"):
        b.add_edge(nid, mul_path)
    b.add_edge(mul_path, "pathway:0")
    b.add_node("out:index", "outcome", "KWRA-Index", column=4,
               collapse_group="outcome",
               meta={"result_kind": "index", "unit": "0–100", "is_outcome": True})
    b.add_edge("pathway:0", "out:index")

    # Schicht B — Temperaturpfad
    b.add_node("int:t_zelle", "intermediate", "Zell-Sommertemperatur (DWD + UHI)",
               column=1, collapse_group="intermediates",
               meta={"unit": "°C",
                     "note": "DWD 1 km + mittelwerttreuer UHI-Zuschlag + Höhenkorrektur "
                             "(Bericht §3.1); Grünanteil steckt genau hier — kein "
                             "Doppelkanal."})
    b.add_edge("src:dwd", "int:t_zelle")
    b.add_edge("src:osm", "int:t_zelle")
    mul_tw = _op(b, "op:add:tw", "compute", "T_w",
                 "13 Sommerwochen aus empirischen intra-saisonalen Quantilen "
                 "(21 DWD-Stationen, 1991–2020; ersetzt die frühere Gauß-Setzung).\n"
                 r"$$T_w = \bar T_{Zelle} + q_{w,Region},\quad w = 1\dots13$$")
    b.add_edge("int:t_zelle", mul_tw)
    P("heat.q_wochenquantile", "Wochenquantile q_w (Region)",
      "CSV (N/M/S × 13)", "K", "eigene DWD-Auswertung (wochenquantile_region.csv)",
      mul_tw, "Bericht §3.2; σ_intra 2,36–2,58 K gemessen.")
    b.add_node("int:t_w", "intermediate", "Wochentemperaturen T_w",
               column=2, collapse_group="intermediates", meta={"unit": "°C"})
    b.add_edge(mul_tw, "int:t_w")

    mul_ex = _op(b, "op:exp:exzess", "compute", "RR−1",
                 "Wochen-Exzess der RKI-Expositions-Wirkungs-Funktion je Altersband.\n"
                 r"$$\sum_{w=1}^{13}\bigl(e^{\beta_a (T_w - T_{0,Region})_+} - 1\bigr)$$")
    b.add_edge("int:t_w", mul_ex)
    P("heat.t0_region", "Wirkschwelle T₀ (N/M/S)", "19,7 / 20,2 / 20,8", "°C",
      "Winklmayr 2022", mul_ex)
    P("heat.beta_85plus_region", "ERF-Steigung β₈₅₊ (N/M/S)",
      "0,0634 / 0,0625 / 0,0876", "1/K",
      "Winklmayr 2022 (Ablesekette §3.3); Süd = 0,0531 × 1,65 "
      "(Rev.-7-Nachschätzung, Holdout-Fit §4)", mul_ex)
    P("heat.f_alter", "Altersfaktoren f_a", "0,357 / 0,588 / 0,631 / 1,0", "—",
      "Rückrechnung Rev. 6 (§3.3a — ersetzt 0,404/0,577/0,62)", mul_ex)
    b.add_node("int:exzess", "intermediate", "Hitze-Exzess je Band (Jahressumme)",
               column=3, collapse_group="intermediates")
    b.add_edge(mul_ex, "int:exzess")

    # Bevölkerung + Basissterblichkeit + Modifikator
    b.add_node("int:pop_bands", "intermediate", "Bevölkerung je Altersband",
               column=1, collapse_group="intermediates")
    b.add_edge("src:zensus", "int:pop_bands")
    mul_vv = _op(b, "op:mul:vvers", "multiply", "×",
                 "Bandweiser Versorgungs-/Isolations-Modifikator "
                 "(mittelwertzentriert, kalibrierneutral).\n"
                 r"$$v_{vers,a} = [1 + \mathbb{1}_{a\ge 65}\,\beta_{iso}(q_{1P}-\bar q)]\,"
                 r"[1 + \mathbb{1}_{85+}\,\beta_{pfl}(q_{pfl}-\bar q_{pfl})]$$")
    b.add_edge("src:zensus", mul_vv)
    b.add_edge("src:osm", mul_vv)
    P("heat.beta_iso", "Isolations-Effekt β_iso (65+)", 0.90, "—",
      "Semenza 1996 / Mikrozensus 2023 (q̄ 0,346)", mul_vv, "nur D-Pfad (Log 28).")
    P("heat.beta_pfl", "Pflegeheim-Effekt β_pfl (85+)", 1.54, "—",
      "Fouillet/Bouchama/Klenk (Kette §3.3b; q̄ 0,149)", mul_vv, "nur D-Pfad.")
    b.add_node("int:v_vers", "intermediate", "Modifikator v_vers (bandweise)",
               column=2, collapse_group="intermediates")
    b.add_edge(mul_vv, "int:v_vers")

    mul_d = _op(b, "op:mul:d", "multiply", "×",
                "Hitzebedingte Todesfälle je Band (Teil-Ausweis).\n"
                r"$$D_a = c_{kal}\,v_{vers,a}\,\mathrm{pop}_a\,\frac{m_a}{10^5}\,"
                r"\frac{1}{52}\sum_w (e^{\beta_a\Delta_+}-1)$$")
    for nid in ("int:exzess", "int:pop_bands", "int:v_vers"):
        b.add_edge(nid, mul_d)
    P("heat.m_basissterberate", "Basissterberaten m_a",
      "213,2 / 1.737,9 / 4.812,3 / 14.800,2", "1/100.000·a",
      "Destatis 2023 (ersetzt 180/1.800/4.600/15.500)", mul_d)
    P("heat.c_kal", "Kalibrierfaktor c_kal", 0.581, "—",
      "RKI-Reihe, Fenster 2012–2024, Fit auf bevölkerungsgewichteten "
      "Sommermitteln (Rev. 7; ersetzt 0,742)", mul_d,
      "Genau ein nationaler Skalar (Band 0,55–0,66); Pauschalkorrektur und "
      "c_reg-Übergangsfaktoren sind in Rev. 7 entfallen (Bericht §4, "
      "Prüfstein 12/16).")
    b.add_node("int:d_faelle", "intermediate", "Hitzebedingte Todesfälle D (Teil-Ausweis)",
               column=4, collapse_group="intermediates",
               meta={"unit": "1/Jahr"})
    b.add_edge(mul_d, "int:d_faelle")

    mul_yll = _op(b, "op:mul:yll", "multiply", "×",
                  "Mortalitätsbewertung nach MK 4.0/P52: YLL statt Todesfall-Pauschale.\n"
                  r"$$\mathrm{YLL}_z = \sum_a D_a \cdot \bar L_a$$")
    b.add_edge("int:d_faelle", mul_yll)
    P("heat.l_restlebenserwartung", "Restlebenserwartung L̄_a",
      "23,39 / 15,59 / 8,90 / 5,44", "Jahre", "Sterbetafel 2022/2024 (§3.5)", mul_yll)
    b.add_node("out:native", "outcome", "Verlorene Lebensjahre (YLL)",
               column=5, collapse_group="outcome",
               meta={"result_kind": "native", "unit": "Jahre/Jahr", "is_outcome": True,
                     "note": "Native Ergebnisgröße laut Bericht (Log 3); Rate: YLL je "
                             "1.000 EW·Jahr."})
    b.add_edge(mul_yll, "out:native")

    # Morbidität (F-Pfad)
    b.add_node("int:hd", "intermediate", "Hitzetage HD (DWD hot_days)",
               column=1, collapse_group="intermediates",
               meta={"unit": "Tage/Jahr", "note": "ohne UHI-Verschiebung (Bericht §3.4)."})
    b.add_edge("src:dwd", "int:hd")
    mul_f = _op(b, "op:mul:f", "multiply", "×",
                "Hitzeassoziierte Erkrankungsfälle (zweiseitig linear, bei 0 gedeckelt).\n"
                r"$$F_z = \sum_a \mathrm{pop}_a\,\frac{r_{0,a}}{10^5}\,"
                r"\max(0,\,1 + e_{HD}(\mathrm{HD}-\mathrm{HD}_{ref}))$$")
    b.add_edge("int:hd", mul_f)
    b.add_edge("int:pop_bands", mul_f)
    P("heat.r0_einweisungsrate", "Baseline-Einweisungsraten r₀,a",
      "1,9 / 6,3 / 10,8 / 15,6", "1/100.000·a", "Destatis T67 + K&Z (§3.4)", mul_f)
    P("heat.e_hd", "Effekt je Hitzetag e_HD", 0.024, "1/Tag",
      "Karlsson & Ziebarth (konditional; Band bis 0,061)", mul_f)
    P("heat.hd_ref", "Referenz-Hitzetage HD_ref", 7.2, "Tage/Jahr",
      "K&Z-Basisperiode 1999–2008", mul_f)
    b.add_node("int:f_faelle", "intermediate", "Erkrankungsfälle F (Teil-Ausweis)",
               column=4, collapse_group="intermediates", meta={"unit": "1/Jahr"})
    b.add_edge(mul_f, "int:f_faelle")

    # €
    cost = _op(b, "op:cost", "cost_rate", "Kostensatz",
               "Monetarisierung K1 (Ursache Hitze).\n"
               r"$$€_z = \mathrm{YLL}_z \cdot \mathrm{VOLY} + F_z \cdot c_{Fall}$$")
    b.add_edge("out:native", cost)
    b.add_edge("int:f_faelle", cost)
    P("heat.voly", "VOLY", 160800, "€₂₀₂₄/Jahr",
      "UBA MK 4.0 / Amann 2020a (P52; VSL nur Sensitivität)", cost)
    P("heat.c_fall", "Behandlungskosten je Fall", 7152, "€₂₀₂₄",
      "Destatis Kostennachweis (Proxy)", cost)
    b.add_node("out:eur", "outcome", "Bewerteter Schaden — Konto K1 (Hitze)",
               column=6, collapse_group="outcome",
               meta={"result_kind": "eur", "unit": "€/Jahr", "is_outcome": True,
                     "note": "Untergrenze (nur K1); Infokästen/Raten laut Bericht §6."})
    b.add_edge(cost, "out:eur")

    return _prune_lineage(b.build()), params


# ── Payloads je Risiko ────────────────────────────────────────────────────────

def build_payload(nr: str) -> dict:
    today = datetime.date.today().strftime("%d.%m.%Y")
    if nr == "95":
        from app.data import catalog
        g, p = _graph_95_plan()
        tabs = [{
            "label": "Ziel-Modell (Bericht Rev. 7): YLL & €",
            "note": "So wird #95 nach /integriere-risiko 95 im Produkt gerechnet und "
                    "dargestellt (YLL × VOLY, empirische Wochenquantile, ein nationaler "
                    "Skalar c_kal 0,581 auf bevölkerungsgewichteter Kalibrierbasis, "
                    "β_Süd nachgeschätzt 0,0876, neue Altersketten).",
            "lineage": g, "parameters": p,
        }]
        params = parameter_registry.catalog_parameters()
        for code, label in (
                ("EXPECTED_ANNUAL_MORTALITY",
                 "Ist-Produktstand Mortalität (integriert)"),
                ("EXPECTED_ANNUAL_MORBIDITY",
                 "Ist-Produktstand Erkrankungen (integriert)")):
            if code in catalog.RISKS_BY_CODE:
                tabs.append({
                    "label": label,
                    "note": "Ist-Stand aus Backend-Registry/Lineage-Builder — seit der "
                            "Integration (30.08.2026) der Rev.-7-Stand (Befund 76 "
                            "geschlossen).",
                    "lineage": lineage_graph.build_risk_lineage(code),
                    "parameters": params,
                })
        return {
            "title": "#95 Hitzebelastung",
            "subtitle": "Ziel-Modell laut Methodik-Bericht Rev. 7 "
                        "(docs/methodik/95_hitzebelastung.md); Ist-Produktstand als "
                        "Vergleichstabs.",
            "banner": "Integration vollzogen (30.08.2026): Das Produkt rechnet den "
                      "Rev.-7-Stand des abgenommenen Berichts (YLL × VOLY, empirische "
                      "Wochenquantile, c_kal 0,581). Die Ist-Tabs kommen live aus "
                      "Backend-Registry/Lineage-Builder; Ledger-Befund 76 ist "
                      "geschlossen.",
            "generated": today,
            "tabs": tabs,
        }
    if nr == "96":
        g, p = _graph_96()
        return {
            "title": "#96 Aeroallergene pflanzlicher Herkunft",
            "subtitle": "Geplantes Schicht-B-Modell laut Methodik-Bericht "
                        "(docs/methodik/96_aeroallergene.md).",
            "banner": "Vorschau des geplanten Modells — noch nicht integriert. "
                      "Nach /integriere-risiko 96 erzeugt das Produkt dieses Diagramm "
                      "aus der Registry; Abweichungen wären ein Befund.",
            "generated": today,
            "tabs": [{"label": "Symptomtage & € (K1 Allergene)", "lineage": g,
                      "parameters": p}],
        }
    if nr == "98":
        g, p = _graph_98()
        return {
            "title": "#98 UV-bedingte Gesundheitsschädigungen",
            "subtitle": "Geplantes Schicht-B-Modell laut Methodik-Bericht "
                        "(docs/methodik/98_uv_schaedigungen.md).",
            "banner": "Vorschau des geplanten Modells — noch nicht integriert. "
                      "Nach /integriere-risiko 98 erzeugt das Produkt dieses Diagramm "
                      "aus der Registry; Abweichungen wären ein Befund.",
            "generated": today,
            "tabs": [{"label": "YLL, Zusatzfälle & € (K1 UV)", "lineage": g,
                      "parameters": p}],
        }
    print(f"HINWEIS: keine Wirkungsmechanismus-Vorschau für Risiko '{nr}' definiert "
          f"(bekannt: 95, 96, 98) — bei neuen Risiken hier einen Graph-Builder ergänzen.",
          file=sys.stderr)
    return {}


# ── Bundle-Inlining ──────────────────────────────────────────────────────────

def ensure_dist() -> None:
    if (DIST / "preview.html").exists():
        return
    print("preview-dist fehlt — baue Frontend-Bundle …", file=sys.stderr)
    subprocess.run(
        [str(ROOT / "frontend/node_modules/.bin/vite"), "build",
         "--config", "vite.preview.config.ts"],
        cwd=ROOT / "frontend", check=True,
    )


def _inline_css_assets(css: str) -> str:
    """Ersetzt url(...)-Referenzen (KaTeX-Fonts u. a.) durch data:-URIs."""
    def sub(m: re.Match) -> str:
        ref = m.group(1).strip("'\"")
        if ref.startswith("data:"):
            return m.group(0)
        f = DIST / "assets" / Path(ref).name
        if not f.exists():
            return m.group(0)
        mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        if f.suffix == ".woff2":
            mime = "font/woff2"
        elif f.suffix == ".woff":
            mime = "font/woff"
        elif f.suffix == ".ttf":
            mime = "font/ttf"
        b64 = base64.b64encode(f.read_bytes()).decode()
        return f"url(data:{mime};base64,{b64})"
    return re.sub(r"url\(([^)]+)\)", sub, css)


def assemble(payload: dict, out_path: Path) -> None:
    ensure_dist()
    html = (DIST / "preview.html").read_text(encoding="utf-8")
    js_ref = re.search(r'src="\./(assets/[^"]+\.js)"', html)
    css_ref = re.search(r'href="\./(assets/[^"]+\.css)"', html)
    assert js_ref and css_ref, "preview-dist/preview.html: Asset-Referenzen nicht gefunden"
    js = (DIST / js_ref.group(1)).read_text(encoding="utf-8")
    css = _inline_css_assets((DIST / css_ref.group(1)).read_text(encoding="utf-8"))
    # </script> im JSON-Payload entschärfen
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    page = html
    page = page.replace(
        f'<script type="module" crossorigin src="./{js_ref.group(1)}"></script>', "")
    page = page.replace(
        f'<link rel="stylesheet" crossorigin href="./{css_ref.group(1)}">', "")
    page = page.replace(
        "</head>", f"<style>\n{css}\n</style>\n</head>")
    page = page.replace(
        "</body>",
        f'<script>window.__LINEAGE_PREVIEW__ = {data};</script>\n'
        f'<script type="module">\n{js}\n</script>\n</body>')
    out_path.write_text(page, encoding="utf-8")
    print(f"Wirkungsmechanismus-Vorschau erzeugt: {out_path}")
    # Snap-/Flatpak-Browser dürfen nicht auf /opt zugreifen — falls der Nutzer
    # ~/kap2-vorschau angelegt hat, dort eine Kopie aktuell halten.
    mirror = Path.home() / "kap2-vorschau"
    if mirror.is_dir():
        (mirror / out_path.name).write_text(page, encoding="utf-8")
        print(f"  Kopie für den Browser: {mirror / out_path.name}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Aufruf: wirkungsmechanismus_preview.py <risiko-nr>")
    nr = sys.argv[1]
    payload = build_payload(nr)
    if not payload:
        return
    slug = {"95": "95_hitzebelastung", "96": "96_aeroallergene",
            "98": "98_uv_schaedigungen"}[nr]
    assemble(payload, OUT_DIR / f"{slug}_wirkungsmechanismus.html")


if __name__ == "__main__":
    main()

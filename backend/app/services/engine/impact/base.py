"""CellContext + Bausteine für die Schicht-B-Schadensfunktionen (Stufe 4).

Eine ``CellContext`` bündelt alles, was eine Impact-Funktion je Zelle braucht: die
absoluten Rohgrößen (``ci``), die absoluten und normierten H/E/V-Werte, die Risiko-
Indizes (Screening) und den regionalen Kontext. Die absoluten Hazard-Werte
(z. B. Hitzetage je Zelle in ``hev["hazards"]["HEAT_WAVE"]``) sind die **Intensität**,
mit der die Schadensfunktionen rechnen — statt des dimensionslosen Index.

``g(risk)`` ist der Vulnerabilitäts-Modifikator ``0,5 + V̂`` (MODELL_KRITIK §6): der
Mittelwert der normierten Sensitivitäten des Risikos hebt/senkt den Outcome
(V̂=0 → ×0,5, V̂=1 → ×1,5), ohne die Linearitätsfehler des Index selbst zu erben.

Parameter werden über die Registry-IDs ``risks.<CODE>.impact.<key>`` (risikospezifisch)
bzw. ``impact.<key>`` (global) aufgelöst und sind damit editier- und override-fähig.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

from app.services.engine import override_context


@dataclass
class CellContext:
    ci: dict            # absolute Zell-Rohgrößen (pop, Alter, Flächen, Assets, uhi_delta …)
    hev: dict           # absolute H/E/V ({"hazards": {...}, "exposures": {...}, "vulnerabilities": {...}})
    hev_norm: dict      # normierte H/E/V (0..1)
    indices: dict       # Risiko-Code → Index (Screening)
    regional: dict      # regionaler Kontext (hot_days, heavy_rain_index, …)

    @property
    def pop(self) -> float:
        return float(self.ci.get("pop", 0.0) or 0.0)

    def inp(self, key: str, default: float = 0.0) -> float:
        v = self.ci.get(key, default)
        return float(v) if v is not None else float(default)

    def haz(self, code: str) -> float:
        """Absoluter Hazard-Wert der Zelle (Intensität), z. B. Hitzetage."""
        return float(self.hev.get("hazards", {}).get(code, 0.0) or 0.0)

    def haz_norm(self, code: str) -> float:
        """Screening-normierter Hazard-Wert der Zelle (0..1), MIT Norm-Overrides.

        Nur für Screening/Index gedacht — NICHT als Schadensfunktions-Treiber, sonst
        veränderte ein editierter Screening-Normbereich die absoluten Schäden (§3.3)."""
        return float(self.hev_norm.get("hazards", {}).get(code, 0.0) or 0.0)

    def haz_intensity(self, code: str) -> float:
        """Normierte Hazard-Intensität (0..1) mit FIXEN Katalog-Referenzgrenzen.

        Treiber der Schicht-B-Schadensfunktionen: entkoppelt von den editierbaren
        Screening-Normgrenzen (norm_min/max). Damit ändert ein Screening-Norm-Override
        NICHT mehr die absoluten €/Outcome-Werte (behebt die §3.3-Restlücke); die
        Schicht-B-Editierbarkeit läuft ausschließlich über die Impact-Parameter
        (Rate/Kurve/Assetwert), nicht über die Screening-Normierung. Ohne Norm-Override
        ist ``haz_intensity`` identisch zu ``haz_norm`` (gleiche Katalog-Grenzen)."""
        from app.data import catalog
        meta = catalog.INDICATOR_BY_CODE.get(code, {})
        lo = float(meta.get("norm_min", 0.0))
        hi = float(meta.get("norm_max", 1.0))
        if hi <= lo:
            return 0.0
        x = (self.haz(code) - lo) / (hi - lo)
        return max(0.0, min(1.0, x))

    def g(self, risk: dict) -> float:
        """Vulnerabilitäts-Modifikator 0,5 + Mittel(V̂) des Risikos (0,5..1,5)."""
        vcodes = risk.get("vulnerabilities", [])
        vs = [float(self.hev_norm.get("vulnerabilities", {}).get(c, 0.0) or 0.0) for c in vcodes]
        return 0.5 + (sum(vs) / len(vs) if vs else 0.0)

    def p(self, risk_code: str, key: str, default: float) -> float:
        """Risikospezifischer, override-fähiger Impact-Parameter."""
        v = override_context.get_override(f"risks.{risk_code}.impact.{key}", default)
        return float(v) if v is not None else float(default)

    def pg(self, key: str, default: float) -> float:
        """Globaler, override-fähiger Impact-Parameter (``impact.<key>``)."""
        v = override_context.get_override(f"impact.{key}", default)
        return float(v) if v is not None else float(default)


def attributable_fraction(intensity: float, beta: float, threshold: float) -> float:
    """Attributable Fraktion ``1 − exp(−β·(Intensität − Schwelle)+)`` ∈ [0, 1).

    Nichtlinear in der Intensität: unterhalb der Schwelle 0, darüber steigend und durch 1
    begrenzt (eine attributable Fraktion kann nicht > 100 % sein). Durch die Schwelle ist
    die Wirkung **überproportional in der Rohintensität** (Verdopplung der Hitzetage mehr
    als verdoppelt die attributable Mortalität) — behebt den Linearitätsfehler des
    Index-Modells (MODELL_KRITIK §3.4). β und Schwelle sind editierbar (RKI/Winklmayr 2022).
    """
    return 1.0 - exp(-beta * max(0.0, intensity - threshold))

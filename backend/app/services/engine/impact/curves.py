"""Schadenskurven für die monetären Schadensfunktionen (Schicht B, §6.2).

``damage_fraction`` bildet die normierte Hazard-Intensität (0..1) über eine konvexe
Kurve auf einen jährlichen Schadensgrad (0..1) ab. Konvex (Exponent > 1), weil der
Schaden mit der Intensität überproportional steigt (Tiefe-Schaden-Kurven, HOWAS21/JRC):
geringe Belastung → geringer Schaden, hohe Belastung → stark steigend.

Hinweis: Die exakte Tiefe-Schaden-Kurve auf Basis von Wassertiefen je Wiederkehrperiode
(JRC River Flood Hazard Maps, KOSTRA) ist als spätere Verfeinerung vorgesehen (braucht
rasterio + den DE-Ausschnitt-Download). Hier wird die real vorhandene, normierte
Hazard-Intensität der Zelle als annualisierter Schadenstreiber genutzt.
"""

from __future__ import annotations


def damage_fraction(intensity_norm: float, exponent: float = 1.5) -> float:
    """Konvexe Schadensgrad-Kurve: ``clamp(intensity, 0, 1) ** exponent`` ∈ [0, 1]."""
    x = max(0.0, min(1.0, intensity_norm))
    return x ** exponent

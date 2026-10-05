"""Maßnahmen des PDF-Ergebnisberichts (Teil 6, T-1419): Daten je Maßnahme und Rangfolge.

Eine Zeile entsteht aus dem Ergebnis von ``measure_service.compute_impact`` (``impact_summary``)
einer angelegten Maßnahme — derselben Rechnung, aus der Oberfläche und Maßnahmen-Excel lesen:

- **Kosten:** CAPEX und OPEX je Jahr mit ihren Komponenten aus ``cost_breakdown``; jede
  Komponente trägt ihre Quelle aus dem Katalog (``compute_costs``). Eine Komponente ohne Quelle
  bricht die Erzeugung ab (Vorgabe P1: kein leeres Quellenfeld im Bericht).
- **Vermiedene Schäden je Jahr:** ``annual_benefit_damage_eur`` + ``annual_benefit_flat_eur``,
  dazu ein direkter Zusatznutzen (``annual_benefit_direct_eur``) getrennt.
- **Gewissheit und Umsetzung:** dieselben Zellentexte wie die Spalten „Gewissheit“ und
  „Umsetzung“ des Maßnahmen-Excel (``export_service.gewissheit_text``/``umsetzung_text``); nur
  der Ablagevermerk „abgelegt unter docs/…“ in einer Quellenangabe fällt weg (``ohne_ablageort``,
  harte Regel 4: kein Pfad aus dem Produkt-Repo im Bericht).
- **Qualitativ:** Trägt die Maßnahme keinen Euro-Nutzen (Vermerk ``benefit_display`` statt
  Betrag, oder Nutzen nicht positiv), ist sie *qualitativ*: kein Euro-Betrag für die Wirkung,
  keine Kennzahl, Rang hinter allen bezifferten Maßnahmen (Gliederung Teil 6, P2).

**Nutzen-Kosten-Verhältnis** (Rangfolge): vermiedene Schäden und Zusatznutzen über den
Betrachtungszeitraum geteilt durch die Kosten im selben Zeitraum,

    Verhältnis = Nutzen je Jahr × J / (CAPEX + OPEX je Jahr × J),

J = Jahre vom Umsetzungsjahr bis zum Ende des Projektionszeitraums des Produkts (2065),
unabgezinst und mit zeitkonstanter Wirkung — dieselben Annahmen wie die Kostenprojektion des
Produkts (``cost_projection_service``, reine Zeitpräferenzrate 0 %).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from app.services.ergebnisbericht.klima import JAHRE_PROJEKTION

#: Ende des Betrachtungszeitraums: letztes Jahr der Klimaprojektion des Produkts.
HORIZONT_ENDE = JAHRE_PROJEKTION[-1]

QUALITATIV = "qualitativ"

_BLOCK = {"capex": "CAPEX (einmalig)", "opex": "OPEX je Jahr"}

# Ablagevermerk in den Quellen der Umsetzungsdaten („; abgelegt unter docs/quellen/…pdf“). Er nennt
# den Speicherort im Produkt-Repo, keinen Wert; harte Regel 4 verbietet ihn im Bericht.
_ABLAGE = re.compile(r";?\s*abgelegt unter docs/[^\s)]*")


def ohne_ablageort(text: str) -> str:
    """Zellentext ohne den Ablagevermerk im Produkt-Repo; alles Übrige bleibt Zeichen für Zeichen."""
    return _ABLAGE.sub("", text)


@dataclass
class Kostenkomponente:
    block: str                # "capex" | "opex"
    bezeichnung: str
    einzelpreis_eur: float
    menge: float
    mengeneinheit: str
    betrag_eur: float
    quelle: str


@dataclass
class Massnahmenzeile:
    code: str
    name: str
    ort: str
    umsetzungsjahr: int
    capex_eur: float
    opex_eur: float
    komponenten: list[Kostenkomponente]
    gewissheit: str           # Zellentext wie Spalte „Gewissheit“ des Maßnahmen-Excel
    umsetzung: str            # Zellentext wie Spalte „Umsetzung“ des Maßnahmen-Excel
    vermiedene_schaeden_eur: float | None = None
    zusatznutzen_eur: float | None = None
    vermerk: str | None = None      # nur bei qualitativen Maßnahmen: warum kein Betrag
    flaeche_m2: float | None = None
    kosten_offen: bool = False      # summary: kosten_nutzen_kennzahl_offen (Stadtbaum ohne Fall/Stückzahl)
    kosten_vermerk: str | None = None
    extra: dict = field(default_factory=dict)

    @property
    def qualitativ(self) -> bool:
        return self.nutzen_eur is None

    @property
    def nutzen_eur(self) -> float | None:
        """Nutzen je Jahr (vermiedene Schäden + Zusatznutzen); None bei qualitativer Maßnahme."""
        if self.vermerk is not None:
            return None
        n = (self.vermiedene_schaeden_eur or 0.0) + (self.zusatznutzen_eur or 0.0)
        return n if n > 0 else None

    @property
    def jahre(self) -> int:
        """Jahre im Betrachtungszeitraum, Umsetzungsjahr eingeschlossen (mindestens 1)."""
        return max(1, HORIZONT_ENDE - self.umsetzungsjahr + 1)

    @property
    def kosten_zeitraum_eur(self) -> float:
        return self.capex_eur + self.opex_eur * self.jahre

    @property
    def nutzen_kosten(self) -> float | None:
        """Nutzen-Kosten-Verhältnis über den Betrachtungszeitraum; ``math.inf`` ohne Kosten,
        None bei qualitativer Maßnahme und bei offenen Kosten (``kosten_offen``: keine Kennzahl)."""
        n = self.nutzen_eur
        if n is None or self.kosten_offen:
            return None
        k = self.kosten_zeitraum_eur
        return math.inf if k <= 0 else n * self.jahre / k


def massnahmenzeile(measure_type: str, name: str, summary: dict, *, ort: str,
                    umsetzungsjahr: int) -> Massnahmenzeile:
    """Eine Berichtszeile aus dem ``impact_summary`` einer Maßnahme."""
    from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
    from app.services import massnahmen_gewissheit as mg
    from app.services.export_service import gewissheit_text, umsetzung_text

    komponenten: list[Kostenkomponente] = []
    for block in ("capex", "opex"):
        for c in ((summary.get("cost_breakdown") or {}).get(block) or {}).get("components") or []:
            quelle = str(c.get("source") or "").strip()
            if not quelle:
                raise ValueError(f"Maßnahme {name!r}: Kostenkomponente {c.get('param')!r} ohne "
                                 f"Quelle; ein leeres Quellenfeld wird nicht gedruckt (P1)")
            komponenten.append(Kostenkomponente(
                block=block, bezeichnung=str(c.get("label") or c.get("param")),
                einzelpreis_eur=float(c.get("unit_price") or 0.0),
                menge=float(c.get("quantity") or 0.0),
                mengeneinheit=str(c.get("quantity_unit") or ""),
                betrag_eur=float(c.get("amount_eur") or 0.0), quelle=quelle))

    schaeden = float(summary.get("annual_benefit_damage_eur") or 0.0) \
        + float(summary.get("annual_benefit_flat_eur") or 0.0)
    zusatz = float(summary.get("annual_benefit_direct_eur") or 0.0)
    if "annual_benefit_damage_eur" not in summary and "annual_benefit_flat_eur" not in summary:
        schaeden = float(summary.get("annual_benefit_eur") or 0.0) - zusatz
    vermerk = summary.get("benefit_display") or None
    if vermerk is None and schaeden + zusatz <= 0:
        vermerk = ("Für diese Maßnahme liegt keine in Euro bezifferte Wirkung vor; sie ist "
                   "deshalb qualitativ bewertet.")

    gewissheit = {g["code"]: g for g in mg.massnahmen_gewissheit()}.get(measure_type)
    return Massnahmenzeile(
        code=measure_type, name=name, ort=ort, umsetzungsjahr=int(umsetzungsjahr),
        capex_eur=float(summary.get("capex_eur") or 0.0),
        opex_eur=float(summary.get("opex_annual_eur") or 0.0),
        komponenten=komponenten,
        gewissheit=gewissheit_text(gewissheit),
        umsetzung=ohne_ablageort(umsetzung_text(MASSNAHMEN_UMSETZUNG.get(measure_type))),
        vermiedene_schaeden_eur=schaeden if schaeden > 0 else None,
        zusatznutzen_eur=zusatz if zusatz > 0 else None,
        vermerk=vermerk,
        flaeche_m2=summary.get("affected_area_m2"),
        kosten_offen=bool(summary.get("kosten_nutzen_kennzahl_offen")),
        kosten_vermerk=summary.get("kosten_vermerk") or None,
    )


def rangfolge(zeilen: list[Massnahmenzeile]) -> list[Massnahmenzeile]:
    """Bezifferte Maßnahmen absteigend nach Nutzen-Kosten-Verhältnis (bei Gleichstand nach
    Nutzen, dann Name), danach die qualitativen in der Reihenfolge nach Name."""
    bezifferte = [z for z in zeilen if not z.qualitativ and z.nutzen_kosten is not None]
    offene = [z for z in zeilen if not z.qualitativ and z.nutzen_kosten is None]
    qualitative = [z for z in zeilen if z.qualitativ]
    bezifferte.sort(key=lambda z: (-z.nutzen_kosten, -z.nutzen_eur, z.name))
    offene.sort(key=lambda z: (-(z.nutzen_eur or 0.0), z.name))
    qualitative.sort(key=lambda z: z.name)
    return bezifferte + offene + qualitative


def blockname(block: str) -> str:
    return _BLOCK[block]

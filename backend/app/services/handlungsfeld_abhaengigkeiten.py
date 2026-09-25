"""Abhängigkeiten der gerechneten Klimawirkungen über Handlungsfelder (Anforderung A4).

Leitfaden-Anforderung A4 (S. 30): „Eine handlungsfeld- … übergreifende Betrachtung der
Ergebnisse hilft, wechselseitige Abhängigkeiten zu identifizieren.“

Beleg ist ausschließlich die Liste der im Fließtext der KWRA 2021 (Teilbericht 6,
Kapitel 3.4) benannten Einzelbeziehungen ``kwra_querverbindungen.BENANNTE_BEZIEHUNGEN``
— dieses Modul führt keine eigene Beziehungsliste. Je gerechneter Klimawirkung
(je ``kwra_id`` einmal) werden die Beziehungen ausgegeben, in denen sie Quelle oder
Ziel ist. Eine Beziehung mit ``richtung`` „gegenseitig“ gilt in beide Richtungen,
wie in ``querverbindungen.querverbindungs_auswertung``.

Es gibt keine Gewichtung und keine Stärke: Wie stark eine Abhängigkeit wirkt, legt
der CMO fest (Anmerkung M-0005). Das Handlungsfeld eines Partners stammt aus
``catalog.RISKS``/``catalog.PLANNED_RISKS`` (``kwra_field``), ersatzweise aus
``kwra_querverbindungen.NETZROLLEN`` (``handlungsfeld``), danach aus den Knoten von
``kwra_rueckkopplungen.RUECKKOPPLUNGEN``; ist es dort nirgends geführt, bleibt es
``None`` — es wird nicht ergänzt.
"""

from __future__ import annotations

from app.data import catalog
from app.data import kwra_querverbindungen as kq
from app.data import kwra_rueckkopplungen as rk


def _handlungsfeld_je_kwra_id() -> dict[int, str]:
    """Handlungsfeld je kwra_id aus Katalog (RISKS vor PLANNED_RISKS), dann Netzrollen."""
    felder: dict[int, str] = {}
    for eintrag in list(catalog.RISKS) + list(catalog.PLANNED_RISKS):
        if eintrag.get("kwra_field"):
            felder.setdefault(eintrag["kwra_id"], eintrag["kwra_field"])
    for eintrag in kq.NETZROLLEN:
        if eintrag.get("handlungsfeld"):
            felder.setdefault(eintrag["kwra_id"], eintrag["handlungsfeld"])
    # Weiterer Rückfall: Knoten der Rückkopplungen (TB 6 Kap. 3.4, S. 82, 85–86, Abb. 9),
    # z. B. #65 Bedarf an Kühlenergie → Energiewirtschaft.
    for rueckkopplung in rk.RUECKKOPPLUNGEN:
        for knoten in rueckkopplung["knoten"]:
            if knoten.get("handlungsfeld"):
                felder.setdefault(knoten["kwra_id"], knoten["handlungsfeld"])
    return felder


def _gerechnete_klimawirkungen(gerechnete_codes) -> dict[int, dict]:
    """kwra_id → Katalogeintrag (erster Teil-Ausweis) der gerechneten Risiko-Codes."""
    if gerechnete_codes is None:
        gerechnete_codes = [r["code"] for r in catalog.RISKS]
    klimawirkungen: dict[int, dict] = {}
    for code in gerechnete_codes:
        if code not in catalog.RISKS_BY_CODE:
            raise ValueError(f"Unbekannter Risiko-Code (nicht in catalog.RISKS): {code}")
        risiko = catalog.RISKS_BY_CODE[code]
        klimawirkungen.setdefault(risiko["kwra_id"], risiko)
    return klimawirkungen


def abhaengigkeiten_der_kommune(gerechnete_codes=None) -> list[dict]:
    """Benannte Beziehungen je gerechneter Klimawirkung und die darüber erreichten
    anderen Handlungsfelder.

    ``gerechnete_codes``: Risiko-Codes aus ``catalog.RISKS``; ohne Argument alle.
    Liefert je ``kwra_id`` genau einen Eintrag, aufsteigend nach ``kwra_id``.
    """
    gerechnet = _gerechnete_klimawirkungen(gerechnete_codes)
    felder = _handlungsfeld_je_kwra_id()

    ergebnis: list[dict] = []
    for kid, risiko in sorted(gerechnet.items()):
        eigenes_feld = risiko.get("kwra_field")
        beziehungen: list[dict] = []
        for nr, b in enumerate(kq.BENANNTE_BEZIEHUNGEN):
            gegenseitig = b.get("richtung") == "gegenseitig"
            if b.get("quelle_kwra_id") == kid:
                partner_id, partner_name = b.get("ziel_kwra_id"), b.get("ziel")
                wirkt_auf_partner, partner_wirkt_ein = True, gegenseitig
            elif b.get("ziel_kwra_id") == kid:
                partner_id, partner_name = b.get("quelle_kwra_id"), b.get("quelle")
                wirkt_auf_partner, partner_wirkt_ein = gegenseitig, True
            else:
                continue
            partner_feld = felder.get(partner_id) if partner_id is not None else None
            beziehungen.append({
                "beziehung_nr": nr,
                "partner_kwra_id": partner_id,
                "partner_name": partner_name,
                "partner_handlungsfeld": partner_feld,
                "partner_gerechnet": partner_id is not None and partner_id in gerechnet,
                "anderes_handlungsfeld": (
                    partner_feld is not None and partner_feld != eigenes_feld
                ),
                "richtung": b.get("richtung"),
                "wirkt_auf_partner": wirkt_auf_partner,
                "partner_wirkt_ein": partner_wirkt_ein,
                "beleg": b.get("beleg"),
            })
        andere_felder = sorted({
            e["partner_handlungsfeld"] for e in beziehungen if e["anderes_handlungsfeld"]
        })
        ergebnis.append({
            "kwra_id": kid,
            "name": risiko.get("kwra_name") or risiko["name"],
            "handlungsfeld": eigenes_feld,
            "beziehungen": beziehungen,
            "andere_handlungsfelder": andere_felder,
        })
    return ergebnis

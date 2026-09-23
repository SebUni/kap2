"""Ausgebbare Nachweisfassung in Markdown (Ticket T-0463, Teil 3 des Nachweises
nach § 8 Abs. 1 KAnG, Vorhaben T-0445).

Dieses Modul formatiert ausschließlich den von
``app.services.kang_beruecksichtigung.nachweis_fachuebergreifend`` gelieferten
Nachweis als Markdown-Dokument. Es rechnet nichts nach und kennt den
Risiko-/Maßnahmenkatalog nicht; jede Zahl und jeder Status kommt unverändert
aus dem übergebenen ``nachweis``-dict.

Bewusst **nicht** Teil dieses Pakets: Anbindung an ``export_service.py`` oder
eine Route — das sind eigene, parallele Tickets.
"""

from __future__ import annotations

TITEL = "# Nachweis der fachübergreifenden und integrierten Berücksichtigung (§ 8 Abs. 1 KAnG)"

METHODENVERWEIS = (
    "Feld-für-Feld-Erläuterung dieses Nachweises: siehe "
    "`docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md`."
)


def _de_betrag(wert: float) -> str:
    """Formatiert einen Geldbetrag in deutscher Schreibweise (Punkt als
    Tausender-, Komma als Dezimaltrennzeichen, zwei Nachkommastellen).

    Entscheidung des CEO vom 20.09.2026: Jedes Dokument, das das Haus
    verlässt oder einer Kommune vorgelegt wird, nutzt deutsche
    Zahlenschreibweise.
    """
    return f"{wert:,.2f}".replace(",", "⁣").replace(".", ",").replace("⁣", ".")


def _tabelle_betroffene_handlungsfelder(handlungsfelder: list[dict]) -> str:
    zeilen = [
        "| Cluster | Handlungsfeld | Status | Risiken | Schaden p.a. (EUR) | Maßnahmen |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for eintrag in handlungsfelder:
        if eintrag["status"] == "nicht betroffen":
            continue
        risiken = ", ".join(eintrag["risiken"]) or "—"
        massnahmen = ", ".join(eintrag["massnahmen"]) or "—"
        zeilen.append(
            "| {cluster} | {feld} | {status} | {risiken} | {schaden} | {massnahmen} |".format(
                cluster=eintrag["cluster"],
                feld=eintrag["feld"],
                status=eintrag["status"],
                risiken=risiken,
                schaden=_de_betrag(eintrag["schaden_eur"]),
                massnahmen=massnahmen,
            )
        )
    return "\n".join(zeilen)


def _tabelle_offene_handlungsfelder(offene_handlungsfelder: list[dict]) -> str:
    zeilen = [
        "| Cluster | Handlungsfeld |",
        "| --- | --- |",
    ]
    for eintrag in offene_handlungsfelder:
        zeilen.append("| {cluster} | {feld} |".format(
            cluster=eintrag["cluster"], feld=eintrag["feld"],
        ))
    return "\n".join(zeilen)


def _integrierende_massnahmen(massnahmen_codes: list[str]) -> str:
    if not massnahmen_codes:
        return "Keine Maßnahme der Planung setzt an mehr als einem Handlungsfeld an."
    return "\n".join(f"- {code}" for code in massnahmen_codes)


def nachweis_markdown(nachweis: dict) -> str:
    """Formatiert den Nachweis aus ``nachweis_fachuebergreifend`` als Markdown.

    ``nachweis`` ist das Rückgabe-dict von
    ``app.services.kang_beruecksichtigung.nachweis_fachuebergreifend`` mit den
    Schlüsseln ``handlungsfelder``, ``zusammenfassung`` und ``abgrenzung``.

    Rückgabe: ein Markdown-Dokument mit den Abschnitten 'Betroffene
    Handlungsfelder' (eine Tabellenzeile je Eintrag mit Status ungleich
    'nicht betroffen'), 'Offene Handlungsfelder' (eine Tabellenzeile je Eintrag
    aus ``zusammenfassung['offene_handlungsfelder']``), 'Integrierende
    Maßnahmen' und 'Abgrenzung' (Volltext von ``nachweis['abgrenzung']``).
    Geldbeträge stehen in deutscher Zahlenschreibweise (Punkt als Tausender-,
    Komma als Dezimaltrennzeichen); das Dokument verweist auf die
    Methodenbeschreibung ``docs/NACHWEIS_FACHUEBERGREIFEND_KANG.md``.
    """
    handlungsfelder = nachweis["handlungsfelder"]
    zusammenfassung = nachweis["zusammenfassung"]
    abgrenzung = nachweis["abgrenzung"]

    teile = [
        TITEL,
        "",
        (
            "Betroffene Handlungsfelder: {betroffen_n}, davon berücksichtigt: "
            "{beruecksichtigt_n}, offen: {offen_n}."
        ).format(**zusammenfassung),
        "",
        METHODENVERWEIS,
        "",
        "## Betroffene Handlungsfelder",
        "",
        _tabelle_betroffene_handlungsfelder(handlungsfelder),
        "",
        "## Offene Handlungsfelder",
        "",
        _tabelle_offene_handlungsfelder(zusammenfassung["offene_handlungsfelder"]),
        "",
        "## Integrierende Maßnahmen",
        "",
        _integrierende_massnahmen(zusammenfassung["integrierende_massnahmen"]),
        "",
        "## Abgrenzung",
        "",
        abgrenzung,
        "",
    ]
    return "\n".join(teile)

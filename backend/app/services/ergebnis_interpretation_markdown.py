"""Interpretationsbericht als Markdown (Konformitätszeile 19, A8; T-1141, Vorhaben T-1010).

UBA-Broschüre „Klimarisikoanalysen auf kommunaler Ebene“, Abschnitt 2.2.6, S. 30:
„Der priorisierte Handlungsbedarf … ist die Grundlage für eine Maßnahmenplanung.“
Der Bericht bündelt die Interpretationsbelege einer Kommune in genau sieben festen
Abschnitten in dieser Reihenfolge:

1. ``Leitfragen`` — ``data.kra_leitfragen`` (A1),
2. ``Unsicherheit der Daten`` — ``unsicherheits_zusammenschau`` (A2),
3. ``Abhängigkeiten über Handlungsfelder`` — ``handlungsfeld_abhaengigkeiten`` (A4),
4. ``Nachbarkommunen`` — ``nachbarkommunen_screening`` (A5),
5. ``Handlungsbedarf und Handlungsoptionen`` — ``charakterisierung.charakterisierungen``,
   ``massnahmen_gewissheit`` und ``data.massnahmen_umsetzung`` (A3, A8, A9),
6. ``Gender und Diversität`` — ``data.diversitaet_aspekte`` (A7),
7. ``Einbeziehung`` — ``ergebnis_nachweise`` (A6, A10).

Es wird nichts neu gerechnet (Muster ``kurzfassung_markdown``): Dieses Modul wählt aus
und formatiert. Bewusst nicht enthalten:

- eine Priorisierung aus Klimarisiko und Anpassungsdauer — das ist eine fachliche
  Festlegung des CMO (Zeile 6, Anmerkung M-0005); der Bericht sagt, dass sie fehlt;
- Euro-Beträge (Vorgabe P2);
- jede Einbeziehung ohne Nachweis: Fehlt ein Eintrag, steht dort ``nicht erfasst``.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from app.data import catalog
from app.data.kra_leitfragen import NICHT_BEANTWORTET

if TYPE_CHECKING:  # nur für die Typangabe; der Formatter läuft ohne Datenbank
    from sqlalchemy.orm import Session

UEBERSCHRIFTEN = (
    "Leitfragen",
    "Unsicherheit der Daten",
    "Abhängigkeiten über Handlungsfelder",
    "Nachbarkommunen",
    "Handlungsbedarf und Handlungsoptionen",
    "Gender und Diversität",
    "Einbeziehung",
)

SATZ_KEINE_PRIORISIERUNG = (
    "Es liegt keine aus Klimarisiko und Anpassungsdauer hergeleitete Priorisierung vor; "
    "wie der Handlungsbedarf daraus gereiht wird, ist noch nicht festgelegt. Die "
    "Charakterisierungsgruppe unten ordnet die Klimawirkungen ein, reiht sie aber nicht."
)

UMSETZUNG_TEXT = {
    "kommune_allein": "Kommune allein",
    "mit_partnern": "mit Partnern",
}

EBENE_TEXT = {"gemeinde": "Gemeinde", "kreis": "Landkreis", "land": "Land"}


def _datum(wert) -> str:
    """Datum im Text als TT.MM.JJJJ (Stil KAP3)."""
    if isinstance(wert, date):
        return wert.strftime("%d.%m.%Y")
    return str(wert)


def _zahl(wert) -> str:
    """Zahl mit Dezimalkomma, höchstens eine Nachkommastelle."""
    if wert is None:
        return "—"
    return f"{wert:.1f}".replace(".", ",")


def _name(code: str) -> str:
    return (catalog.RISKS_BY_CODE.get(code) or {}).get("name", code)


def _abschnitt_leitfragen(leitfragen: list[dict]) -> str:
    zeilen = [
        "Die Leitfragen stammen aus der UBA-Broschüre „Klimarisikoanalysen auf kommunaler "
        "Ebene“ (2022). Je Frage steht, ob das Produkt sie für die Kommune beantwortet.",
        "",
    ]
    for f in leitfragen:
        if f["beantwortet_durch"] == NICHT_BEANTWORTET:
            stand = "nicht beantwortet"
        else:
            stand = f"beantwortet in: {f['stelle_im_produkt']}"
        zeilen.append(
            f"{f['nr']}. {f['wortlaut']} (S. {f['seite']}) — {stand}. {f['begruendung']}"
        )
    return "\n".join(zeilen)


def _abschnitt_unsicherheit(zusammenschau: dict) -> str:
    zeilen = [
        "| Handlungsfeld | Niedrigste Gewissheit | Parameter ohne Beleg | "
        "Klimawirkungen mit dieser Gewissheit |",
        "| --- | --- | --- | --- |",
    ]
    for e in zusammenschau["handlungsfelder"]:
        namen = ", ".join(_name(c) for c in e["klimawirkungen_niedrigste_stufe"])
        zeilen.append(
            f"| {e['handlungsfeld']} | {e['niedrigste_gewissheit']} | "
            f"{e['parameter_nicht_belegt']} | {namen} |"
        )
    text = "\n".join(zeilen)
    if zusammenschau.get("hinweis"):
        text += "\n\n" + zusammenschau["hinweis"]
    return text


def _abschnitt_abhaengigkeiten(abhaengigkeiten: list[dict]) -> str:
    zeilen = [
        "Genannt sind nur die Beziehungen, die die KWRA 2021 (Teilbericht 6, Kapitel 3.4) "
        "benennt. Wie stark eine Abhängigkeit wirkt, ist nicht bewertet.",
    ]
    for e in abhaengigkeiten:
        zeilen += ["", f"**{e['name']}** (Handlungsfeld {e['handlungsfeld'] or '—'})", ""]
        if e["andere_handlungsfelder"]:
            zeilen.append("Weitere Handlungsfelder: " + ", ".join(e["andere_handlungsfelder"]) + ".")
        else:
            zeilen.append("Keine benannte Beziehung in ein anderes Handlungsfeld.")
        for b in e["beziehungen"]:
            if b["wirkt_auf_partner"] and b["partner_wirkt_ein"]:
                richtung = "wechselseitig"
            elif b["wirkt_auf_partner"]:
                richtung = "wirkt auf"
            else:
                richtung = "wird beeinflusst von"
            feld = b["partner_handlungsfeld"] or "Handlungsfeld nicht geführt"
            zeilen.append(f"- {richtung}: {b['partner_name']} ({feld})")
    return "\n".join(zeilen)


def _abschnitt_nachbarkommunen(nachbarkommunen: list[dict]) -> str:
    zeilen = [
        "Screening-Index 0–100, bundesweit normiert, je Klimawirkung für die eigene "
        "Gemeinde und die angrenzenden Gemeinden. Die Werte sind aufgelistet, nicht "
        "verdichtet.",
        "",
    ]
    for e in nachbarkommunen:
        if not e["index_vorhanden"]:
            zeilen.append(f"- {e['name']}: kein Screening-Index vorhanden.")
            continue
        nachbarn = "; ".join(
            f"{n['name']} {_zahl(n['index'])}" for n in e["nachbarn"]
        ) or "keine angrenzende Gemeinde gefunden"
        zeilen.append(
            f"- {e['name']}: eigene Gemeinde {_zahl(e['eigener_index'])}; Nachbarn: {nachbarn}"
        )
    if not nachbarkommunen:
        zeilen.append("Für diese Kommune liegen keine Screening-Werte vor.")
    return "\n".join(zeilen)


def _umsetzung(eintrag: dict | None) -> str:
    if not eintrag:
        return "Umsetzungsebene nicht hinterlegt"
    text = UMSETZUNG_TEXT.get(eintrag["umsetzung"], eintrag["umsetzung"])
    ebenen = ", ".join(EBENE_TEXT.get(e, e) for e in eintrag.get("ebenen") or [])
    return f"{text} (Ebenen: {ebenen})" if ebenen else text


def _abschnitt_handlungsbedarf(
    charakterisierungen: dict[str, dict],
    massnahmen: list[dict],
    umsetzung: dict[str, dict],
) -> str:
    zeilen = [SATZ_KEINE_PRIORISIERUNG]
    for code, c in charakterisierungen.items():
        zeilen += [
            "",
            f"**{_name(code)}** — Charakterisierungsgruppe „{c['gruppe']}“ "
            f"(Gewissheit {c['gewissheit']}, Anpassungspotenzial "
            f"{_zahl(c['anpassungspotenzial'] * 100)} %)",
            "",
        ]
        verknuepft = [
            (m, k) for m in massnahmen for k in m["klimawirkungen"] if k["code"] == code
        ]
        if not verknuepft:
            zeilen.append("Keine Maßnahme im Katalog verknüpft.")
            continue
        zeilen += [
            "| Maßnahme | Umsetzungsebene | Gewissheit der Klimawirkung | Evidenz der Wirkung |",
            "| --- | --- | --- | --- |",
        ]
        for m, k in verknuepft:
            evidenz = "nur qualitativ verknüpft" if k["qualitativ"] else m["wirkung_evidenz"]
            zeilen.append(
                f"| {m['name']} | {_umsetzung(umsetzung.get(m['code']))} | "
                f"{k['gewissheitsstufe']} | {evidenz} |"
            )
    return "\n".join(zeilen)


def _abschnitt_diversitaet(diversitaet: dict[str, dict], codes) -> str:
    zeilen = [
        "Je Klimawirkung, welche Merkmale von Personengruppen in die Rechnung eingehen "
        "und welche nicht (UBA-Broschüre 2022, S. 30).",
    ]
    for code in codes:
        eintrag = diversitaet.get(code)
        zeilen += ["", f"**{_name(code)}**", ""]
        if not eintrag:
            zeilen.append("Keine Angabe hinterlegt.")
            continue
        for a in eintrag.get("beruecksichtigt") or []:
            zeilen.append(f"- berücksichtigt: {a['aspekt']} — {a['wie']}")
        for a in eintrag.get("nicht_beruecksichtigt") or []:
            zeilen.append(f"- nicht berücksichtigt: {a['aspekt']}")
    return "\n".join(zeilen)


def _abschnitt_einbeziehung(nachweise: list[dict]) -> str:
    zeilen = [
        "Welche Stellen die Ergebnisse gelesen haben, mit Datum. Die Software nennt nur "
        "erfasste Nachweise.",
        "",
    ]
    for n in nachweise:
        if not n["eintraege"]:
            zeilen.append(f"- {n['bezeichnung']}: {n['status']}")
            continue
        liste = "; ".join(
            f"{e['stelle']} am {_datum(e['datum'])}"
            + (f" ({e['vermerk']})" if e.get("vermerk") else "")
            for e in n["eintraege"]
        )
        zeilen.append(f"- {n['bezeichnung']}: {liste}")
    return "\n".join(zeilen)


def interpretationsbericht_markdown(name: str, daten: dict) -> str:
    """Formatiert den Interpretationsbericht aus den unveränderten Dienstergebnissen.

    ``daten`` enthält die Schlüssel ``leitfragen`` (``LEITFRAGEN``), ``unsicherheit``
    (``unsicherheits_zusammenschau``), ``abhaengigkeiten`` (``abhaengigkeiten_der_kommune``),
    ``nachbarkommunen`` (``nachbar_screening_fuer_kommune``), ``charakterisierungen``
    (``charakterisierung.charakterisierungen``), ``massnahmen_gewissheit``,
    ``massnahmen_umsetzung`` (``MASSNAHMEN_UMSETZUNG``), ``diversitaet``
    (``DIVERSITAET_JE_KLIMAWIRKUNG``) und ``nachweise`` (``ergebnis_nachweise.nachweise``).
    """
    inhalte = (
        _abschnitt_leitfragen(daten["leitfragen"]),
        _abschnitt_unsicherheit(daten["unsicherheit"]),
        _abschnitt_abhaengigkeiten(daten["abhaengigkeiten"]),
        _abschnitt_nachbarkommunen(daten["nachbarkommunen"]),
        _abschnitt_handlungsbedarf(
            daten["charakterisierungen"], daten["massnahmen_gewissheit"],
            daten["massnahmen_umsetzung"],
        ),
        _abschnitt_diversitaet(daten["diversitaet"], list(daten["charakterisierungen"])),
        _abschnitt_einbeziehung(daten["nachweise"]),
    )
    teile = [f"# Interpretation der Ergebnisse: {name}", ""]
    for ueberschrift, inhalt in zip(UEBERSCHRIFTEN, inhalte):
        teile += [f"## {ueberschrift}", "", inhalt, ""]
    return "\n".join(teile)


def interpretationsbericht_fuer_kommune(db: Session, kommune) -> str:
    """Holt die Ergebnisse der vorhandenen Dienste und formatiert den Bericht."""
    from app.data.diversitaet_aspekte import DIVERSITAET_JE_KLIMAWIRKUNG
    from app.data.kra_leitfragen import LEITFRAGEN
    from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
    from app.services import charakterisierung, ergebnis_nachweise
    from app.services.handlungsfeld_abhaengigkeiten import abhaengigkeiten_der_kommune
    from app.services.massnahmen_gewissheit import massnahmen_gewissheit
    from app.services.nachbarkommunen_screening import nachbar_screening_fuer_kommune
    from app.services.unsicherheits_zusammenschau import unsicherheits_zusammenschau

    daten = {
        "leitfragen": LEITFRAGEN,
        "unsicherheit": unsicherheits_zusammenschau(kommune.id),
        "abhaengigkeiten": abhaengigkeiten_der_kommune(),
        "nachbarkommunen": nachbar_screening_fuer_kommune(db, kommune),
        "charakterisierungen": charakterisierung.charakterisierungen(),
        "massnahmen_gewissheit": massnahmen_gewissheit(),
        "massnahmen_umsetzung": MASSNAHMEN_UMSETZUNG,
        "diversitaet": DIVERSITAET_JE_KLIMAWIRKUNG,
        "nachweise": ergebnis_nachweise.nachweise(db, kommune.id),
    }
    return interpretationsbericht_markdown(kommune.name, daten)

"""Test des Katalogs der Bestandsaufnahme-Größen (Ticket T-0754, Vorhaben T-0447).

Deckt ab: (a) 15 Codes in fester Reihenfolge, (b) Gruppe/Label/Einheit wie im Ticket,
(c) je Größe Quellschlüssel (im Register) XOR Lückensatz, (d) Lückensätze wörtlich.
"""

from __future__ import annotations

from app.data import bestandsaufnahme as b
from app.data.sources import SOURCE_REFERENCES

CODES = [
    "aeltere_ab_65", "kinder_unter_18", "arbeitslosenquote", "pflegebeduerftige",
    "alleinlebende_aeltere", "vorerkrankte", "wohnungslose", "energie",
    "wasser_abwasser", "verkehrsknoten", "kommunikation", "krankenhaeuser",
    "pflegeeinrichtungen", "kitas_schulen", "schadensereignisse",
]
VP, KS, VE = "vulnerable_personen", "klimasensible_strukturen", "vergangene_ereignisse"
TABELLE = {
    "aeltere_ab_65": (VP, "Ältere Menschen ab 65 Jahren", "%"),
    "kinder_unter_18": (VP, "Kinder und Jugendliche unter 18 Jahren", "%"),
    "arbeitslosenquote": (VP, "Arbeitslose (Arbeitslosenquote)", "%"),
    "pflegebeduerftige": (VP, "Pflegebedürftige Menschen", ""),
    "alleinlebende_aeltere": (VP, "Alleinlebende ältere Menschen", ""),
    "vorerkrankte": (VP, "Menschen mit Vorerkrankungen", ""),
    "wohnungslose": (VP, "Wohnungslose Menschen", ""),
    "energie": (KS, "Energieinfrastruktur", "Vorkommen"),
    "wasser_abwasser": (KS, "Wasser- und Abwasserinfrastruktur", "Vorkommen"),
    "verkehrsknoten": (KS, "Verkehrsknoten", "Vorkommen"),
    "kommunikation": (KS, "Kommunikationsinfrastruktur", "Vorkommen"),
    "krankenhaeuser": (KS, "Krankenhäuser", "Anzahl"),
    "pflegeeinrichtungen": (KS, "Pflegeeinrichtungen", "Anzahl"),
    "kitas_schulen": (KS, "Kindertagesstätten und Schulen", ""),
    "schadensereignisse": (VE, "Vergangene Schadensereignisse durch Wetterextreme", ""),
}
LUECKEN = {"pflegebeduerftige", "alleinlebende_aeltere", "vorerkrankte",
           "wohnungslose", "kitas_schulen", "schadensereignisse"}


def test_codes_und_reihenfolge():
    assert [g["code"] for g in b.BESTANDSAUFNAHME_GROESSEN] == CODES


def test_gruppe_label_einheit():
    for g in b.BESTANDSAUFNAHME_GROESSEN:
        assert (g["gruppe"], g["label"], g["einheit"]) == TABELLE[g["code"]]


def test_quelle_xor_luecke():
    for g in b.BESTANDSAUFNAHME_GROESSEN:
        assert bool(g["quellen"]) != bool(g["luecke"]), g["code"]
        for q in g["quellen"]:
            assert q in SOURCE_REFERENCES, q


def test_luecken_woertlich():
    gefunden = {g["code"] for g in b.BESTANDSAUFNAHME_GROESSEN if g["luecke"]}
    assert gefunden == LUECKEN
    for g in b.BESTANDSAUFNAHME_GROESSEN:
        if g["code"] in LUECKEN:
            assert g["luecke"] == (
                f"Für die Größe {g['label']} liegt dem Produkt keine Datenquelle je "
                "Kommune vor; sie ist im Rahmen der Konzepterstellung vor Ort zu erheben."
            )


def test_laufzeitsatz():
    assert b.LAUFZEITSATZ_VORLAGE.format(label="X") == (
        "Für die Größe X war die Datenquelle für diese Kommune nicht abrufbar; "
        "der Wert fehlt in dieser Bestandsaufnahme."
    )

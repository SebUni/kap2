# Ebene POLLEN_LOAD: Ĝ-Streuung und kommunale Referenz Ḡ (#96 §3.3)

Plausibilisierung der Ebene mit dem Produktionsmodell je Kommune.
**Ḡ ist kein Parameter**: Das Produkt bildet die Referenz seit Rev. 2 im
Lauf aus den Zellen der jeweiligen Kommune (Aufgabe §3.2, geschlossene
Betrachtungsebene); die Tabelle zeigt, wie stark Ĝ zwischen
Siedlungstypen streut und dass die Referenz nachrechenbar ist.

| Kommune | Typ | bewohnte Zellen | Betroffene | Ḡ | Median Ĝ |
|---|---|---|---|---|---|
| Weyarn | Landgemeinde, grünreich (Süd) | 308 | 428 | 0.27041 | 0.32322 |
| Offenbach am Main | Großstadt, dicht bebaut (Mitte) | 1480 | 14610 | 0.17401 | 0.18714 |
| Freising | Mittelstadt (Süd) | 1108 | 5369 | 0.17965 | 0.18956 |

- Streuung der kommunalen Referenzen: **0.1740 … 0.2704** (Stichproben-Mittel 0.1775 — nur Kennzahl, kein Modellparameter)
- Erwartete Richtung bestätigt: dicht bebaute Städte niedrig, ländlich-
  grüne Gemeinden hoch — die Ebene misst, was sie soll.
- KEIN eingefrorener Referenzzustand (Bericht Log 19): Ḡ wird in jedem
  Lauf aus dem aktuellen Vegetationszustand der Kommune gebildet. Ein
  Pinning würde einem flächigen Programm einen Niveaueffekt zubuchen,
  den die intra-urbane λ-Evidenz nicht trägt (Modellgrenze 7).

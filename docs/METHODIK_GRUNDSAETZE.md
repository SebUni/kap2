# Methodik-Grundsätze für Schadensrechnungen (risikounabhängig)

Destillat aus den Methodik-Reviews 1–3 (Aug. 2026, M0-Gesundheitsrisiken). Diese Regeln gelten
für **jedes** Risiko, das neu in Schicht B (absolute Schadensfunktionen) aufgenommen wird —
sie haben nichts mit #95/#96/#98 im Besonderen zu tun und werden hier fortgeschrieben.
Anwendungsbeispiele: `docs/METHODIK_M0_GESUNDHEIT.pdf`, Kap. 2–4 (die Grundsätze werden dort je Risiko konkret umgesetzt; §1.6 des Berichts verweist nur hierher).

## G1 — Bottom-up statt Verteilschlüssel

Lokale Treiber (Zellklima, Bevölkerung, Bestand) bestimmen den Wert jeder Zelle. Bundes- oder
Landesstatistik geht **ausschließlich als Kalibrier-/Sanity-Anker** ein — als ein einziger Skalar
auf die Deutschland-Summe, nie als Verteilungsschlüssel. Lackmustest: *Eine Kommune ohne Treiber
muss ~0 erhalten* (keine Flussaue → keine Flutopfer, kein Hitzesignal → keine Hitzetoten).
Ansätze der Form „nationaler Topf × Anteil" scheiden aus.

## G2 — Mortalität als YLL × VOLY

Verlorene Lebensjahre × Wert eines Lebensjahres (Methodik der UBA-MK 4.0), Todesfälle je
Altersband nur als interne Zwischengröße; der VSL-Weg bleibt dokumentierte Sensitivität.
Konsequenz beachten: YLL bewertet altersabhängig und ist bei altenlastigen Risiken ~Faktor 5–10
konservativer als VSL — die Relation zwischen Risiken verschiebt sich; das gehört kommuniziert (G8).
Konsistenz-Check der Setzungen: VSL ÷ VOLY ≈ plausible Lebensjahre — beide aus derselben Quelle mit
derselben Anpassung herleiten (z. B. MK-4.0-Paar 6,19 Mio € ÷ 160,8 T€ ≈ 38 LJ).

## G3 — Altersstruktur überall, wo die Evidenz altersabhängig ist

Nicht nur die Mortalität: auch Morbidität/Inzidenz altersspezifisch rechnen (Raten je Altersband),
sonst systematische Fehlverteilung zwischen alterndem ländlichem Raum und junger Innenstadt.
Wo Elastizitäten (z. B. je Hitzetag) nicht altersgeschichtet publiziert sind: Annahme „gleiche
relative Elastizität über alle Bänder" explizit dokumentieren.

## G4 — Nur empirisch belegte Sensitivitäten in den Absolutwert

Statt generischer 0–1-Indizes: messbare Größen mit publizierter Effektgröße und Spanne
(Distanz in km, Anteil Einpersonenhaushalte, Heimbewohner-Anteil, Außenberufs-Anteil …).
Unbelegte Modulatoren stehen im Default auf neutral (= 1) und existieren nur als dokumentierte
Maßnahmen-Hebel oder Sensitivitätsband. Schwache Effekte ehrlich als schwach kennzeichnen
(nicht als „Versorgungsdimension" verkaufen).

## G5 — Gemessene statt gesetzte Parameter, regional variiert

Wo ein Parameter messbar ist, wird er aus Daten geschätzt statt gesetzt (Streuungen aus
DWD-Klimatologien, Übersetzungsfaktoren aus Messreihen, Kalibrierfaktoren per Kleinste-Quadrate
gegen die Anker-Zeitreihe). Regional differenzieren, wo die Datenlage es trägt.

## G6 — Schlüsselgrößen als Kartenebenen, Ergebnisse als lesbare Raten

Jede zentrale Zwischengröße der Rechnung ist eine eigene Produkt-Ebene (Transparenz).
Ergebnis-Layer als **Rate je 1.000 Einwohner** bzw. je Hektar darstellen — Rohwerte je 100-m-Zelle
(„0,018 Todesfälle") sind unlesbar und wirken unseriös; zusätzlich eine aggregierte Ebene
(Quartier/Gemeindeteil) für die Summenkommunikation.

## G7 — Nachvollziehbarkeit als Form

LaTeX-Formeln; je Formel eine **alphabetisch sortierte** Formelzeichen-Tabelle
(Zeichen · Name · Einheit · Wert/Herkunft); Abkürzungen bei Erstnutzung erklären; jede Summe/
Verteilung in Klartext erklären, wo hilfreich mit Mini-Rechenbeispiel (Zahlen, keine Prosa).
Kernformel-Lesart: **Menge × Rate × Preis** — zwischen Klimasignal und € steht immer eine
physische Größe, die sich unabhängig gegen amtliche Statistik plausibilisieren lässt
(Beweislastregel; das unterscheidet Schicht B von einem Kostentopf).

## G8 — Abgrenzungen fest verdrahten, nicht disclaimen

1. **Benennung:** Teilsummen heißen im UI nach ihrem Geltungsbereich („bewerteter Schaden —
   Konto K1 Gesundheit"), nie „Gesamtschaden".
2. **Vollständigkeitsanzeige:** sichtbar „Stufe M0: 1 von 8 Schadenskonten aktiv" mit
   Aufklappliste, welches Konto mit welcher Roadmap-Stufe folgt.
3. **Versionsstempel am Ergebnis:** „berechnet mit Modellstand M0 (Untergrenze)" — Werte werden
   in Beschlussvorlagen zitiert und springen bei Stufenwechseln.

## G9 — Modifikatoren mittelwertzentriert; OR korrekt übersetzen

Jeder multiplikative Modifikator ist so zentriert, dass das **Bundesmittel = 1** bleibt
(`1 + β·(x − x̄)`), sonst verschiebt er das nationale Niveau, der Kalibrierfaktor fängt es ein
und niemand weiß mehr, was der Kalibrierfaktor korrigiert. Individuelle Odds-Ratios werden über
das Bevölkerungsmittel in Zellanteils-Steigungen übersetzt:

```
RR(Zelle) = [1 + q·(OR−1)] / [1 + q̄·(OR−1)]   ⇒   β = (OR−1) / [1 + q̄·(OR−1)]
```

(Der individuelle OR direkt als Steigung wäre um den Nenner zu hoch.)

## G10 — Maßnahmen mit Interventionsevidenz bewerten

Fall-Kontroll-Odds-Ratios („Verstorbene vs. Überlebende unterschieden sich in X") messen nicht
die Wirkung einer **Einführung** von X — Interventions-/quasi-experimentelle Studien sind
regelmäßig um Faktor 5–10 nüchterner. Für jeden Maßnahmen-Hebel außerdem der
**Doppelzählungs-Wächter:** Ist der Durchschnittseffekt der Maßnahme bereits in den
Kalibrierjahren des Basiswerts enthalten (z. B. laufende Warnsysteme)? Dann bewertet der Hebel
nur den *marginalen* Zusatzeffekt.

## G11 — Verteilungs-Tails ernst nehmen

Wo wenige Extremwochen/-ereignisse fast den ganzen Effekt tragen (typisch: 3 von 13 Wochen ≈ 90 %),
empirische Quantile aus der Klimatologie statt Verteilungsannahmen verwenden — Gauß unterschätzt
rechte Schwänze systematisch, und ein Fehler im Schwanz schlägt ~1:1 auf das Ergebnis durch.
Dabei die **intra-saisonale** Streuung schätzen, nicht die zwischenjährliche (falsche Größe).

## G12 — Kalibrierung ist kein Verteilungsnachweis

Ein globaler Anker-Skalar korrigiert das *Niveau*, nicht *Verteilungsfehler*. Die räumliche und
strukturelle Verteilung braucht **unabhängige Prüfungen auf der kritischsten Achse** des Modells —
z. B. Altersverteilung gegen publizierte Verteilungen und Anker auf beiden Seiten des
Stadt-Land-Gradienten (urban UND ländlich), wenn das Modell UHI-getrieben ist.

## G13 — Keine Wirkung über zwei Kanäle

Jede physikalische Wirkung geht genau einmal ins Modell ein. Beispiel: Grün-/Baumkronenanteil
steckt im UHI-Zuschlag der Zelltemperatur — ihn zusätzlich als „Vulnerabilität" zu führen, wäre
Doppelzählung derselben Wirkung. Vor Aufnahme jedes Faktors prüfen, ob er bereits implizit in
einem anderen Eingang enthalten ist (gleiches Prinzip wie die Mittelwerttreue gegen das DWD-Raster).

## G14 — Herleitungspflicht für jeden Parameter

Kein Formelzeichen ohne abgeschlossene Herleitung **im Bericht selbst** — unabhängig davon, ob
der Wert übernommen, abgeleitet, gemessen oder abgeschätzt ist: Fundstelle + Umrechnung, oder
komplette Rechenkette mit Zwischenwerten, oder Datensatz + Aggregationsregel + Ergebnis, oder
(nur wenn keine Quelle existiert) begründete Abschätzung mit Bandbreite und Sensitivität.
Unzulässig sind Platzhalter, „wird bei Implementierung hergeleitet", „schätzen wir aus X ab"
ohne die Abschätzung, und Modifikatoren, deren Herkunft niemand benennen kann. Das gilt auch
für Defaults, Bandgrenzen, Zentrierungs-Mittelwerte und Kostensätze. Prüfregel: Jede Zeile
der Zeichentabelle muss in „Wert/Herkunft" auf eine fertige Herleitung zeigen, nie auf später.

---

## Checkliste für jedes neue Schicht-B-Risiko

1. Wirkungskette strikt aus der Schadensbaum-Arbeitsmappe; Konto + R9-Abgrenzung benennen (was ist
   bewusst NICHT enthalten, wo bucht es stattdessen).
2. Bottom-up-Formel: Menge (Zelle) × Rate (Wirkungsfunktion) × Preis (Konto) — physische
   Zwischengröße benennen und gegen amtliche Statistik plausibilisieren (G1/G7).
3. Altersstruktur prüfen (G3); Mortalität als YLL (G2).
4. Sensitivitäten: nur belegte, zentriert, OR korrekt übersetzt (G4/G9); Doppelkanal-Check (G13).
5. Parameter messen statt setzen, regional (G5); Tails empirisch (G11).
6. Kalibrieranker + mindestens eine unabhängige Verteilungsprüfung auf der kritischen Achse (G12).
7. Maßnahmen-Hebel: Interventionsevidenz, marginal, Doppelzählungs-Wächter (G10).
8. Kartenebenen + Raten-Darstellung (G6); UI-Abgrenzungen (G8).
9. Jede Zahl mit Quelle (Ratchet); Effektgrößen aus Sekundärfunden vor Übernahme im Volltext
   verifizieren.
10. Herleitungspflicht: kein Formelzeichen ohne vollständige Herleitung im Bericht — keine
    Platzhalter, keine „später"-Verweise (G14).

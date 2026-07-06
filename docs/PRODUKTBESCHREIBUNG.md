# KAP2 — Produktbeschreibung

**Klimawirkungs- und Risikoanalyse (KWRA) und Anpassungsplanung für Kommunen**

*Stand: Juli 2026 · Umfang: Zweiseiter · Abschnitt 6 ist ausschließlich für den internen Gebrauch bestimmt.*

---

## 1. Kurzprofil

KAP2 ist eine Software für die vollständige Klimawirkungs- und Risikoanalyse deutscher Kommunen — von der automatischen Datenerhebung über die räumliche Risikobewertung auf dem 100-Meter-Raster bis zur priorisierten Anpassungsplanung mit Kosten und Nutzen in Euro. Die Analyse erfüllt die methodischen Anforderungen der DIN EN ISO 14091, der Klimawirkungs- und Risikoanalyse des Bundes (KWRA 2021, UBA) und der UBA-Empfehlungen für kommunale Klimarisikoanalysen. Damit liefert KAP2 Kommunen die fachliche Grundlage, die das Bundes-Klimaanpassungsgesetz (KAnG) von den Ländern und Kommunen verlangt — und die Voraussetzung für Förderprogramme der Deutschen Anpassungsstrategie (DAS-Förderung, ANK) ist.

Was KAP2 von allen bekannten Angeboten unterscheidet: **Es vereint beides.** Die Risikoanalyse folgt der KWRA-Systematik des Bundes — relative Risikobewertung über Wirkungsketten, vergleichbar und anschlussfähig. Die KWRA selbst liefert jedoch keine Geldwerte. KAP2 ergänzt sie deshalb um eine eigene Schadensfunktionsschicht, die die Risiken zusätzlich als absolute Größen abschätzt: erwartete Jahresschäden in Euro, je Risiko, je Ortsteil, mit und ohne Anpassungsmaßnahmen. Aus „hohes Hitzerisiko" wird so greifbar: „X Mio. € erwarteter Schaden pro Jahr". Grundlage dafür: Jede Zahl ist belegt — jeder Modellparameter ist einsehbar, mit zitierfähiger Quelle hinterlegt und kommunenspezifisch anpassbar; ein Herkunftsgraph zeigt den vollständigen Rechenweg vom Rohdatum bis zur Kennzahl. So ist die Analyse prüfbar — durch Gemeinderat, Fördermittelgeber und Fachöffentlichkeit.

## 2. Was KAP2 leistet

**Automatischer Datenbezug.** Für jede deutsche Kommune (Auswahl per Suche, amtliche Gebietsgrenze) bezieht KAP2 selbstständig die erforderlichen Daten aus amtlichen und offenen Quellen: Zensus 2022 (Bevölkerung und Sozialstruktur im 100-m-Gitter), Klimaraster des Deutschen Wetterdienstes (DWD CDC), Pegeldaten der Wasserstraßen- und Schifffahrtsverwaltung (PEGELONLINE), Copernicus/ERA5-Klimatologien, digitales Höhenmodell, OpenStreetMap (Gebäude, Infrastruktur, Landnutzung) und BBSR-INKAR-Indikatoren. Es ist keine eigene Datenbeschaffung durch die Kommune nötig.

**Risikoanalyse nach KWRA-Logik.** KAP2 bewertet auf jeder 100-m-Rasterzelle das Zusammenwirken von 23 Klimagefahren, 24 Expositionen und 33 Vulnerabilitätsindikatoren entlang kuratierter Wirkungsketten (Gefährdung × Exposition × Vulnerabilität). Das Ergebnis sind 47 Klimarisiken in den fünf Risikofeldern der KWRA — Hitze, Trockenheit & Niedrigwasser, Hochwasser & Starkregen, Gradueller Wandel, Verbund- & Kaskadenrisiken — jeweils als Risiko-Index je Zelle, als Hotspot-Zonen auf der Karte und als kommunale Gesamtkennzahl.

**Ergebnisse in Euro — der Kern von KAP2.** Über die KWRA hinaus schätzt eine eigene Schadensfunktionsschicht die Risiken als absolute Geldwerte ab — mit anerkannten Verfahren der Klimaschadens-Ökonomie: Gesundheitsfolgen über Kostensätze (u. a. Wert eines statistischen Lebens), Gebäude- und Infrastrukturschäden über Schadensfunktionen und Jahresverlustraten, Versorgungsausfälle über Ausfallkosten, Umweltschäden über Ökosystemleistungswerte. Eine Projektion zeigt die Risikoentwicklung 2025–2065 unter den Klimaszenarien RCP 4.5 und RCP 8.5. Damit sprechen die Ergebnisse die Sprache von Kämmerei und Rat — nicht nur Ampelfarben, sondern Beträge.

**Anpassungsplanung mit Kosten-Nutzen-Rechnung.** Aus einem Katalog von 47 Anpassungsmaßnahmen — gegliedert nach den Handlungsfeldern des KAnG, von Entsiegelung und Gründächern über Retentionsflächen bis zu Hitzeaktionsplänen — werden Maßnahmen direkt auf der Karte verortet. KAP2 berechnet je Maßnahme Investitions- und Betriebskosten (CAPEX/OPEX) sowie den Nutzen als vermiedene Schäden und stellt die Gesamtkosten der Kommune mit und ohne Maßnahmen gegenüber. So entsteht eine belastbare Priorisierung: welche Maßnahme wirkt wo am meisten pro eingesetztem Euro.

**Nachvollziehbarkeit als Grundlage.** Damit die Euro-Zahlen belastbar sind: Alle Modellparameter (Kostensätze, Schwellenwerte, Wirkungsstärken) sind in einer Parameter-Registry offen einsehbar, mit Quellenangabe versehen und je Kommune überschreibbar — lokales Wissen fließt dokumentiert ein, die Verantwortung bleibt bei der Kommune. Der Herkunftsgraph (Lineage) macht jeden Rechenschritt transparent.

**Anschluss an kommunale Arbeitsabläufe.** Ergebnisse werden als GeoPackage (alle Ebenen, GIS-fertig) und als Excel (Maßnahmen, Parameter samt Quellenverzeichnis) exportiert und lassen sich so direkt in kommunale GIS-Systeme, Konzepte und Förderanträge übernehmen.

## 3. Für wen ist KAP2

- **Kommunen** — Klimaanpassungsmanagement, Umwelt- und Stadtplanungsämter als Anwender; Kämmerei, Verwaltungsspitze und Rat als Adressaten der Ergebnisse. Vom ländlichen Gemeindegebiet bis zur Großstadt: Die Analyse skaliert automatisch mit der Gebietsgröße.
- **Beratungs- und Planungsbüros**, die Klimaanpassungskonzepte und KWRA-Mandate für Kommunen bearbeiten und mit KAP2 die Analyse-, Bewertungs- und Priorisierungsarbeit auf eine reproduzierbare, belegte Grundlage stellen.

KAP2 wird hybrid eingesetzt: als Werkzeug im Beratungsmandat — die Kommune als Mandant erhält Ergebnisse, Karten und Berichte — und perspektivisch mit direktem Zugang für Kommunen, die selbst mit dem Werkzeug arbeiten wollen.

## 4. Abgrenzung: Was KAP2 anders macht

**Klimadaten- und Informationsportale** (DWD-Klimaatlas, KLiVO-Portal, GERICS-Klimaausblicke) zeigen, wie sich das Klima ändert — aber nicht, was das für eine konkrete Kommune kostet. Sie liefern Klimasignale auf Landkreis- oder Rasterebene, jedoch keine Risikobewertung je Ortsteil, keine Monetarisierung und keine Maßnahmenplanung.

**Leitfaden- und Selbstcheck-Tools** (UBA-Klimalotse, Stadtklimalotse) strukturieren den Anpassungsprozess methodisch, rechnen aber nichts: keine räumliche Auflösung, keine Daten, keine Euro-Beträge. Sie ergänzen KAP2 prozessseitig, ersetzen aber keine Analyse.

**Klassische Gutachten und Konzepterstellung** durch Ingenieur- und Beratungsbüros (z. B. Hydrotec, GreenAdapt, GI Geoinformatik) liefern fundierte Einzelergebnisse — typischerweise projektweise, über viele Monate, mit projektspezifischer, für Dritte schwer prüfbarer Methodik. KAP2 macht denselben Analysekern reproduzierbar, deutschlandweit einheitlich, in Tagen statt Monaten verfügbar und vollständig quellenbelegt. Für vertiefende Fachplanung (etwa hydraulische Detailmodelle) bleibt das Gutachten der richtige zweite Schritt — KAP2 zeigt vorher, wo er sich lohnt.

KAP2 ist nach unserer Marktsicht das einzige Angebot, das **KWRA-konforme Risikoanalyse mit einer absoluten Schadensschätzung in Euro und Maßnahmen-Kosten-Nutzen-Rechnung vereint** — flächendeckend für jede deutsche Kommune in 100-m-Auflösung, auf dem Fundament vollständiger Quellen-Transparenz. *(Detaillierte Einordnung von 20 Wettbewerbern: siehe [WETTBEWERBSANALYSE.md](WETTBEWERBSANALYSE.md).)*

## 5. Nutzungs- und Preismodell

KAP2 wird als Analyse im Mandat (Ergebnislieferung an die Kommune) und perspektivisch als direkter Produktzugang angeboten. Die Bepreisung bemisst sich an der **Einwohnerzahl des betrachteten Gebiets** — sie skaliert damit fair mit Nutzen und Komplexität der Analyse, von der kleinen Gemeinde bis zur Großstadt. Konkrete Konditionen werden je Vorhaben vereinbart.

---

## 6. Intern: Reifegrad & Grenzen *(nicht zur Weitergabe)*

- **Konformitätsclaim absichern.** Abschnitt 1 erhebt einen harten Anspruch (ISO 14091 / KWRA 2021 / KAnG-Anforderungen). Dieser ist plausibel, aber noch nicht systematisch nachgewiesen. **To-do:** Konformitäts-Checkliste gegen DIN EN ISO 14091 und den UBA-Leitfaden für kommunale Klimarisikoanalysen erstellen und Lücken schließen, bevor der Zweiseiter extern verwendet wird.
- **Aussagekraft der Absolutwerte.** Die eigene Modellkritik (`docs/MODELL_KRITIK.md`) stuft den Risiko-Index als belastbares Screening ein; die monetären Absolutwerte tragen trotz der Schadensfunktions-Nachbesserungen (Schicht B) Unsicherheiten. Gegenüber Mandanten als „erwartete Größenordnung, Parameter anpassbar" kommunizieren, nicht als centgenaue Prognose. Kein Ersatz für Detailgutachten (z. B. 2D-hydraulische Starkregenmodelle).
- **Technischer Reifegrad.** Es gibt derzeit keine Benutzerverwaltung, keine Rollen und keine Mandantentrennung (eine Instanz, Kommunen als Datensätze). Für das Hybrid-Modell mit Direktzugang ist Auth/Multi-Tenancy Voraussetzung — offener Entwicklungsposten.
- **Berichtsformat.** Export existiert als GeoPackage/Excel; ein formatierter Ergebnisbericht (PDF) für Rat und Förderantrag fehlt noch.
- **Nächster Schritt:** Dashboard-Neugestaltung auf Basis dieses Dokuments — das Dashboard muss die hier beschriebenen Kernversprechen (KWRA-Analyse + absolute Schadensschätzung in € als USP, KAnG-Anschluss, Belegbarkeit als Grundlage) für Mandanten sichtbar machen.

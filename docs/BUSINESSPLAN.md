# KAP2 — SaaS-Businessplan (Lean)

*Stand: August 2026 · Internes Arbeitsdokument · Basierend auf [PRODUKTBESCHREIBUNG.md](PRODUKTBESCHREIBUNG.md) und [WETTBEWERBSANALYSE.md](WETTBEWERBSANALYSE.md) · Vorlage: `saas_business_plan_template.md.pdf`*

> Annahme im gesamten Dokument: Preismodell **0,10 € je Einwohner und Jahr** (Jahreslizenz je analysierter Kommune). Offene Punkte dazu in Abschnitt 13.

---

## 1. Executive Summary

- **Firma / Produkt:** KAP2 *(Rechtsform und Firmierung noch festzulegen)*
- **One-Line-Pitch:** KAP2 erstellt für jede deutsche Kommune automatisch eine KWRA-konforme Klimarisikoanalyse auf dem 100-m-Raster — und beziffert Risiken und Anpassungsmaßnahmen als Erstes am Markt in Euro (erwartete Jahresschäden, Kosten-Nutzen je Maßnahme).
- **Problem:** Das Klimaanpassungsgesetz (KAnG) verpflichtet Länder und Kommunen faktisch zu Klimarisikoanalysen und Anpassungskonzepten; heutige Wege dorthin sind monatelange Einzelgutachten ohne Geldwerte oder kostenlose Portale ohne Kommunenschärfe.
- **Lösung:** Vollautomatischer Datenbezug (Zensus, DWD, PEGELONLINE, Copernicus, OSM u. a.), 47 Klimarisiken je 100-m-Zelle nach KWRA-Systematik, Schadensschätzung in €, 47 Maßnahmen mit CAPEX/OPEX und vermiedenen Schäden, vollständige Quellen- und Parametertransparenz (Registry + Lineage), Export als GeoPackage/Excel.
- **Zielmarkt:** Deutsche Kommunen (Anwender: Klimaanpassungs-, Umwelt-, Planungsämter; Adressaten: Kämmerei und Rat) sowie Beratungs- und Planungsbüros mit KWRA-/Konzept-Mandaten.
- **Geschäftsmodell:** Nutzungsbasierte Jahreslizenz, bemessen an der Einwohnerzahl des analysierten Gebiets: **0,10 € je Einwohner p. a.** (empfohlen: Mindestpreis je Kommune, s. Abschnitt 5); Büros lizenzieren je betreutem Mandat.
- **Traction:** Pre-Revenue. Produkt live nutzbar (MVP+): Analysekern für jede deutsche Kommune lauffähig, nationaler Batch über alle Kommunen gerechnet, öffentliche Landing-/Demo-Schicht mit Deutschland-Karte vorhanden. Noch keine zahlenden Kunden.
- **Funding Ask:** Kein externes Funding geplant (Bootstrap); optional später Wachstumsfinanzierung für Vertrieb.

## 2. Problem

- **Schmerzpunkt:** Kommunen müssen (KAnG, DAS-/ANK-Förderlogik) belegen, wo Klimarisiken bestehen und welche Maßnahmen sich lohnen — haben aber weder Daten noch Personal noch Methodik. Ergebnisse müssen vor Rat, Kämmerei und Fördermittelgeber bestehen, also in Euro und prüfbar sein.
- **Wer spürt ihn am stärksten:** Klimaanpassungsmanager:innen und Umweltämter kleiner und mittlerer Kommunen (keine eigenen GIS-/Klimafachleute) sowie Beratungsbüros, die Konzepte in Serie liefern müssen und die Analysearbeit jedes Mal neu aufbauen.
- **Heutige Lösung:** Einzelgutachten der Büros (viele Monate, fünf- bis sechsstellige Projektkosten, Methodik für Dritte schwer prüfbar, keine durchgängigen €-Werte) oder kostenlose Portale (DWD-Klimaatlas, GERICS, Klimalotse) ohne Ortsschärfe, Risikobewertung oder Monetarisierung — oft ergänzt um Excel-Eigenbau.
- **Warum jetzt:** KAnG in Kraft, Landesumsetzungen und Förderprogramme (DAS/ANK, KfW) laufen an; Zensus 2022 und offene Geodaten machen die Vollautomatisierung erstmals flächendeckend möglich. Wer die Position „förderfähige Analyse + Software" zuerst besetzt, setzt den Standard (vgl. Wettbewerbsrisiko GreenAdapt).

## 3. Lösung / Produkt

- **Was das Produkt tut:** Kommune per Suche wählen → KAP2 bezieht alle Daten selbst, rechnet Gefährdung × Exposition × Vulnerabilität auf jeder 100-m-Zelle, zeigt Hotspots auf der Karte, schätzt erwartete Jahresschäden in € (Projektion 2025–2065, RCP 4.5/8.5) und priorisiert Maßnahmen nach Kosten-Nutzen.
- **Kernfeatures (Top 5):**
  1. Automatischer amtlicher Datenbezug für jede deutsche Kommune (keine Zuarbeit nötig)
  2. 47 Klimarisiken nach KWRA-Systematik in 100-m-Auflösung inkl. Hotspot-Karten
  3. Schadensschätzung in € je Risiko und Ortsteil — der USP
  4. 47 Maßnahmen mit CAPEX/OPEX und vermiedenen Schäden, direkt auf der Karte verortet
  5. Vollständige Nachvollziehbarkeit: Parameter-Registry mit Quellen, je Kommune überschreibbar, Herkunftsgraph; Export GeoPackage/Excel
- **Differenzierung / Verteidigbarkeit:** Einziges bekanntes Angebot, das KWRA-Konformität mit absoluter €-Schätzung und Maßnahmen-Kosten-Nutzen vereint (siehe [WETTBEWERBSANALYSE.md](WETTBEWERBSANALYSE.md), 20 Anbieter). Moat: kuratierte Wirkungsketten + quellenbelegte Parameterbasis (jahrelange Fachkuratierung, schwer schnell zu kopieren), Daten-Pipeline über ~10 amtliche Quellen, Transparenz als Vertrauensvorsprung im öffentlichen Sektor. Kein Netzwerkeffekt — Vorsprung muss über Tempo und Förder-/Vertriebszugang gehalten werden.
- **Produktphase:** [x] MVP live (funktional darüber hinaus) · [ ] Paying customers. Offen für Direktvertrieb: Benutzerverwaltung/Mandantentrennung, PDF-Ergebnisbericht, Absicherung des Konformitätsclaims (siehe Abschnitt 11).

## 4. Zielmarkt & Kunde

- **Ideales Kundenprofil (ICP):**
  - *Primär (Jahr 1–2):* Beratungs-/Planungsbüros mit kommunalen Klimaanpassungs-Mandaten — sie haben Budgetzugang (geförderte Konzepte) und Wiederholungsbedarf.
  - *Sekundär (ab Multi-Tenancy):* Kommunen ab ca. 10.000 Einwohnern mit Klimaanpassungsmanagement oder KAnG-/Förderdruck; Käufer: Amtsleitung Umwelt/Planung, Budgetfreigabe Kämmerei/Rat.
- **Nutzer vs. Käufer:** Nutzer sind Fachplaner:innen (Amt oder Büro); Käufer ist die Verwaltungsspitze/Kämmerei bzw. die Büro-Geschäftsführung. Ergebnisse adressieren Rat und Fördermittelgeber — das Produkt muss für Nicht-Nutzer überzeugend berichten (→ PDF-Bericht als Vertriebsvoraussetzung).
- **Marktgröße** (bei 0,10 €/EW p. a.; ~83,5 Mio. EW, ~10.700 Kommunen):
  - **TAM:** Alle deutschen Kommunen ≈ **8,4 Mio. € ARR** — die Per-Capita-Logik deckelt den Markt strukturell (siehe Risiken/offene Fragen: Preis-Floor bzw. höherer Satz prüfen).
  - **SAM:** Kommunen ≥ 10.000 EW (~1.600 Kommunen, ~65 Mio. EW) plus Büro-Mandate ≈ **6,5 Mio. € ARR**.
  - **SOM (36 Monate, realistisch):** 100–200 Kommunen-Äquivalente über den Büro-Kanal und erste Direktkunden ≈ **300–500 Tsd. € ARR**.
- **Markttrends:** KAnG-Umsetzungsdruck über die Länder; ANK-/DAS-Fördermittel; Hitzesommer und Starkregenereignisse halten das Thema auf der Ratsagenda; Personalmangel in Verwaltungen begünstigt Automatisierung.

## 5. Geschäftsmodell & Preise

- **Preismodell:** [x] Usage-based (einwohnerbasierte Jahreslizenz) — faire Skalierung mit Nutzen und Rechenaufwand, leicht kommunizierbar („10 Cent pro Bürger und Jahr").
- **Preispunkte** (0,10 €/EW p. a., Empfehlung mit Mindestpreis **990 €/Jahr**, sonst sind ~85 % der Kommunen < 10.000 EW wirtschaftlich sinnlos):
  - Gemeinde 5.000 EW: 990 € (Floor) · Stadt 25.000 EW: 2.500 € · Stadt 100.000 EW: 10.000 € · Großstadt 500.000 EW: 50.000 € p. a.
  - *Büro-Lizenz:* gleicher Tarif je betreutem Mandat (Abrechnung über das Büro, Weiterberechnung im geförderten Projekt möglich — dort ist der Betrag im Projektbudget vernachlässigbar klein und förderfähig).
- **Abrechnung:** Jährlich im Voraus (passt zu kommunalen Haushalten; unterjährige Monatsabos sind im kommunalen Beschaffungswesen unüblich).
- **Erwarteter ARPU:** ~2.500–3.500 €/Jahr je Kommune-Äquivalent (Mix aus Floor-Fällen und mittleren Städten).

## 6. Go-to-Market

- **Akquisekanäle:** (1) **Büro-Partnerschaften** als Hebel — ein Büro bringt viele Kommunen; (2) Fachvertrieb über Kommunalnetzwerke (Zentrum KlimaAnpassung, Difu, kommunale Spitzenverbände, Landes-Energieagenturen); (3) Content/Nachweis: öffentliche Deutschland-Karte + Demo als Türöffner, Fachbeiträge zur €-Methodik; (4) Listung im KLiVO-Portal.
- **Vertriebsmotion:** [x] Sales-assisted (öffentlicher Sektor: Demos, Pilotprojekte, Vergabeverfahren; Self-Serve erst nach Multi-Tenancy als ergänzender Funnel über die Demo).
- **Schlüsselpartnerschaften:** 2–3 Konzept-Büros als Erstpartner (zugleich Wettbewerber-Neutralisierung, vgl. Rang 3 der Wettbewerbsanalyse); GIS-Anschluss (GeoPackage) als Integrations-Türöffner in bestehende kommunale Workflows.
- **Launch-Plan (erste 90 Tage):**
  1. Konformitäts-Checkliste ISO 14091/UBA abschließen → Zweiseiter extern freigeben
  2. PDF-Ergebnisbericht bauen (Vertriebsvoraussetzung für Rat/Förderantrag)
  3. 3 Pilot-Mandate über Büro-Partner zu Pilotkonditionen; 2 Referenz-Fallstudien („Kommune X: Y Mio. € erwarteter Jahresschaden, Top-5-Maßnahmen") veröffentlichen

## 7. Wettbewerb

*Vollanalyse mit 20 Anbietern und Bedrohungs-Ranking: [WETTBEWERBSANALYSE.md](WETTBEWERBSANALYSE.md). Kondensat:*

| Wettbewerber | Stärken | Schwächen | Unser Vorteil |
|---|---|---|---|
| GreenAdapt (Bedrohung #1) | Identische Zielgruppe, eigene Software, bester Förderzugang | Nach öffentlichem Stand keine durchgängige €-Schadensschätzung | Vollständige €-Schicht + Parametertransparenz; Tempo |
| Ingenieur-/Konzept-Büros (Hydrotec, GEO-NET, energielenker u. a.) | Besitzen heute Kundenbeziehung und Förderkanal; fachliche Tiefe (Hydraulik, Stadtklima) | Monate je Projekt, projektspezifische Methodik, kaum €-Werte, nicht skalierbar | Tage statt Monate, reproduzierbar, deutschlandweit einheitlich — und als Partner gewinnbar |
| Kostenlose Portale (DWD, GERICS, Klimalotse) | Gratis, amtlich, bekannt — der „gut genug"-Einwand | Keine Kommunenschärfe, kein Risiko in €, keine Maßnahmenrechnung | Positionierung „der Rechenkern zum Klimalotse-Prozess"; beginnt, wo Portale enden |
| Enterprise-Klimarisiko (repath, Munich Re, XDI) | €-Monetarisierung, Kapital, SaaS-DNA | Asset-/Konzernfokus, kein KWRA-/Kommunal-Anschluss, grobe Auflösung | KWRA-Konformität + kommunaler Vertriebszugang; Markt für sie (noch) zu klein |

## 8. SaaS-Kennzahlen (Ziele)

- **CAC:** Büro-Kanal ~1.000–2.000 € je Kommune-Äquivalent; Direktvertrieb an Kommunen eher 5.000 €+ (lange Zyklen) — daher Kanalpriorität Büros.
- **LTV:** ARPU ~3.000 € × ≥ 5 Jahre Haltedauer × ~90 % Marge ≈ **13.000 €** (KAnG verlangt Fortschreibung/Monitoring — das Produkt ist wiederkehrend, nicht einmalig; genau deshalb Jahreslizenz statt Einmalanalyse).
- **LTV:CAC-Ziel:** ≥ 5:1 über den Büro-Kanal (Ziel > 3:1 Benchmark).
- **Churn:** < 10 % p. a. ab Jahr 2 (öffentlicher Sektor kündigt selten, Risiko ist eher Nicht-Verlängerung nach Konzeptabschluss → Monitoring-/Fortschreibungs-Features als Retention-Hebel).
- **MRR/ARR-Ziel Jahr 1:** 30–60 Tsd. € ARR (10–20 Kommunen-Äquivalente über Piloten).
- **Bruttomarge:** > 90 % (alle Datenquellen amtlich/offen und kostenfrei; Kosten: Hosting, Batch-Compute, KI-Assistent-Tokens) — über SaaS-Benchmark 70–85 %.

## 9. Team

- **Gründer & Rollen:** Sebastian Lange — Produkt, Entwicklung, Methodik (aktuell Solo; Fachkuratierung der Parameter-/Quellenbasis inklusive).
- **Nächste Schlüsselrollen:** (1) Kommunalvertrieb/Partnermanagement (erster Hire nach zahlenden Piloten); (2) fachlicher Beirat/Freelance-Review Klimafolgenökonomie zur Absicherung der €-Methodik; später (3) zweite:r Entwickler:in (Bus-Faktor).
- **Advisors:** Noch offen — Ziel: je eine Person aus Kommunalverwaltung (Anwendersicht), Förderlandschaft (ANK/DAS) und Klimaökonomie.

## 10. Finanz-Snapshot

- **Startkosten:** Bereits getragen (Eigenentwicklung); verbleibend: Rechtsform/Verträge/Versicherung ~5–10 Tsd. €, ggf. Zertifizierungs-/Review-Aufwand für den Konformitätsclaim.
- **Monatlicher Burn:** < 500 € Infrastruktur (Hosting, Batch-Läufe, Mistral-Tokens) solange ohne Personal; faktischer Burn = Opportunitätskosten der Gründerzeit.
- **Runway:** Nicht limitierend (Bootstrap, minimale Fixkosten).
- **Umsatzprojektion** (bei 0,10 €/EW + 990 €-Floor, Büro-Kanal-Fokus):
  - **J1:** 30–60 Tsd. € (Pilotphase, 10–20 Kommunen-Äquivalente)
  - **J2:** 120–200 Tsd. € (2–3 aktive Büro-Partner, erste Direktkunden nach Multi-Tenancy)
  - **J3:** 300–500 Tsd. € (Verlängerungen + Landes-/Kreis-Rahmenverträge als Upside)
- **Funding:** Nicht erforderlich für den Basisplan; optionaler Raise nur, falls Enterprise-Wettbewerb (repath) in den Markt eintritt und Vertriebstempo entscheidend wird.
- **Mittelverwendung (falls Raise):** Vertrieb/Partnermanagement, Konformitäts-/Methodik-Absicherung, Länder-Datenadapter (LoD2-Ausbau).

## 11. Meilensteine / Roadmap

| Meilenstein | Ziel-Termin |
|---|---|
| MVP live (Analysekern, alle Kommunen, Demo-Schicht) | ✅ erreicht (Juli 2026) |
| Konformitäts-Checkliste ISO 14091/UBA + externer Zweiseiter freigegeben | Q3 2026 |
| PDF-Ergebnisbericht (Rat/Förderantrag) | Q4 2026 |
| 3 bezahlte Pilot-Mandate über Büro-Partner | Q4 2026 – Q1 2027 |
| Benutzerverwaltung & Mandantentrennung → Direktzugang für Kommunen | Q1–Q2 2027 |
| Erste 10 zahlende Kunden (Kommunen-Äquivalente) | Mitte 2027 |
| Break-even (Vollkosten inkl. 1 Vertriebs-Hire) | 2028 |
| Series A / Raise | Nicht geplant (nur reaktiv, s. o.) |

## 12. Risiken & Gegenmaßnahmen

- **Größtes Risiko — „Gratis ist gut genug" + Förderlogik:** Kommunen halten kostenlose Bundes-/Landesangebote für ausreichend, und Fördertöpfe finanzieren traditionell Beratungs*leistung*, nicht Software*lizenzen*. **Mitigation:** Vertrieb primär über Büros (dort ist KAP2 Werkzeug im geförderten Mandat, kein eigener Beschaffungsvorgang); Positionierung als Rechenkern, der dort beginnt, wo Gratis-Angebote enden; Referenz-Fallstudien mit €-Zahlen, die Portale nicht liefern können.
- **Strukturell gedeckelter Markt:** 0,10 €/EW ergibt selbst bei Vollabdeckung Deutschlands nur ~8,4 Mio. € ARR. **Mitigation:** Preis-Floor (990 €), spätere Zusatzmodule (Monitoring/Fortschreibung, Berichtswesen, Detailrisiko-Pakete), perspektivisch höherer Satz oder Staffelmodell — Preis vor Skalierung validieren, Erhöhung nach Referenzphase ist im öffentlichen Sektor schwer.
- **Glaubwürdigkeit der €-Werte:** Die Absolutwerte tragen Modellunsicherheiten (vgl. [MODELL_KRITIK.md](MODELL_KRITIK.md)); ein öffentlich zerpflücktes Ergebnis wäre vertrieblich verheerend. **Mitigation:** Kommunikation als „erwartete Größenordnung, Parameter anpassbar", Transparenz-Architektur als Schutz, externer Methodik-Review vor Skalierung, kein Ersatz-Claim gegenüber Detailgutachten.
- **Wettbewerbsfenster:** GreenAdapt oder ein herunterskalierender Enterprise-Anbieter besetzt die Position zuerst. **Mitigation:** Tempo bei Referenzen, Büro-Partner vertraglich binden, USP-Tiefe (Parameterbasis) ausbauen.
- **Solo-Gründer / Bus-Faktor:** Produkt, Methodik und Vertrieb hängen an einer Person. **Mitigation:** Dokumentationsstand hoch halten (bereits gut: Berechnungshandbuch, Modellkritik), früher Vertriebs-Hire, Beirat.

## 13. Offene Fragen (zur Klärung durch den Product Owner)

1. **Preisbezug:** Gilt 0,10 €/EW **pro Jahr** (Abo, hier angenommen) oder **einmalig pro Analyse**? Einmalig würde LTV, Projektionen und das SaaS-Modell grundlegend ändern.
2. **Mindestpreis:** Ist der empfohlene Floor (990 €/Jahr) gewollt? Ohne Floor sind ~9.000 Kommunen unter 10.000 EW keine tragfähigen Kunden.
3. **Büro-Konditionen:** Gleicher Tarif je Mandat oder Partnerrabatt/Flatrate für Büros mit vielen Mandaten?
4. **Firmierung:** Name, Rechtsform, Gründungszeitpunkt für Abschnitt 1.
5. **Kapazität:** Wie viele Wochenstunden fließen realistisch in Vertrieb? Die J1-Projektion nimmt nebenberufliche Pilotakquise über 2–3 Büro-Kontakte an.

---

*Tipp aus der Vorlage übernommen: Dieses Dokument quartalsweise fortschreiben.*

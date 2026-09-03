# Methodik-Bericht #98 — UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)

Status: **Rev. 14 (Abarbeitung der Review-Runden 16–23, Befunde 336–420) — im Review** ·
03.09.2026 ·
Instruktionsquelle: `docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md` (v2) · Umsetzungsgrundlage:
**Ansatz 98-A** (amtliche Inzidenz + Trend-Attribution über BAF; Entscheidungslog Nr. 1)
· Familie: **K1-Gesundheit bottom-up** (Prototyp #95; §2.6 — kein erneuter Drei-Ansätze-Vergleich)

> **Konformitätsvermerk zur Aufgaben-Fortschreibung 30.08.2026** (Ressourcen-Regel
> §3.4, Datenebenen-Anlagepflicht §3.1; Nutzer-Entscheid, vgl. #95 Rev. 8):
> Dieser Bericht ist geprüft konform — er plant **keinen** nationalen
> 100-m-Vollraster-Lauf als Prüf-/Abgleichinstrument. Die benötigten Zellgrößen
> laufen auf den **drei** Wegen, die §3.1 vorsieht — *vorhanden*, *neu anzulegen*
> und *geparkt (Datenquelle fehlt)* — und werden im
> Bericht durchgängig so bezeichnet (Befunde 215/366):
> die SSD-Ebene (DWD `sunshine_duration` 1 km, Register 98-E20-01) ist
> „**neu anzulegen**“, vollständig spezifiziert und inzwischen angelegt (§3.2/§3.6);
> die Außenbeschäftigten-Ebene (98-OUT-01) ist „**geparkt** (Datenquelle fehlt)“
> mit Beschaffungs-Watchlist — für sie existiert keine keyless Zellquelle, und ihr
> Parameter \(r_{\text{out}}\) läuft dokumentiert auf dem Zentrierungs-Neutralwert
> \(q = \bar q\) ⇒ Faktor 1. **Ebenso geparkt ist die Verhaltens-Ebene**
> \(\varphi_{\text{Komfort}}\) (98-S154-01, Befund 378): auch für sie fehlt eine
> keyless kommunale Quelle, ihr Parameter \(v_{\text{verh}}\) läuft auf dem
> Neutralwert 1 und ist als eigene Achse in §4 ausgewiesen. Es sind also **zwei**
> geparkte Ebenen, nicht eine. Alle übrigen Zellgrößen sind vorhanden oder
> regional/national.

> **Revisionsstand.** Rev. 1 (30.08.2026) = Migration des #98-Anteils von M0 Rev. 5
> (`docs/render/METHODIK_M0_GESUNDHEIT.html`, Kap. 4) in das §4-Format plus Abarbeitung
> der #98-relevanten Befunde der Gegenprüfung (GP-9/-10, 15, 16, 22, 26/34, 28–32, 37, 41,
> 43) und der Review-Runden 1–3 (Befunde 201–212).
> **Rev. 2 (31.08.2026)** = Review-Runde 4 (Befunde 213–222). Modellrelevant sind
> drei Änderungen, alle im Entscheidungslog Nr. 16–18: (1) der Baseline-**Anker** ist
> jetzt das Mittel **2021–2023** statt des Einzeljahrs 2023, weil die abgelesenen
> altersspezifischen Raten laut Abbildungstitel über genau diese drei Jahre gepoolt
> sind (Befund 220) — dadurch ändern sich \(c_{\text{kal}}\), \(\lambda_e\) und alle
> Bundessummen; (2) \(k_{\text{UV}}\) steht als **Herleitungswert 0,8434** in der
> Registry statt gerundet 0,84 (Befund 213); (3) \(v_{\text{verh}}\) ist als
> **Jahres**faktor mit explizitem Wirkungsort definiert (Befund 216).
> **Rev. 3 (01.09.2026)** = Review-Runde 5 (Befunde 223–229). Modellrelevant sind
> zwei Änderungen, beide im Entscheidungslog Nr. 19–20: (1) die nationale
> \(\Delta\text{SSD}\) ist jetzt **bevölkerungsgewichtet** (8,51 % statt
> flächengewichtet 7,82 %), weil das Produktionsmodell bevölkerungsgewichtet über
> Zellen summiert — §3.4 „Kalibriermodell = Produktionsmodell" (Befund 223);
> (2) \(\bar L_e\) wird über die **Jahres**mediane des Ankerfensters gerechnet
> statt über das Sterbealter des Einzeljahrs 2023 (Befund 224). Dadurch ändern
> sich alle Bundessummen: € 367 → **401 Mio**, YLL 1.521 → **1.664**.
> **Rev. 4 (01.09.2026)** = Review-Runde 6 (Befunde 230–237). Modellrelevant ist
> **eine** Änderung (Entscheidungslog Nr. 23): \(k_{\text{UV}}\) wird mit einem
> **ortsgleichen** Nenner hergeleitet — dem Raster-SSD-Trend an der Dortmunder
> Messzelle (6,48 %/Dek.) statt dem NRW-Gebietsmittel (5,81 %/Dek.) ⇒
> **0,7562 statt 0,8434**. Zugleich ist der Quellen-Widerspruch benannt, den Rev. 3
> übersehen hatte: Der Stations-SSD-Trend 11,3 %/Dek. ist **belegt** (Abstract von
> [31]) und nicht, wie fünfmal behauptet, unbelegt. Wirkung: € 401 → **360 Mio**,
> YLL 1.664 → **1.492**.
> **Rev. 5 (01.09.2026)** = Review-Runde 7 (Befunde 238–244). Modellrelevant ist
> wieder \(k_{\text{UV}}\) (Entscheidungslog Nr. 24): Rev. 4 hatte den **Nenner**
> auf Rasterskala gezogen, den **Zähler** aber als Stationsmessung stehen lassen.
> Eigene Messung zeigt, dass die Skalendifferenz **metrikabhängig** ist (Raster ÷
> Station: SSD 0,57, Globalstrahlung 0,76). Die Globalstrahlung liegt in beiden
> Familien vor und trägt jetzt die Übersetzung ⇒ \(k_{\text{UV}}\) = **0,5782**;
> beide Bandstützen sind gerechnet (**0,4336–0,6667** statt 0,4336–1,0, Befund 239).
> Wirkung: € 360 → **275 Mio**, YLL 1.492 → **1.141**.
> **Rev. 6 (01.09.2026)** = Review-Runde 8 (Befunde 245–251). Modellrelevant ist
> Entscheidungslog Nr. 25: Der Stationsquotient Dosis/Globalstrahlung ist in [31]
> **beziffert** (»Global radiation increases similarly to the UV data«) und war in
> Rev. 5 fälschlich aus einer Relationsangabe geschätzt worden ⇒ k_UV = **0,6667**.
> Das Band kommt jetzt aus der **räumlichen Streuung** über acht Standorte
> (**0,3656–0,9187**) statt aus zwei Skalen-Grenzfällen — das ist die dominierende
> Unsicherheit. Wirkung: € 275 → **317 Mio**, YLL 1.141 → **1.315**.
> **Rev. 7 (01.09.2026)** = Review-Runde 9 (Befunde 252–263). Der **Volltext** von
> [31] liegt seit 01.09.2026 vor (Open Access) und löst die beiden offenen
> A-Befunde: Der Stationsquotient ist in Tab. 2/Tab. 4 **beziffert** (4,9/4,6 =
> 1,0652) statt qualitativ, und die GR/SunD-Reihen stammen von DWD-Station **1117
> Bochum**, nicht aus Dortmund. Der Rasterquotient war dort **bevölkerungsgewichtet**
> (0,6323) ⇒ \(k_{\text{UV}}\) = **0,6735**; das Band kam erstmals aus den
> **publizierten Standardfehlern**, die räumliche Streuung wurde zur
> **Modellgrenze 9** (Befunde 255/256). Wirkung: € 317 → **320 Mio**.
> **Rev. 8 (01.09.2026)** = Review-Runde 10 (Befunde 264–273). Modellrelevant ist
> Entscheidungslog Nr. 27: Der bevölkerungsgewichtete Rasterquotient war mit dem
> **SSD-Trend 1997–2022** gewichtet, das Produktionsmodell multipliziert
> \(k_{\text{UV}}\) aber mit der **Normalperioden-ΔSSD**; beide Felder korrelieren
> nur mit r = 0,24. Mit dem richtigen Gewicht: q = **0,6774** statt 0,6320 ⇒
> \(k_{\text{UV}}\) = **0,7216**. Wirkung: € 320 → **343 Mio**. Zusätzlich ist der
> Lint `backend/scripts/lint_methodik.py` gebaut, der Revisionsrückstände und
> Bericht-⇄-Registry-Divergenzen maschinell abfängt (Befunde 248/258/264).
> **Rev. 9 (01.09.2026)** = Review-Runde 11 (Befunde 274–282). Zwei Punkte:
> (1) Der Rasterquotient wird jetzt mit **Baseline-Fällen** statt Köpfen gewichtet
> (Befund 278) ⇒ q = **0,6843**, \(k_{\text{UV}}\) = **0,7289**, € **347 Mio**.
> (2) Die Runde hat aufgedeckt, dass in Rev. 8 acht Befunde als „übernommen“
> geschlossen waren, ohne umgesetzt zu sein — Ursache waren Ersetzungsskripte, deren
> Fehlschläge ich nicht geprüft habe. Der Lint ist entsprechend verschärft: Er sieht
> jetzt **LaTeX-Zahlen** (in dieser Schreibweise), prüft **Definitionsgleichungen** gegen die
> Registry und löst **Dict-Parameter-Blöcke** auf. Er findet den Rückstand, den
> Runde 11 gemeldet hat.
> **Rev. 10 (01.09.2026)** = Review-Runde 12 (Befunde 283–293). **Keine
> Modelländerung** — die Runde hat den Modellkern ausdrücklich nicht beanstandet.
> Abgearbeitet wurden ausschließlich Nachweis- und Rückstandsbefunde, darunter die
> vierfach zurückgefallene `source_detail` in `params.py` (jetzt **neu geschrieben**
> statt gepatcht) und die durch globale Ersetzung überschriebenen Revisionsnotizen
> (jetzt wieder historisch korrekt). Der Lint prüft zusätzlich den **Knoten-Abgleich
> gegen die Arbeitsmappe** und bezieht seine Negativmenge nicht mehr aus der
> Korrekturhistorie — 127 Checks.
> **Rev. 11 (01.09.2026)** = Review-Runde 13 (Befunde 294–301). Modellrelevant ist
> Entscheidungslog Nr. 29: Der Rasterquotient ist seit der Fallgewichtung ein
> **gewichtetes Mittel der Punktquotienten** — damit schlagen 57 Punkte mit
> verschwindendem SSD-Trend (q bis 196) voll durch und hoben den Bundeswert um
> 2,3 %. Sie sind jetzt ausgeschlossen, die **Aggregationsregel** ist dokumentiert
> (§3.9) ⇒ q = **0,6683**, \(k_{\text{UV}}\) = **0,7119**, € **339 Mio**.
> **Rev. 12 (01.09.2026)** = Review-Runde 14 (Befunde 302–318). Keine
> Modelländerung; abgearbeitet wurden Rückstände, Kennzeichnungen und
> Lint-Lücken. \(k_{\text{UV}}\) unverändert **0,7119**, € **339 Mio**.
>
> **Rev. 13 (02.09.2026)** = Review-Runde 15 (Befunde 319–335). Keine
> Modelländerung. **Diese Fassung ist bei einem Werkzeugfehler verloren gegangen**
> (sie lag nur im Arbeitsverzeichnis, nicht in der Versionskontrolle); Rev. 14
> setzt deshalb auf Rev. 12 auf. Review-Runde 16 hatte festgestellt, dass von den
> 17 Befunden der Runde 15 nur vier umgesetzt waren — der inhaltliche Verlust ist
> auf diese vier begrenzt und in Rev. 14 nachgezogen (Befunde 356/357).
>
> **Rev. 14 (03.09.2026)** = Review-Runden 16 bis 23 (Befunde 336–420). Keine
> Modelländerung — \(k_{\text{UV}}\) **0,7119**, ΔDosis **4,54 %**, YLL **1.404**,
> € **339 Mio** stehen seit Rev. 11 unverändert und wurden in **jeder** seither
> gefahrenen Review-Runde unabhängig nachgerechnet. **Eine Zählung steht hier
> bewusst nicht** (Befunde 400/407/416): Sie altert mit jeder Runde und ist in
> neun aufeinanderfolgenden Runden zurückgefallen. Die Zahl der Reproduktionen
> führt das Ledger, das sie ohnehin belegt — der Bericht verweist darauf,
> statt sie zu duplizieren. Neu ist der **Rechenschritt kumulative → jährliche Dosis** in §3.4
> (Gleichgewichtslesart mit Transient-Faktor \(\tau\) = 0,20–0,48, jetzt größte
> Achse der §4-Bändertabelle) sowie die vollständig gemessene **Punktmengen-Kette**.
> Prüfmechanik: Ledger auf eine Zeile je Befund, Status aus **Prüfausdrücken**
> abgeleitet (W7); Lint-Ratchets gegen zu enge Ausnahmen und gegen Registry-Specs
> ohne Parameter-Block.
>
> Status je Befund in `reviews/BEFUNDE_98.md`. Diese Markdown-Datei ist die Quelle für
> #98 (§2.7). Alle Ermessensentscheidungen im **Entscheidungslog** (Ende der Datei).
> Anlagen: `backend/scripts/kalibrierung/dwd_ssd_trend.py` +
> `backend/data/kalibrierung/ssd_trend_region.csv`;
> `backend/data/kalibrierung/kid2025_ablesewerte.csv` (Roh-Ablesewerte §3.3);
> `backend/scripts/kalibrierung/kid2025_baseline.py` +
> `backend/data/kalibrierung/kid2025_baseline.md` (Anker, Struktur-Validierung und
> Bänder, §3.3/§4);
> `backend/scripts/kalibrierung/ssd_povw.py` +
> `backend/data/kalibrierung/ssd_povw.{csv,md}` (bevölkerungsgewichtete
> \(\Delta\text{SSD}\), §3.2/§4 — neu in Rev. 3);
> `backend/scripts/kalibrierung/k_uv_herleitung.py` +
> `backend/data/kalibrierung/k_uv_herleitung.{csv,md}`
> (\(k_{\text{UV}}\)-Herleitung auf Rasterskala, §3.2 — Rev. 7; ersetzt die
> Rev.-4-bis-6-Anlage `ssd_dortmund_k_uv.py`).

## 1 Wirkungskette & Knoten-Bilanz (§2.1)

Kette laut Arbeitsmappe (Sheet „Klimawirkungsketten" Z409, Knoten **W186**; Konfidenz
**hoch** — einziger direkter Hazard-Pfeil E20, eindeutige Container-Zuordnung).
Rollen/Kanten: Sheet „Schadensbaum-Netzwerkliste" Z99 (Id 98): **Buchungsobjekt — Ebene B**,
Handlungserfordernis **sehr dringend**; keine Ein-/Ausgangskanten auf Risikoebene.
KWRA-Charakteristik: extensiv betrachtet (keine eigenen KWRA-Indikatoren); der Klimapfad
läuft laut KWRA wesentlich über das **Verhalten** („verhaltensbedingt steigende Exposition
in längeren, sonnigeren Warmphasen" — Monetarisierung ID 98, Blattzeile 103).

### Knoten-Bilanz

| Knoten | Name | rechnet in | Wo (Formel/Ebene) | falls inaktiv: Begründung |
|---|---|---|---|---|
| E20 | UV-Strahlung (direkter Hazard) | Schicht A + B | \(\Delta\text{Dosis}\) über SSD-Normalperiodenvergleich × \(k_{\text{UV}}\) × \(a_{\text{attr}}\) (§3.2); Ebene UV_RADIATION/SSD (neu) | — |
| S154 | Freizeitverhalten | **Sensitivitätsband** (Default 1) | \(v_{\text{verh}}\)-Band +0,25…+0,60 je Komforttag (§3.5) | keine quantifizierte Effektgröße „Mehr-Exposition je Komforttag" für DE [36]; US-Zeitverwendungs-Evidenz nur Band (§3.2: unbelegte Modulatoren Default 1; Log 11) |
| S155 | Gefahrenbewusstsein | Maßnahmen-Hebel (**qualitativ**) | UV-Schutz im öffentlichen Raum / UV-Index-Kommunikation (§5) | Basiswert: Nutzen-Kosten-Verhältnisse sind keine Effektgröße auf Dosis/Inzidenz (GP-26/34; Log 12) |
| S158 | Monitoring / Frühwarnsysteme | Maßnahmen-Hebel (**qualitativ**; Kostenwirkung bereits im Basiswert) | Früherkennungs-Förderung (SCS-Teilnahme); §5 — Befund 203 | Basiswert setzt bereits SCS-Kosten für alle Fälle an — additiver Hebel hätte kein Headroom; quantifizierbar erst mit Detektionsmix-Parameter (Ersetzungspfad) |
| R35 | Vorkommen von Bevölkerung | Schicht A + B | \(\text{pop}_a\) (Zensus 2022; Ebene u20 aus #96 mitgenutzt) | — |
| R36 | Vorkommen von Gesundheitsinfrastruktur | Schicht A (Screening) | Ebene HEALTHCARE_ACCESS im Index (§3.7) | Basiswert Default 1: keine Evidenz für einen Distanz-/Kapazitätseffekt auf Hautkrebs-Outcomes; Zugangseffekte stecken im SCS-Hebel (§3.2; Log 13) |
| — | Berufliche Außenexposition (**kein Knoten der W186-Kette**) | **Sensitivitätsband** (Basiswert-Default 1) | \(r_{\text{out}}\) (nur SCC-Anteil am Zusatz, nur Bänder 20–64 … 85+; §3.4); Ebene Außenbeschäftigten-Anteil **geparkt (Datenquelle fehlt)** — Beschaffungs-Watchlist INKAR/SVB (§3.1; Befund 215) | GP-9: Kettentreue („nicht mehr, nicht weniger") — Aufnahme in den Basiswert erforderte eine Fortschreibung der Arbeitsmappe + Abgleich-Protokoll-Punkt (dokumentierter Ersetzungsweg); Evidenz (BK 5103, Meta-OR 1,77 [43]) und \(\bar q_{\text{out}}\)-Herleitung liegen vollständig vor (Log 10) |

### Weitergaben (zweispaltig; Quelle: Netzwerkliste + Abgleich-Protokoll)

| Output-Kanten (Abgleich-Protokoll) | Konto-Ausschlüsse / verwandte Buchungen (K1-Definition) |
|---|---|
| **keine** — die Netzwerkliste führt für #98 keine Output-Kanten, das Abgleich-Protokoll keinen Punkt zu #98 (einzige K1-weite Fortschreibung: **P52** Mortalitätsbewertung YLL × VOLY, gilt für alle K1-Buchungsobjekte) | **R9-Partition** (Monetarisierung ID 98: „Doppelzählung mit anderen K1-Ursachen"): jeder Fall zählt genau einmal unter der Ursache UV; **Produktionsausfälle → K2** (K1-Definition), **Systemvorhaltung → K8 via ID 102** (K1-Definition; keine Kante von #98) |

### Konto-Einbettung

- **Konto:** K1 Gesundheit, **Ursache: UV** (R9-Partition); Bausteine **K1-Mortalität +
  K1-Morbidität** (Netzwerkliste Z99; Monetarisierung Blattzeile 103: „Zusätzliche
  Erkrankungsfälle × Behandlungskosten + Mortalitätsanteil als YLL × VOLY [MK 4.0;
  Fortschreibung P52; VSL nur Sensitivität]").
- **Anzuwendende Rechenregeln:** R9 (laut Monetarisierung, Spalte „Regeln").
- **Nur K1 aktiv (M0):** bewusste **Untergrenze** („konservativ" = *unterschätzend* wie in
  #95/#96); Augenschäden (Katarakt — im Monetarisierungs-Gegenstand genannt) und
  Produktivität (K2, ab M3) nicht enthalten — dokumentierte Untererfassung (§6).

## 2 Evidenz-Register (§2.2)

Risikoübergreifend wiederverwendbare Zeilen zusätzlich in `docs/evidenz/register.md`.
Nur Zeilen mit Entscheidung **Basiswert** kommen in den Formeln (§3) vor.

| Register-ID | Knoten → Outcome | Effektgröße | Studientyp | Quelle | Übertragbarkeit | Datenlage je Zelle | Entscheidung | E-Regel |
|---|---|---|---|---|---|---|---|---|
| 98-E20-01 | E20 SSD-Änderung (Klimanormalperioden) | **bevölkerungsgewichtet DE +8,51 %; N/M/S +7,82/+9,15/+7,77 %** [72] (flächengewichtet zum Vergleich: DE +7,82 %, 1.544,0 → 1.664,8 h [69]) | amtliche Messreihe, eigene Auswertung (Skript [69]) | DWD-CDC Gebietsmittel [33]; `ssd_trend_region.csv` [69]; Gemeindepunkt-Gewichtung `ssd_povw.csv` [72] | DE-weit; Fenster 1961–90 vs. 1991–2020 (GP-Befund 37); Gewichtung wie im Produktionsmodell (Befund 223) | DWD sunshine_duration 1 km (Ebene **neu anzulegen**) | **Basiswert** | Log 4 |
| 98-E20-02 | SSD → erythemwirksame Dosis | \(k_{\text{UV}}\) = **0,7119** (Band **0,3622–1,0616**) = (Dosis/Global)|Station × (Global/SSD)|Raster = (4,9/4,6) × 0,6683 | publizierte Messreihen ([31] Tab. 2 und Tab. 4, Volltext) × eigene Rastertrendrechnung; zwei Messfamilien, über die Globalstrahlung skalenfrei verbunden | Lorenz 2024 [31] (**Volltext** primär verifiziert); eigene Rastermessung [73] | Messort der GR/SunD-Reihen ist DWD-Station 1117 **Bochum** (10 km von der UV-Station); Skalendifferenz Station↔Raster ist **metrikabhängig** (GR 0,98, SunD 0,59); Band = publizierte Standardfehler (±49,1 %, 1 σ) | berechnet | **Basiswert** | Log 2, 23–26 |
| 98-E20-03 | Klimawandel → Anteil am SSD-/Dosistrend | \(a_{\text{attr,UV}}\) = 0,75 (Band 0,5–1,0) — **gekennzeichnete Abschätzung** | Einordnung (Lorenz: „starker Einfluss der Bewölkungsabnahme"; Aerosol-„Brightening" spricht gegen 1,0) | [31]; GP-Befund 15 | Attributionstudie für DE-UV existiert nicht (Lücke, Ersetzungspfad) | Literatur-Band | **Basiswert** | Log 3 |
| 98-E20-04 | Dosis → Inzidenz (Verstärkungsfaktoren) | BAF: SCC 2,5 ± 0,7 · BCC 1,4 ± 0,4 · MM 0,6 ± 0,4 (%-Inzidenz je +1 % Dosis) | biologisch-epidemiologisches Standardmodell; unabhängig bestätigt | Slaper 1996 [29]; RIVM 2023 [29]; Madronich 2021 [30] | international etabliert (Montreal-Protokoll-Folgenabschätzung) | — | **Basiswert** | Log 1 |
| 98-R35-01 | R35 Bevölkerung → Baseline-Fälle | \(I_{e,a}\) je Band (Ablesekette §3.3 aus KID-2025-Abb. 3.13.2/3.14.3, normiert auf den **Anker 2021–2023**) | amtliche Krebsregisterdaten (Abbildungs-Ablesung, gekennzeichnet) | ZfKD KID 2025, Kap. 3.13/3.14 [27] | DE, gepoolt **2021–2023** (Abbildungstitel) — Anker deshalb dasselbe Fenster (Befund 220); Struktur-Validierung ASR +0,1…+1,9 % (§4) | Zensus-Altersbänder (+ u20 aus #96) | **Basiswert** | Log 5, 16 |
| 98-K1-01 | Fall → Erstjahres-Behandlungskosten | MM 5.326 (SCS-detektiert) / 9.038 €₍₂₀₁₅₎ (nicht-SCS); NMSC 4.660/5.890 — Basis = SCS-Werte ⇒ 6.724/5.883 €₂₀₂₄ | Krankenkassen-Routinedaten (AOK; DiD-Design) | Speckemeier 2022 [34] (Volltext-Abstract primär verifiziert; Kohorte Diagnose 2014/2015) | DE; **Proxy**: Gesamt- statt inkrementelle Kosten, nur Erstjahr (§3.4) | national | **Basiswert** (untere Stütze) + Band | Log 7 |
| 98-K1-02 | MM/C44 → Letalität, Restlebenserwartung | \(\lambda_{\text{MM}}\) = 0,11466 · \(\lambda_{\text{C44}}\) = 0,005236 (Mittel 2021–2023); \(\bar L_{\text{MM}}\) = 10,4569 · \(\bar L_{\text{C44}}\) = 5,4787 J. (Jahresmediane des Ankerfensters, Befund 224) | amtliche Statistik + Approximationen (**gekennzeichnet**: Perioden- bzw. Median-Approximation, GP-Befund 43) | ZfKD KID 2025 Tab. 3.13.1/3.14.1 [27]; Sterbetafel 2022/2024 [48] | DE; Zähler und Nenner im selben Fenster wie die Ablesekette (Befund 220) | national | **Basiswert** | Log 8, 16 |
| 98-S154-01 | S154 Verhalten → Mehr-Exposition je Komforttag | \(s\) ≈ +0,45 (Kernband +0,25…+0,60) als **Tages**wert; Hitzetage > 30 °C: −5…−13 % Aktivität | Zeitverwendungs-/Dosimetrie-Evidenz (US) | Graff Zivin & Neidell 2014 [57]; [58,59] | US-Übertragbarkeit begrenzt; Ambient-Anteil steckt bereits in ΔDosis (Doppelzählungsschutz) | Jahresumrechnung braucht den dosisgewichteten Komforttag-Anteil \(\phi\) — Ebene **geparkt** (§3.4; Befund 216) | **Sensitivitätsband** (Default 1) | Log 11, 17 |
| 98-S155-01 | S155 UV-Schutzprogramme → Inzidenz | Nutzen-Kosten 2,2–8,7 : 1 (AUS/USA/EU) — **keine** Dosis-/Inzidenz-Effektgröße | Programm-Evaluationen | Shih/Doran/Collins [37] | keine deutsche Studie [37] | kommunal | **Maßnahmen-Hebel (qualitativ)** | Log 12 |
| 98-S158-01 | S158 Früherkennung (SCS) → Fallkosten/Letalität | −18,8 % [8,4–23,1] Erstjahreskosten je MM-Fall bei SCS-Detektion (belegt das Sparpotenzial); Letalitätswirkung nicht angesetzt | quasi-experimentell (DiD, Routinedaten) | Speckemeier 2022 [34] | DE; **Wirkung im Basiswert enthalten** (Basis-\(c_e\) = SCS-Werte; Befund 203) | kommunal (Teilnahmequoten) | **Maßnahmen-Hebel (qualitativ)** | Log 12 |
| 98-OUT-01 | Berufliche Außenexposition → SCC | OR 1,77 [1,37–2,30] (Fall-Kontroll-Pool; Kohorten 1,68 [1,08–2,63]); \(\bar q_{\text{out}}\) = 0,070 (VGR 2023: [572 + 2.643] / 45.909 Tsd. [70]) | Meta-Analyse (BK-5103-Grundlage) | Schmitt 2011 [43] (Abstract primär verifiziert); Destatis VGR [70] | DE; **kein Knoten der W186-Kette** (GP-9); Evidenz gilt für **Erwerbs-/Nacherwerbsbänder**, nicht für u20 (Befund 218) | INKAR/SVB-Branchenanteile — Ebene **geparkt (Datenquelle fehlt)**, Watchlist (Befund 215) | **Sensitivitätsband** (Basiswert-Default 1) | Log 10, 18 |
| 98-R36-01 | R36 Gesundheitsinfrastruktur → Outcome | keine Evidenz für Distanz-/Kapazitätseffekt auf Hautkrebs-Inzidenz/-Letalität | — | — | Zugangseffekt steckt im SCS-Hebel | HEALTHCARE_ACCESS (Schicht A) | **bewusst inaktiv** (Default 1) | Log 13 |

## 3 Modell (§2.3) — Ansatz 98-A, Schicht B

**Native Ergebnisgröße (§3.6, deklariert): verlorene Lebensjahre (YLL) je Jahr** (GP-Befund
28). Teil-Ausweise unter der KWRA-Klammer: klimaattribuierte Zusatzfälle \(\Delta F_e\)
(je Entität), €.

**Gemeinsamer Preisstand aller Kostensätze dieses Berichts: €2024**; Umrechnungsfaktoren je
Satz in der Zeichentabelle (Destatis-VPI, 2020 = 100: 2015 = 94,5 · 2024 = 119,3 [19]).

### 3.1 Entitäten (§-Konvention)

\(e \in \{\text{MM}, \text{C44}\}\): malignes Melanom (ICD-10 C43) und nicht-melanotischer
Hautkrebs (C44). Innerhalb C44 wirken BAF und Außenberufs-Evidenz entitätsspezifisch
(SCC vs. BCC). **Split-Quellen im Widerspruch (§3.8, benannt — Befund 202):** das
wertetragende KID-2025-C44-Kapitel [27] gibt für 2021–2023 „knapp drei Viertel Basaliome …
etwa ein Viertel Plattenepithelkarzinome" an (\(w_{\text{SCC}}\) ≈ 0,25); die
2015er-BfS-Fallzahlen (BCC 158.840 · SCC 98.950, Sekundärangabe in [27]/[36]) ergäben
0,384. **Basiswert = 0,25** (aktuelle Registerdaten der Primärquelle), Band 0,25–0,50
(obere Stütze: BfS-2015-Split; mögliche Ursache der Differenz: Untererfassung/Meldepraxis
von SCC-Mehrfachtumoren — Volltext-Verifikation [36] als Ersetzungspfad). Der Split wird
**altersinvariant** angewendet (GP-Befund 41 — dokumentierte Annahme; Richtung: SCC-Anteil
steigt real mit dem Alter ⇒ Unterschätzung des Zusatzes in alten Kommunen):

$$ \text{BAF}_{\text{C44}} \;=\; 0{,}75 \cdot 1{,}4 + 0{,}25 \cdot 2{,}5 \;=\; 1{,}675 \qquad (\text{Band } 1{,}675\text{–}1{,}95 \text{ über } w_{\text{SCC}} = 0{,}25\text{–}0{,}50). $$

### 3.2 Klimasignal: Dosisänderung (Anker `#delta-dosis`, `#k-uv`)

$$ \Delta\text{Dosis}_{\text{Zelle}} \;=\; \frac{\text{SSD}_{\text{Zelle}}^{\,1991\text{–}2020} - \text{SSD}_{\text{Zelle}}^{\,1961\text{–}1990}}{\text{SSD}_{\text{Zelle}}^{\,1961\text{–}1990}} \cdot k_{\text{UV}} \cdot a_{\text{attr,UV}} $$

- **Mittelungsfenster = Klimanormalperioden je Zelle** (GP-Befund 37; Einzeljahre sind
  wegen der SSD-Variabilität ungeeignet — Rekordjahre ≈ 2.015–2.024 h [33]).
  **Verifikation bei der Integration (31.08.2026):** Das 1-km-Raster
  `sunshine_duration` ist ab 1961 verfügbar; die 60 Jahresraster wurden einmalig zu
  zwei Normalperioden-Mittelrastern vorgemittelt (Anlage `ssd_normalperioden.npz`) —
  der Zellwert ist der Regelfall, das Bundesland-Gebietsmittel nur noch Fallback für
  Zellen außerhalb des Rasters.
- **Nationaler Bezugswert = bevölkerungsgewichtet, nicht flächengewichtet
  (Befund 223; Log 19).** Das Produktionsmodell rechnet \(\Delta\text{Dosis}\) je Zelle
  und summiert Zellen zur Kommune; die wirksame nationale \(\Delta\text{SSD}\) ist damit
  das **bevölkerungsgewichtete** Mittel der relativen Zelländerungen. Das
  DWD-Gebietsmittel (+7,82 %) und das Rasterflächenmittel (+7,90 %) sind beide
  **flächen**gewichtet und dafür der falsche Bezug — §3.4 nennt „bevölkerungsgewichtete
  Exposition" ausdrücklich als Fall, in dem ein Näherungswert die Kalibrierung
  unzulässig macht (dieselbe Klasse hat #95 in Rev. 8 gelöst). Gewichtet wird auf der
  **Gemeindepunkt-Ebene** — 10.824 amtliche Gemeindepunkte (BKG VG250 `vg250_pk`) mit
  Zensus-2022-Gemeindebevölkerung, SSD über dieselbe Produktfunktion gelesen, die auch
  die Schadensfunktion benutzt (Anlage [72]); die Ressourcen-Regel bleibt gewahrt, ein
  100-m-Vollraster-Lauf findet nicht statt.

  | Aggregation | ΔSSD DE | Rolle |
  |---|---|---|
  | DWD-Gebietsmittel, flächengewichtet [69] | 7,82 % | bis Rev. 2 Berichtswert |
  | Gemeindepunkte, ungewichtet [72] | 7,76 % | **Kontrolle**: bestätigt die Ablesung gegen das Flächenmittel |
  | Gemeindepunkte, **bevölkerungsgewichtet** [72] | **8,51 %** | wirksamer Wert des Produktionsmodells |

  Korrektur **+8,8 %**. Ursache: Die einwohnerstarken Länder haben überdurchschnittliche
  Zuwächse (NRW 9,63 % · Niedersachsen 9,09 % · Hessen 8,57 %), die dünn besiedelten
  Nord-/Nordostländer unterdurchschnittliche (Mecklenburg-Vorpommern 4,79 % ·
  Schleswig-Holstein 5,29 %). Regionswerte bevölkerungsgewichtet [72]:
  **Nord +7,82 % · Mitte +9,15 % · Süd +7,77 %** — das sind **Berichts- und Prüfgrößen**
  (Beispielzelle, Sanity-Anker), **keine** Produktionsgrößen: Die Fallback-Kette des
  Produkts kennt keine Regionsstufe (Zelle → Bundesland → Deutschland) und bleibt
  bewusst flächengewichtet (§3.6).
- **\(k_{\text{UV}}\) = 0,7119 (Band 0,3622–1,0616)** — Brücke über die
  **Globalstrahlung**, beide Quotienten aus dem **Volltext** von [31] bzw. eigener
  Rastermessung (Anlage [73]; Befunde 230/238/245/252/255/256, Log 23–26).

  *Das Skalenproblem.* Der Dosistrend **+4,9 %/Dekade** (H_er,day Dortmund 1997–2022,
  [31] Tab. 2, SE 1,8) ist eine **Stations**messung; das Modell wendet
  \(k_{\text{UV}}\) auf die **Raster**-ΔSSD der Zelle an. Die Skalen unterscheiden
  sich **metrikabhängig** — belegt an der Messzelle selbst. Wichtig: [31] misst
  Globalstrahlung und Sonnenscheindauer **nicht in Dortmund**, sondern an der
  DWD-Station **1117 Bochum** („10 km from the UV monitoring station"); der
  Rasterquotient gehört deshalb an die Bochumer Zelle (Befund 252):

  | Größe | Station ([31] Tab. 4) | 1-km-Raster an der Messzelle [73] | Raster ÷ Station |
  |---|---|---|---|
  | Globalstrahlung GR_int | 4,6 %/Dek. | **4,51 %/Dek.** | **0,98** |
  | Sonnenscheindauer SunD | 11,3 %/Dek. | **6,62 %/Dek.** | **0,59** |

  Das Raster gibt die Globalstrahlung **nahezu exakt** wieder, die Sonnenscheindauer
  nur zu 59 %. Die Quelle nennt den physikalischen Grund: GR ist von Aerosol-optischer
  Dicke und Bewölkung bestimmt, SunD **allein** von Bewölkung — die
  Rasterinterpolation glättet die Schwellenwertgröße SunD stärker als die
  Energiegröße GR. Eine direkte Paarung Stations-Zähler ÷ Raster-SSD-Nenner wäre
  deshalb ein **Kategorienfehler** (§3.9).

  *Die Brücke.* Die **Globalstrahlung liegt in beiden Messfamilien vor**:

  $$ k_{\text{UV}} = \left.\frac{\Delta\text{Dosis}}{\Delta\text{Global}}\right|_{\text{Station}} \times \left.\frac{\Delta\text{Global}}{\Delta\text{SSD}}\right|_{\text{Raster}} = \frac{4{,}9}{4{,}6} \times 0{,}6683 = 1{,}0652 \times 0{,}6683 = \mathbf{0{,}7119} $$

  Beide Quotienten sind **skalenfrei** — je zwei Größen derselben Messfamilie. Beim
  Stationsquotienten liegen die beiden Messorte allerdings **10 km** auseinander
  (UV-Dosis Dortmund, GR Bochum); die Quelle bildet den Quotienten selbst so.
  **Gekennzeichnete Annahme (Befund 267):** Die Bewölkungsentwicklung — der laut
  Quelle dominante Treiber beider Reihen — ist über diese Distanz gleich. Das ist
  auf der Skala synoptischer Bewölkung plausibel, aber nicht belegt. Der **Stationsquotient 1,0652** ist jetzt aus dem Volltext **beziffert**
  ([31] Tab. 2 und Tab. 4) und nicht mehr aus einer Relationsangabe geschätzt; er ist
  die quantitative Fassung der Abstract-Aussage „Global radiation increases similarly
  to the UV data".

  **Quelleninterner Widerspruch, benannt statt geglättet (§3.8; Befund 252).** Das
  Abstract von [31] sagt zusätzlich, die Sonnenscheindauer steige „about twice as
  much as global radiation". Die Tabellenwerte derselben Arbeit ergeben jedoch
  11,3 / 4,6 = **2,46**, nicht 2,0; umgekehrt entspräche „twice" einem
  Globalstrahlungstrend von 5,65 %/Dek. statt der in Tab. 4 publizierten 4,6.
  Der Bericht folgt durchgängig den **bezifferten Tabellenwerten** (Tab. 2: Dosis
  4,9; Tab. 4: Global 4,6, SunD 11,3), nicht der gerundeten Prosaangabe — das ist
  die Lesart, die §3.9 verlangt („Übernommen: exakte Fundstelle, Originalwert mit
  Einheit"). Für den Stationsquotienten ist der Widerspruch ohne Wirkung: Er
  stammt seit Rev. 9 aus Tab. 2 ÷ Tab. 4 und nicht mehr aus einer Relationsangabe. Der **Rasterquotient 0,6683** ist über 10.682 Gemeindepunkte
  mit **Baseline-Fällen × \(\Delta\text{SSD}_{\text{Normalperiode}}\)** gewichtet —
  also mit der Größe, die das Produktionsmodell summiert
  (\(\Delta F = \sum_z F_z \cdot \text{BAF} \cdot \Delta\text{Dosis}_z\)).
  Beide Gewichtungsfragen sind ergebnisrelevant: Mit dem SSD-**Trend** 1997–2022 statt
  der Normalperioden-ΔSSD ergäbe sich 0,6320, der geführte Wert liegt also **+5,7 %**
  darüber (die beiden SSD-Felder korrelieren nur mit **r = 0,24**, Befund 266); mit **Köpfen** statt Fällen 0,6644, der
  geführte Wert liegt also **+0,6 %** darüber (Befund 278). Beide Sensitivitäten
  stammen aus der Anlage [73], sie werden nicht im Text fortgeschrieben.

  **Gekennzeichnete Näherung (§3.9; Befund 340):** Die Fallgewichte bilden die
  kommunale Altersstruktur über `share_over_65` ab; die Aufteilung innerhalb u65
  und 65+ folgt einem bundesweit konstanten Schlüssel, nicht den fünf Bändern des
  Produktionsmodells — Wirkung gegen reine Kopfgewichtung wie eben beziffert.
  Ebenso ergäben die beiden Entitäten leicht verschiedene Werte
  (MM 0,6674 · C44 0,6689); geführt wird das mit ihrem €-Anteil gewichtete Mittel
  (**€-Anteil MM** = \(\Delta F_{\text{MM}}\cdot(c_{\text{MM}} +
  \lambda_{\text{MM}}\bar L_{\text{MM}}\,\text{VOLY})\div\) Gesamt =
  **0,4316**, hergeleitet, nicht gesetzt — Befund 290/348), die Restdifferenz von
  < 0,2 % ist gegen das Band (±49 %) vernachlässigbar. An der Messzelle allein:
  0,6811.

  **Aggregationsregel (§3.9; Befund 338).** \(q\) ist das mit diesen Fällen
  **gewichtete Mittel der Punktquotienten** \(q_z = \Delta\text{Global}_z /
  \Delta\text{SSD}_z\) — nicht der Quotient getrennt summierter Zähler und
  Nenner. Damit schlagen Punkte mit verschwindendem SSD-Trend voll durch: Ihr
  Quotient ist numerisch instabil, nicht klein. Ausgeschlossen werden deshalb
  Punkte mit einem SSD-Trend < 1 %/Dekade — eine **gekennzeichnete Abschätzung**,
  deren Ergebnis-Sensitivität die Anlage [73] als Schwellenreihe ausweist (ohne
  Ausschluss +2,4 %, ab 0,25 %/Dek. bereits +0,2 %).

  **Punktmengen-Kette (Befund 338).** Alle Stufen sind in den Anlagen gemessen,
  nicht fortgeschrieben. Sie erklärt zugleich, warum die beiden Kalibrierläufe
  unterschiedlich viele Punkte führen:

  | Stufe | Punkte | verwendet in |
  |---|---|---|
  | amtliche Gemeindepunkte, BKG VG250 `vg250_pk` (Gebietsstand 01.01.2025) | **10.949** | — |
  | davon mit Zensus-2022-Einwohnerzahl (96 ohne) | **10.853** | — |
  | davon mit SSD-Rasterwert (29 ohne) | **10.824** | ΔSSD-Lauf, Anlage [72] |
  | davon mit auswertbaren Trendreihen in **beiden** Rastern | **10.739** | k_UV-Lauf, Anlage [73] |
  | davon nach Stabilitätsausschluss (SSD-Trend ≥ 1 %/Dek.) | **10.682** | \(q\) und Perzentile der Modellgrenze 9 |

  Der ΔSSD-Lauf braucht nur das SSD-Raster und führt deshalb mehr Punkte als der
  k_UV-Lauf, der beide Raster paart.

  **Band = publizierte Messunsicherheit (§3.9; Befunde 255/256).** SE(Dosis) = 1,8 auf
  4,9 = 36,7 %; SE(Global) = 1,5 auf 4,6 = 32,6 %; unkorreliert fortgepflanzt
  **±49,1 %** (1 σ) ⇒ **0,3622–1,0616**. Das ist die konservative Fassung: Beide
  Reihen sind bewölkungsgetrieben und positiv korreliert, die reale Unsicherheit des
  Quotienten ist kleiner. Bis Rev. 6 kam das Band aus Min/Max über acht handverlesene
  Städte — eine *räumliche* Streuung, fälschlich als Band der *Bundes*summe gebucht.
  Die räumliche Streuung ist jetzt **Modellgrenze 9**, nicht Bandquelle.

  **Korrekturhistorie.** Rev. 3: 0,8434 (Nenner = NRW-*Gebietsmittel*, Skalen-Mismatch,
  Befund 230). Rev. 4: 0,7562 (Nenner rasterskaliert, Zähler weiter Station — halber  <!--hist-->
  Mismatch, Befund 238). Rev. 5: 0,5782 (Brücke, Stationsquotient aus „roughly twice" <!--hist-->
  geschätzt). Rev. 6: 0,6667 (Stationsquotient aus „similarly" als 1,0 gelesen).  <!--hist-->
  Rev. 7: 0,6735 (Stationsquotient aus dem Volltext **beziffert**, Rasterquotient  <!--hist-->
  bevölkerungsgewichtet). Rev. 8: 0,7216 (Gewichtung auf die Normalperioden-ΔSSD,  <!--hist-->
  Befund 266). Rev. 9: 0,7289 (Fallgewichtung, Befund 278). Rev. 11: **0,7119**  <!--hist-->
  (Aggregationsregel — instabile Punkte ausgeschlossen, Befund 297).
  **Alle acht Werte liegen innerhalb des ausgewiesenen Bandes 0,3622–1,0616.**
  Plausibilisierung: implizite Dosisänderung DE = 8,51 % × 0,7119 ≈ 6,06 % über den
  Normalperiodenversatz ≈ 2,02 %/Dekade — innerhalb des Satelliten-Bands
  +1,2–3,6 %/Dekade [32] ✓.
- **Stationaritätsannahme der Elastizität (gekennzeichnet, Befund 222):**
  \(k_{\text{UV}}\) ist im Fenster **1997–2022** gemessen und wird auf den
  **Normalperiodenversatz 1961–90 → 1991–2020** angewendet — unterstellt ist also eine
  über die Zeit konstante Elastizität Dosis/SSD. Das ist keine Selbstverständlichkeit:
  **Korrektur (Befund 246):** Bis Rev. 5 stand hier, das Messfenster 1997–2022 liege
  »in der Ozon-Erholung«, woraus eine Unterschätzung folge. Die eigene Primärquelle
  misst am selben Ort jedoch einen **signifikanten sommerlichen Ozonrückgang von
  0,9 %/Dekade im Messfenster** [31] — die Ozonentwicklung wirkte dort also
  **dosiserhöhend**, nicht dämpfend. Damit kehrt sich die Richtung um: Die im Fenster
  gemessene Elastizität enthält einen Ozonbeitrag, den der Normalperiodenversatz nicht
  in gleicher Weise trägt ⇒ ΔDosis wird eher **überschätzt**. Die Größenordnung
  (0,9 gegen 6,62 %/Dek. SSD an der Messzelle) ist klein gegen das k_UV-Band
  (**±49 %**), die Richtungsangabe ist aber zu korrigieren und die
  Untergrenzen-Zusage insoweit einzuschränken. Das Band **0,3622–1,0616** deckt die
  Spanne ab; Ersetzungspfad: Dosisrekonstruktion mit Ozon-/Wolken-Zerlegung aus
  Reanalysen (derselbe Pfad wie für \(a_{\text{attr,UV}}\)).
- **\(a_{\text{attr,UV}}\) = 0,75 (Band 0,5–1,0)** — GP-Befund-15-Auflösung (Log 3):
  Attributionsfaktor analog zur #96-Logik (dort 0,50, gemessen [9]); für UV existiert
  keine Attributionsstudie — **gekennzeichnete Abschätzung**: Lorenz nennt als
  Trendursache „v. a. Bewölkungsabnahme" (klimasystemische Größe → hoher Wert), das
  Aerosol-„Brightening" seit den 1980ern ist anthropogen, aber keine Klimawirkung im
  KWRA-Sinn (→ < 1,0). Zentral 0,75, beide Grenzen im Band; Ersetzungspfad:
  Wolken-/Aerosol-Zerlegung aus Reanalysen.
- Resultierende \(\Delta\text{Dosis}\) (Basiswerte): **DE 4,54 %** · Nord 4,17 % ·
  Mitte 4,89 % · Süd 4,14 %.

```python test: beispiel_98_klimasignal
# k_UV uebersetzt eine relative SSD-Aenderung in eine relative Dosisaenderung.
# Zaehler (Stationsmessung der Dosis) und Nenner (Raster-SSD der Zelle) stammen
# aus zwei Messfamilien; die Globalstrahlung liegt in BEIDEN vor und traegt
# deshalb die Bruecke. Beide Quotienten sind skalenfrei, ihr Produkt ist die
# Elastizitaet auf RASTERskala (Ledger-Befunde 230/238/252).
# Stationsquotient 4,9/4,6 = 1,0652 aus [31] Tab. 2 und Tab. 4 (Volltext).
# Rasterquotient 0,6683, gewichtet mit Baseline-Faellen x DeltaSSD_Normalperiode
# ueber 10.682 Gemeindepunkte (Befunde 266/278).
k_uv = (4.9 / 4.6) * 0.6683
assert abs(k_uv - 0.7119) < 0.0001
# Metrikabhaengigkeit an der Messzelle Bochum: Raster/Station betraegt bei der
# Globalstrahlung 0,98, bei der Sonnenscheindauer nur 0,59 — die Skalendifferenz
# haengt an der METRIK, nicht an der Glaettung.
assert abs(4.51/4.6 - 0.98) < 0.01 and abs(6.62/11.3 - 0.59) < 0.01
# Band = publizierte Standardfehler (Befunde 255/256), die EINZIGE geltende
# Bandkonstruktion; die frueher aus Stations-/Rasterextremen gerechneten
# Bandstuetzen sind seit Rev. 7 abgeloest (Befund 336d).
# Band = publizierte Standardfehler (Befunde 255/256): SE 1,8/4,9 und 1,5/4,6,
# unkorreliert fortgepflanzt = +/-49,1 % (1 sigma).
rel = ((1.8/4.9)**2 + (1.5/4.6)**2) ** 0.5
assert abs(rel - 0.491) < 0.002
assert abs(k_uv*(1-rel) - 0.3622) < 0.001 and abs(k_uv*(1+rel) - 1.0616) < 0.001
# Quellen-Widerspruch (§3.8): Stations-SSD 11,3 %/Dek. [31] = Faktor 1,74 ueber
# dem Raster am selben Ort; daraus die untere Bandstuetze.
# Befund 223: BEVOELKERUNGSgewichtete Delta-SSD (Anlage ssd_povw.csv, Gemeindepunkte) —
# das Produktionsmodell summiert bevoelkerungsgewichtet ueber Zellen, nicht flaechengewichtet.
dssd = {"nord": 7.82, "mitte": 9.15, "sued": 7.77, "de": 8.51}
soll = {"nord": 4.17, "mitte": 4.89, "sued": 4.14, "de": 4.54}
for r, v in dssd.items():
    assert abs(v/100 * k_uv * 0.75 * 100 - soll[r]) < 0.01
# Die flaechengewichteten Werte bleiben die Kontrollgroesse: ungewichtetes
# Gemeindepunkt-Mittel 7,76 % liegt am DWD-Gebietsmittel 7,82 % (Ablesung unverzerrt),
# die Bevoelkerungsgewichtung hebt den Wert um knapp 9 %.
assert abs(7.76 / 7.82 - 1) < 0.01
assert abs(8.51 / 7.82 - 1 - 0.088) < 0.002
# Plausibilisierung: implizite Dosisaenderung im Satelliten-Rahmen (1,2-3,6 %/Dekade x ~3 Dekaden Versatz)
assert 1.2 * 3 * 0.5 <= 8.51 * k_uv <= 3.6 * 3   # 6,2 % zwischen 1,8 und 10,8
```

### 3.3 Baseline-Fälle: altersspezifische Inzidenz (Anker `#i-raten`)

$$ F_{e,\text{Zelle}} \;=\; c_{\text{kal},e} \cdot \sum_a \text{pop}_a \cdot \frac{I_{e,a}}{100\,000} $$

**Ablesekette \(I_{e,a}\)** (Log 5; §3.9 „Abgeschätzt" mit Messanker — dieselbe Ablese-Kette
wie die #95-ERF-Steigungen aus Winklmayr-Abb. 3): Die altersspezifischen
Neuerkrankungsraten sind in KID 2025 nur als Abbildungen publiziert (Abb. 3.13.2 C43,
Abb. 3.14.3 C44; je 100.000, 2021–2023, nach Geschlecht); die ZfKD-Datenbankwerte sind
nicht keyless abrufbar (dokumentierte Datenlücke; Ersetzungspfad: ZfKD-Abfrage vor
Integration). **Roh-Ablesewerte je 5-Jahres-Gruppe und Geschlecht** (Ablese-Toleranz
±15 %, gitterlinien-gestützt): vollständig in der Anlage
`backend/data/kalibrierung/kid2025_ablesewerte.csv` (Befund 204); Auszug (F/M je 100.000):
C43: 20–24: 5/2 · 40–44: 25/16 · 60–64: 42/52 · 75–79: 66/120 · 85+: 61/140;
C44: 40–44: 90/55 · 60–64: 315/350 · 75–79: 865/1.420 · 85+: 1.100/2.190.

Aggregation auf die Produktbänder mit **geschlechtsspezifischen Bevölkerungsgewichten**
(Bevölkerung 31.12.2023 nach Altersjahren und Geschlecht, Tab. 12411-06 [48] — ersetzt die
frühere 50/50-Annahme, Befund 204). **Roh-Bandraten** (unnormiert):

| \(I_{e,a}^{\text{roh}}\) je 100.000 | u20 | 20–64 | 65–74 | 75–84 | 85+ | gewichtete Roh-Rate vs. amtliche Rohrate 2021–2023 |
|---|---|---|---|---|---|---|
| MM (C43) | 0,5 | 24,7 | 64,0 | 94,9 | 88,5 | 32,16 vs. 32,20 (**−0,1 %**) |
| C44 | 2,0 | 125,9 | 617,6 | 1.267,2 | 1.479,5 | 291,36 vs. 288,74 (**+0,9 %**) |

**Ablesegrenze (Befund 212, gekennzeichnet):** Für u20 (beide Entitäten) und C44 20–29
liegen die Balken unter der Ablesegrenze der Abbildungen (< ≈ 15 je 100.000 bei
Achse 0–2.500); angesetzt sind **0,5** (MM u20, Band 0–5), **2,0** (C44 u20, Band 0–5)
und **5** (C44 20–24/25–29, Band 0–15) — gekennzeichnete Abschätzungen mit < 0,3 %
Wirkung auf die Bundes-Baseline; die Bandmittelung läuft über die **volle**
Band-Bevölkerung (20–64 inkl. der 20–29-Jährigen).

**Anker-Fenster und Revisionsstand (Befund 220; Log 16).** Die Abbildungen 3.13.2/3.14.3
tragen den Titel „Altersspezifische Neuerkrankungsraten …, Deutschland **2021 – 2023**":
Die abgelesenen Raten sind über drei Jahre **gepoolt**. Der Anker ist deshalb dasselbe
Fenster — das arithmetische Mittel der drei Jahresfallzahlen aus Tab. 3.13.1/3.14.1
(einheitliche Jahres-Auswahlregel, §3.4); ein Einzeljahres-Anker (Rev. 1: 2023) hätte
gepoolte Raten an einem Einzeljahr normiert und damit Zähler und Nenner in verschiedenen
Fenstern geführt. Revisionsstand: KID 2025 (Publikationsstand 2025); die
Neuerkrankungszahlen sind **vollzähligkeitskorrigierte Schätzungen** des ZfKD
(„In 2023 sind in Deutschland **geschätzt** knapp 243.000 Personen … erkrankt", Kap. 3.14)
— kein Jahr ist als vorläufig ausgewiesen, die Drei-Jahres-Mittelung ist zugleich die
Absicherung gegen die Restunsicherheit des jüngsten Registerjahrs.

| Anker (Neuerkrankungen) | 2021 | 2022 | 2023 | **Mittel = Anker** |
|---|---|---|---|---|
| MM (C43) | 26.140 | 27.040 | 27.430 | **26.870** |
| C44 | 236.670 | 243.430 | 242.820 | **240.973** |

**Normierungsskalare (= Kalibrierung, §3.4-konform genau ein Skalar je Entität; wirken in
der Formel — die Tabellenwerte sind Rohwerte, Befund 201):**
\(c_{\text{kal,MM}}\) = 26.870/26.837 = **1,0012** · \(c_{\text{kal,C44}}\) =
240.973/243.158 = **0,9910** — damit reproduziert die Bundes-Baseline den
ZfKD-Anker 2021–2023 auf der Bezugspopulation der Normierung. Ablese-Toleranz
(vorab fixiert): ±15 % vor Normierung — **bestanden** (−0,1 % / +0,9 %; Rev. 1 gegen
das Einzeljahr 2023: −2,2 % / +0,1 %). Rechenweg reproduzierbar in der Anlage
`backend/scripts/kalibrierung/kid2025_baseline.py` [71].

**Bezugspopulation der Normierung — gekennzeichnete Näherung (§3.9; Befund 226;
Log 21).** Der Nenner von \(c_{\text{kal},e}\) ist die amtliche **Fortschreibung
31.12.2023** (83.456.045 Personen, Tab. 12411-06 [48]) — dieselbe Quelle, aus der auch
die geschlechts- und altersjahresgenauen Bandgewichte stammen. Das Produkt wendet die
Bandraten dagegen auf die **Zensus-2022-Zellbevölkerung** an (Zeichentabelle
\(\text{pop}_a\)); deren Gemeinde-Aggregat im Produkt summiert sich auf 82.459.764.
Die Produktions-Baseline liegt damit um **−1,19 %** unter dem Anker — Richtung:
Unterschätzung, konsistent zur Untergrenzen-Zusage, aber nicht „exakt". Die
Bandgewichte bleiben bewusst auf der Fortschreibung, weil nur sie altersjahresgenau
und geschlechtsspezifisch vorliegt; die Restdifferenz der Altersverteilung zwischen
den beiden Stichtagen (15.05.2022 ↔ 31.12.2023) ist zweiter Ordnung. **Kopplung
(§3.9):** Ändert sich die Zensus-Basis des Produkts, ist \(c_{\text{kal}}\) neu zu
rechnen. **Ersetzungspfad:** \(c_{\text{kal}}\) gegen die amtlichen
Zensus-2022-Altersgruppen, sobald sie als Tabelle (nicht als Zellraster) vorliegen —
ein nationaler Zell-Lauf zur Bestimmung der Bandsummen ist nach §3.4 unzulässig —
**und wäre auch inhaltlich untauglich** (Befund 237): Die Zensus-100-m-Altersbänder
sind wegen der Geheimhaltungsunterdrückung (< 3) nicht additiv zur
Gesamtbevölkerung und decken nur ≈ 89,8 % ab (Fundstelle: Modulkommentar über
`zensus_loader.AGE_BAND_COLUMNS`; `AGE_BAND_MIN_COVERAGE` = 0,5 ist die daraus
abgeleitete Rückfallschwelle, nicht die Deckungszahl) — eine nationale Bandsumme aus dem Raster
wäre also selbst dann verzerrt, wenn man sie rechnen dürfte. Der Beschaffungsstand
der amtlichen Zensus-2022-Altersgruppentabelle wird als **Datenlücke mit
Beschaffungs-Watchlist** geführt (§3.8). Die naheliegende reine **Niveau**-Korrektur
(\(c_{\text{kal}} \times 83.456.045/82.459.764\)) wird **verworfen**, weil das
Produkt-Aggregat selbst 0,31 % unter der amtlichen Zensus-2022-Bevölkerung liegt: Sie
ersetzte eine benannte Näherung durch eine unbelegte Skalierung, ohne den
Altersstruktur-Anteil der Differenz zu treffen.

```python test: beispiel_98_baseline_normierung
# Roh-Bandraten x c_kal reproduzieren den Anker 2021-2023 (Befunde 201/220)
pop = {"u20": 15_583_456, "20-64": 49_163_992, "65-74": 9_569_640,
       "75-84": 6_294_744, "85+": 2_844_213}
i_mm  = {"u20": 0.5, "20-64": 24.7, "65-74": 64.0, "75-84": 94.9, "85+": 88.5}
i_c44 = {"u20": 2.0, "20-64": 125.9, "65-74": 617.6, "75-84": 1267.2, "85+": 1479.5}
mm_roh  = sum(pop[b] * i_mm[b]  / 1e5 for b in pop)
c44_roh = sum(pop[b] * i_c44[b] / 1e5 for b in pop)
assert abs(mm_roh - 26_837) < 60 and abs(c44_roh - 243_158) < 600
# Anker = Mittel der drei gepoolten Ablesejahre (KID 2025 Tab. 3.13.1/3.14.1)
anker_mm  = (26_140 + 27_040 + 27_430) / 3
anker_c44 = (236_670 + 243_430 + 242_820) / 3
assert abs(anker_mm - 26_870) < 1 and abs(anker_c44 - 240_973) < 1
assert abs(anker_mm / mm_roh - 1.0012) < 0.0003     # c_kal,MM
assert abs(anker_c44 / c44_roh - 0.9910) < 0.0003   # c_kal,C44
assert abs(mm_roh * 1.0012 - anker_mm) / anker_mm < 0.005
assert abs(c44_roh * 0.9910 - anker_c44) / anker_c44 < 0.005
# Ablese-Toleranz +/-15 % auf der ROHEN Rate (in-sample) ...
p_de = sum(pop.values())
assert abs(mm_roh / anker_mm - 1) < 0.15 and abs(c44_roh / anker_c44 - 1) < 0.15
assert abs(mm_roh / p_de * 1e5 - 32.16) < 0.05      # amtlich 32,20 => -0,1 %
assert abs(c44_roh / p_de * 1e5 - 291.36) < 0.05    # amtlich 288,74 => +0,9 %
```

```python test: beispiel_98_struktur_validierung
# Befund 214: Altersstandardisierte Rate (alter Europastandard) aus der Ablesekette
# gegen KID 2025 Tab. 3.13.1/3.14.1 - OUT-OF-SAMPLE gegenueber c_kal, weil die
# Normierung die ROHE Rate fittet und die ASR anders altersgewichtet.
eurostd = {"0-19": 29_000, "20-24": 7_000, "25-29": 7_000, "30-34": 7_000,
           "35-39": 7_000, "40-44": 7_000, "45-49": 7_000, "50-54": 7_000,
           "55-59": 6_000, "60-64": 5_000, "65-69": 4_000, "70-74": 3_000,
           "75-79": 2_000, "80-84": 1_000, "85+": 1_000}
assert sum(eurostd.values()) == 100_000
# Ablesewerte (Anlage kid2025_ablesewerte.csv), Frauen/Maenner je 5-Jahres-Gruppe
mm_f  = [0.5, 5, 10, 14, 19, 25, 32, 39, 41, 42, 46, 57, 66, 69, 61]
mm_m  = [0.5, 2, 5, 9, 12, 16, 21, 32, 43, 52, 68, 91, 120, 142, 140]
c44_f = [2.0, 5, 5, 25, 60, 90, 140, 195, 265, 315, 430, 650, 865, 1065, 1100]
c44_m = [2.0, 5, 5, 15, 30, 55, 95, 165, 245, 350, 555, 905, 1420, 1905, 2190]
w = list(eurostd.values())
asr = lambda r: sum(wi * ri for wi, ri in zip(w, r)) / 100_000
# amtlich, Mittel 2021-2023 (alter Europastandard)
soll = {"mm_f": (20.7 + 21.0 + 21.1) / 3, "mm_m": (22.3 + 22.9 + 22.9) / 3,
        "c44_f": (139.0 + 142.8 + 143.8) / 3, "c44_m": (173.7 + 175.8 + 172.7) / 3}
ist = {"mm_f": asr(mm_f), "mm_m": asr(mm_m), "c44_f": asr(c44_f), "c44_m": asr(c44_m)}
# Abnahmetoleranz HERGELEITET (Befund 229a/234/240): 2 sigma aus der Ablese-
# genauigkeit, OHNE Aufrundung — sigma = 0,15 x sqrt(sum(w_i r_i)^2)/sum(w_i r_i)
# ergibt im unguenstigsten der vier Reihen 5,07 % => 2 sigma = 10,1 %.
for k in soll:
    assert abs(ist[k] / soll[k] - 1) < 0.101, (k, ist[k], soll[k])
# Regressionsschranke +/-3 % (Befund 229): enger als die Abnahmetoleranz, damit
# eine Verschlechterung der Ablesekette auffaellt, lange bevor 2 sigma reisst.
assert max(abs(ist[k] / soll[k] - 1) for k in soll) < 0.03   # Ist-Ergebnis: max 1,9 %
```

### 3.4 Klimaattribuierter Zusatz, Mortalität, Monetarisierung

$$ \Delta F_{e,\text{Zelle}} \;=\; F_{e,\text{Zelle}} \cdot \text{BAF}_e \cdot \Delta\text{Dosis}_{\text{Zelle}}, \qquad \text{YLL}_{\text{Zelle}} = \sum_e \Delta F_{e,\text{Zelle}} \cdot \lambda_e \cdot \bar L_e $$

**Gekennzeichnete Approximation (Befund 210, analog GP-Befund 43):** der relative Exzess
wird auf die bereits dosiserhöhte Baseline des Ankerfensters 2021–2023 angewendet; der
attributable Anteil wäre exakt
\(\text{BAF} \cdot \Delta D / (1 + \text{BAF} \cdot \Delta D)\) — Richtung:
Überschätzung um **+2,73 %** (MM) bzw. **+7,61 %** (C44) — nachgerechnet aus
\(\text{BAF}\cdot\Delta D\) gegen \(\text{BAF}\cdot\Delta D/(1+\text{BAF}\cdot\Delta D)\)
mit ΔDosis 4,5436 %; beide innerhalb der Bänder (Befund 359).

**Gekennzeichnete Annahme — unstratifizierte Elastizität (§3.2; Befund 367).**
Die Baseline ist über fünf Altersbänder geschichtet, der BAF wirkt aber
**unstratifiziert** auf die Bandsumme: Es gilt dieselbe relative Elastizität in
allen Bändern. Neutral ist das nicht — die τ-Rechnung unten zeigt, dass die
Lebenszeitdosis-Elastizität mit dem Alter fällt (\(\tau=(T/2)/a\)), und MM mit
einem Erkrankungsalter von 63–69 Jahren trägt 64 % der YLL. Eine altersgeschichtete
Elastizität würde den MM-Pfad also eher anheben, den C44-Pfad eher senken. [30]
veröffentlicht keine bandweisen BAF; die Annahme bleibt bis dahin bestehen und ist
über das BAF_MM-Band (±67 % auf den MM-Pfad) mit abgedeckt. **Ersetzungspfad:**
bandweise BAF, sobald eine Quelle sie beziffert.

**Kumulative Dosis → jährliche Umgebungsdosis: die Gleichgewichtslesart
(§3.9; Befunde 247/336f).** Die BAF sind in der Primärquelle [30] als Exponenten
der **Lebenszeit**dosis definiert (\(Y(a) \sim \Phi(a)^{c}\) mit \(\Phi\) =
kumulierte Dosis bis zum Alter \(a\)); \(\Delta\text{Dosis}\) misst dagegen
die Änderung der **jährlichen** Umgebungsdosis. Der Übergang ist ein eigener
Rechenschritt und wird ausdrücklich als Annahme geführt:

> Steigt die jährliche Dosis dauerhaft um \(\Delta D\), so steigt auch die
> Lebenszeitdosis jeder Kohorte um \(\Delta D\) — dann, und nur dann, gilt
> \(\Delta Y/Y = \text{BAF}\cdot\Delta D\) unverändert. Das ist die
> **Gleichgewichtslesart**: ausgewiesen wird das *eingelaufene* Risiko einer
> dauerhaft erhöhten Dosislage, nicht der in diesem Jahr klimabedingt
> entstandene Fallzuwachs.

Gegenüber einer Jahres-Attribution ist das eine **Überschätzung**, weil die Dosis
erst über den Normalperiodenversatz gestiegen ist: Die heute erkrankenden
Kohorten haben den größten Teil ihrer Lebenszeitdosis vor dem Anstieg
akkumuliert. **Abschätzung des Transient-Faktors** \(\tau\) (gekennzeichnete
Abschätzung, §3.9): Steigt die Jahresdosis über \(T\) Jahre linear um
\(\Delta D\) und war davor konstant, ist die kumulative Dosis einer Person im
Alter \(a \ge T\) um die Dreiecksfläche erhöht:

$$ \tau \;=\; \frac{\Delta\Phi/\Phi}{\Delta D/D} \;=\; \frac{T/2}{a} $$

Maßgeblich ist das **Erkrankungs**alter, nicht das Sterbealter: \(Y(a)\) ist die
Inzidenz im Alter \(a\). Nach [27] liegt der Median bei MM 63–69 und C44 74–76
Jahren. Mit dem Mittelpunktabstand der Normalperioden \(T = 30\) Jahre folgt
\(\tau \approx 0{,}20\text{–}0{,}24\); selbst bei doppelt so langem
Anstiegsfenster (\(T = 60\)) bleibt \(\tau \le 0{,}48\).
**Spanne: 0,20–0,48** — weit
außerhalb des \(k_{\text{UV}}\)-Bandes (±49 %) und damit die **größte**
Einzelunsicherheit des Modells; sie ist als eigene Achse in der §4-Bändertabelle
geführt.

*Abweichung zur Review-Schätzung benannt (§3.8):* Befund 247 veranschlagte
\(\tau \approx 0{,}4\text{–}0{,}7\). Die hier ausgeschriebene Integration
ergibt einen kleineren Wert; die Differenz stammt daraus, dass der volle
Normalperiodenversatz von 30 Jahren gegen ein Erkrankungsalter von 63–76
Jahren steht — der Review hatte hier zusätzlich das Sterbealter angesetzt. Der Bericht führt die eigene, offengelegte Rechnung.

Der **Ausweis bleibt bewusst die Gleichgewichtslesart** (\(\tau = 1\)), weil sie
die politisch relevante Größe ist — das bereits eingelaufene Risiko der heutigen
Dosislage. \(\tau\) beziffert, wie weit eine reine Jahres-Attribution darunter
läge.

$$ \text{€}_{\text{Zelle}} \;=\; \sum_e \Delta F_{e,\text{Zelle}} \cdot c_e \;+\; \text{YLL}_{\text{Zelle}} \cdot \text{VOLY}, \qquad \text{Kommune} = \sum_{\text{Zellen}} $$

- **\(\lambda_e\)** = Sterbefälle ÷ Neuerkrankungen, **beide im Ankerfenster 2021–2023**
  [27] (Befund 220): MM 3.081,0/26.870 = **0,11466**; C44 1.261,7/240.973 = **0,005236**
  — **Perioden-Approximation, gekennzeichnet** (GP-Befund 43): bei steigender Inzidenz
  keine Kohorten-Letalität; Richtung: Überschätzung des Mortalitätsanteils.
  (Sterbefälle je Jahr, F+M: MM 2.928/3.146/3.169; C44 1.178/1.275/1.332.)
- **\(\bar L_e\)** = \(e(\text{medianes Sterbealter})\), sterbefallgewichtet über
  **alle Jahre und Geschlechter des Ankerfensters** [27,48] (Befund 224; Log 20):
  MM **10,4569 J.** · C44 **5,4787 J.** — **Median-Approximation, gekennzeichnet**
  (GP-Befund 43): bei rechtsschiefer Sterbealter-Verteilung leicht überschätzend.
  Bis Rev. 2 standen hier 10,58 / 5,30 aus den Sterbealtern des **Einzeljahrs 2023**,
  begründet mit einer Konstanz über 2021–2023, die die Quelle nicht hergibt:
  Tab. 3.13.1/3.14.1 weisen für Männer 76/**77**/76 (MM) und 84/84/**85** (C44) aus.
  Damit lief \(\bar L_e\) auf einer anderen Jahres-Auswahlregel als Anker,
  \(c_{\text{kal}}\) und \(\lambda_e\) (§3.4 „einheitliche Jahres-Auswahlregel";
  §3.9 Kopplung bei Änderung der Basis). Stützstellen der Sterbetafel 2022/2024 [48]:
  e(78)F = 10,9187 · e(76)M = 10,3350 · e(77)M = **9,7311** · e(88)F = 5,0374 ·
  e(84)M = **5,9397** · e(85)M = 5,4745. Wirkung: MM −1,16 %, C44 **+3,37 %**,
  YLL netto +0,5 %.
- **\(c_e\)** (Log 7; Register 98-K1-01): Basis = Erstjahreskosten **SCS-detektierter**
  Fälle (Speckemeier [34], Kohorte 2014/2015, Preisstand-Annahme 2015):
  MM 5.326 × 119,3/94,5 = **6.724 €₂₀₂₄** (Band bis 11.410 = nicht-SCS-detektiert);
  C44 4.660 ⇒ **5.883 €₂₀₂₄** (Band bis 7.436). **Proxy-Kennzeichnung** (§3.1) mit
  Richtungsdiskussion: *überschätzend* — Gesamt- statt inkrementelle Kosten (enthält
  Grundversorgung der überwiegend alten Patienten); *unterschätzend* — nur Erstjahr
  (Folgejahre, Metastasen-Therapien fehlen), SCS-Werte als untere Detektionsweg-Stütze.
  Die Basiswert-Wahl folgt der Untergrenzen-Zusage (#95-Befund-62-Lehre).
- **VOLY = 160.800 €₂₀₂₄** (MK 4.0/P52; Kette in #95 §3.5 [19]); VSL nur Sensitivität.
  **Konsistenz-Check VSL ÷ VOLY (§3.2; Befund 217):** Die Fortschreibung P52 führt
  VSL 3,5 / 4,7 / 6,19 Mio €/Todesfall als Sensitivitäten. Der Quotient ergibt
  **21,8 / 29,2 / 38,5 Lebensjahre** je Todesfall. Dem stehen die hier tatsächlich
  verlorenen Lebensjahre gegenüber: \(\bar L_{\text{MM}}\) = 10,46 und
  \(\bar L_{\text{C44}}\) = **5,48** Jahre. Der VSL unterstellt also das Zwei- bis
  Siebenfache dessen, was bei UV-Schäden real verloren geht — er ist nicht
  altersadjustiert, während die Hautkrebs-Sterbefälle mit medianem Sterbealter 76–88
  Jahren am oberen Ende der Altersverteilung liegen. **Konsequenz (§3.2):** #98 ist der
  altenlastigste Fall der K1-Familie; die YLL-Bewertung fällt hier
  **um Faktor 2,8 (VSL 3,5 Mio) bis 4,9 (VSL 6,19 Mio) niedriger** aus als eine
  Bewertung je Todesfall — nachgerechnet: 180,1 klimaattribuierte Todesfälle × 3,5 Mio
  = 630 Mio € (bzw. 846 bzw. 1.115 Mio € bei VSL 4,7 / 6,19 Mio) gegenüber
  **226 Mio €** im YLL-Pfad. Die **Relation zwischen den Risiken verschiebt sich
  entsprechend**: #98 erscheint gegenüber jung-lastigen Risiken (Extremereignisse,
  Verkehr) systematisch kleiner als unter VSL. Beide Größen stammen aus derselben
  Quelle (MK 4.0/Amann 2020a) mit derselben Preisstand-Anpassung (€2024).
- **Sensitivitätsband \(r_{\text{out}}\)** (nicht im Basiswert; Log 10; GP-Befund 9;
  Formel-Präzisierung Befund 206): der Außenberufs-Modifikator wirkt auf den
  **SCC-Anteil am C44-Zusatz** \(w^Z = w_{\text{SCC}} \cdot 2{,}5 / \text{BAF}_{\text{C44}}
  = 0{,}25 \cdot 2{,}5 / 1{,}675 = 0{,}373\):

  $$ r_{\text{out}} \;=\; (1 - w^Z) + w^Z \cdot \frac{1 + q_{\text{out}} (\text{OR}-1)}{1 + \bar q_{\text{out}} (\text{OR}-1)} $$

  OR = 1,77 [1,37–2,30] [43], \(\bar q_{\text{out}}\) = **0,070** =
  (572 + 2.643)/45.909 Tsd. Erwerbstätige 2023 (Land-/Forstwirtschaft/Fischerei +
  Baugewerbe, VGR [70]; **Proxy**: nicht alle Branchenbeschäftigten arbeiten im Freien,
  Außenberufe anderer Branchen fehlen — beide Richtungen). Mittelwertzentriert
  (Bundesmittel = 1) — verteilungsneutral zur Bundessumme; Beispiel Bau-/Agrar-Kommune
  \(q_{\text{out}}\) = 0,14: **+1,9 %** auf den C44-Zusatz.

  **Bandzuordnung (§3.2; Befund 218).** \(r_{\text{out}}\) wirkt **nur auf die Bänder
  20–64, 65–74, 75–84 und 85+**, nicht auf u20. Begründung: Die Effektgröße stammt aus
  einer Meta-Analyse **beruflicher** Exposition (Schmitt 2011, Grundlage der BK 5103) und
  ist auf den amtlichen **Erwerbstätigen**-Anteil zentriert — für Unter-20-Jährige
  existiert weder eine berufliche Exposition noch eine tragende Fallzahl
  (\(I_{\text{C44,u20}}^{\text{roh}}\) = 2,0 je 100.000 ⇒ < 0,2 % des C44-Zusatzes).
  Für die Bänder 65+ ist die Zuordnung eine **gekennzeichnete Kohorten-Approximation**:
  Beruflich verursachte Plattenepithelkarzinome treten wegen der kumulativen Dosis
  überwiegend nach dem Erwerbsleben auf, der Modifikator verwendet aber den **heutigen**
  Erwerbstätigen-Anteil der Kommune als Stellvertreter für die frühere Exposition
  derselben Kohorte. Richtung: In Kommunen mit schrumpfendem Außenberufs-Sektor
  unterschätzt, in wachsenden überschätzt der Modifikator — bei Aktivierung des Bandes
  zu dokumentieren.

  **Bandgrenzen (§3.9 gilt auch für Bandgrenzen; Befund 219).** Das Band wird als
  \(q_{\text{out}}\)-Spanne geführt und daraus gerechnet, nicht als gesetzte
  \(r_{\text{out}}\)-Spanne:

  | \(q_{\text{out}}\) | 0,00 | 0,070 (\(=\bar q\)) | 0,14 | 0,21 |
  |---|---|---|---|---|
  | \(r_{\text{out}}\) | 0,981 | **1,000** | 1,019 | 1,038 |

  Bandgrenzen **0,981–1,038** = \(q_{\text{out}}\) ∈ [0; 0,21]. Die Obergrenze 0,21
  = **dreifaches Bundesmittel** ist eine **gekennzeichnete Abschätzung** (§3.9): Eine
  belegte kommunale Verteilung der Außenberufs-Anteile existiert nicht, solange die
  Ebene geparkt ist; drei Kommunaltypen stützen die Größenordnung (reine
  Agrar-/Baugemeinden erreichen ein Vielfaches des Bundesmittels, Großstädte liegen
  darunter). Ergebnis-Sensitivität: **−1,9 … +3,8 %** auf den C44-Zusatz, **−1,0 … +2,1 %** auf die €-Summe
  einer Einzelkommune — **null** auf die Bundessumme (Zentrierung). Ersetzungspfad:
  INKAR-Perzentile der Branchenanteile, sobald die Ebene beschafft ist.
- **Sensitivitätsband \(v_{\text{verh}}\)** (Default 1; Log 11/17; Register 98-S154-01;
  Herleitung migriert, Befund 205; Wirkungsort präzisiert, **Befund 216**).
  **Tageswert.** Kette: Outdoor-Freizeit +1,2 min/°C (ATUS, n = 42.280; Basis
  44 min/Tag [57]); ein Komforttag (ΔT ≈ +10 °C) ⇒ +12 min = **+27 %** Außenzeit;
  Zeit-im-Freien erklärt die persönliche Dosis nahezu proportional (R² 0,75–0,79 [59]);
  Kleidungskomponente +15 % (0–35 %, nur Richtung [59]) ⇒ Tages-Mehr-Dosis
  \(s\) ≈ **1,45** (Kernband 1,25–1,60; Hitzetage > 30 °C kehren das Vorzeichen um:
  −5…−13 % Aktivität [58]).
  **Wirkungsort (neu in Rev. 2).** \(s\) ist ein **Tages**wert und darf nicht auf die
  Jahres-\(\Delta\text{Dosis}\) multipliziert werden — der Modellparameter ist deshalb
  der **Jahres**faktor

  $$ v_{\text{verh}} \;=\; 1 + \phi_{\text{Komfort}}\cdot(s-1), \qquad
     \phi_{\text{Komfort}} = \frac{\text{erythemwirksame Jahresdosis an Komforttagen}}{\text{erythemwirksame Jahresdosis gesamt}} $$

  multiplikativ auf \(\Delta\text{Dosis}_{\text{Zelle}}\). \(\phi_{\text{Komfort}}\) ist
  die fehlende Größe: Sie verlangt eine dosisgewichtete Komforttag-Statistik je Zelle
  (Tagesmitteltemperatur-Anomalie **und** Tagesdosis), die das Produkt in M0 nicht führt
  und für die keine keyless Quelle in dieser Kombination vorliegt. Die Ebene ist deshalb
  nach §3.1 **geparkt (Datenquelle fehlt)** mit Beschaffungs-Watchlist
  (DWD-Tagesraster Temperatur × SSD), und der Parameter läuft dokumentiert auf dem
  Neutralwert \(\phi_{\text{Komfort}} = 0\) ⇒ \(v_{\text{verh}}\) = **1** — nicht still.
  Das Registry-Band ist entsprechend der **Jahres**faktor über
  \(\phi_{\text{Komfort}}\) ∈ [0; 0,25] bei \(s\) = 1,45: **1,00–1,11**
  (gekennzeichnete Abschätzung der \(\phi\)-Obergrenze: Komforttage tragen selbst im
  günstigsten Fall nur einen Bruchteil der Jahresdosis, weil die erythemwirksame Dosis
  in DE zu ≈ 70 % auf Mai–August entfällt und dort nicht jeder Tag ein Komforttag ist).
  Der **Tages**wert 1,25–1,60 bleibt Register-Zeile 98-S154-01 und ist **kein**
  Registry-Parameter. Nicht im Basiswert (US-Übertragbarkeit; Ambient-Anteil bereits in
  ΔDosis — Doppelzählungsschutz).

```python test: beispiel_98_lambda_l_kosten
# Letalitaet, Restlebenserwartung, Kostenketten im Ankerfenster 2021-2023 [27,48,34,19]
anker_mm, anker_c44 = (26_140+27_040+27_430)/3, (236_670+243_430+242_820)/3
tote_mm, tote_c44 = (2928+3146+3169)/3, (1178+1275+1332)/3
lam_mm, lam_c44 = tote_mm/anker_mm, tote_c44/anker_c44
assert abs(lam_mm - 0.11466) < 0.00002 and abs(lam_c44 - 0.005236) < 0.000002
# L_quer (Befund 224): sterbefallgewichtet ueber ALLE Jahre UND Geschlechter des
# Ankerfensters, Stuetzstelle = medianes Sterbealter DES JEWEILIGEN JAHRES.
# Sterbetafel 2022/2024: e(78)F 10,9187 | e(76)M 10,3350 | e(77)M 9,7311
#                        e(88)F 5,0374  | e(84)M 5,9397  | e(85)M 5,4745
mm_jahre  = [(1236, 10.9187, 1692, 10.3350),    # 2021: F 78 / M 76
             (1293, 10.9187, 1853,  9.7311),    # 2022: F 78 / M 77
             (1318, 10.9187, 1851, 10.3350)]    # 2023: F 78 / M 76
c44_jahre = [(464, 5.0374, 714, 5.9397),        # 2021: F 88 / M 84
             (521, 5.0374, 754, 5.9397),        # 2022: F 88 / M 84
             (541, 5.0374, 791, 5.4745)]        # 2023: F 88 / M 85
lq = lambda rows: (sum(f*ef + m*em for f, ef, m, em in rows)
                   / sum(f + m for f, _, m, _ in rows))
l_mm, l_c44 = lq(mm_jahre), lq(c44_jahre)
assert abs(l_mm - 10.4569) < 0.001 and abs(l_c44 - 5.4787) < 0.001
# Gegenprobe: die Rev.-2-Werte stammten aus dem Einzeljahr 2023 und lagen daneben
assert abs(l_mm / 10.58 - 1) + abs(l_c44 / 5.30 - 1) > 0.04
# VSL/VOLY-Konsistenz (Befund 217): VSL unterstellt 22-38 Lebensjahre je Todesfall,
# real verloren gehen 5,5 (C44) bzw. 10,5 (MM) — Faktor 2,8-4,9 auf dem Mortalitaetspfad
for vsl, jahre in ((3.5e6, 21.8), (4.7e6, 29.2), (6.19e6, 38.5)):
    assert abs(vsl/160_800 - jahre) < 0.1
assert l_c44 < 3.5e6/160_800 / 3.9
assert abs(5326 * 119.3/94.5 - 6724) < 2 and abs(4660 * 119.3/94.5 - 5883) < 2
assert abs(9038 * 119.3/94.5 - 11410) < 2 and abs(5890 * 119.3/94.5 - 7436) < 2
assert abs((572 + 2643)/45909 - 0.070) < 0.0005
# BAF_C44 aus KID-2025-Split (Befund 202); BfS-2015-Split als obere Bandstuetze
assert abs(0.75*1.4 + 0.25*2.5 - 1.675) < 0.001
assert abs(0.50*1.4 + 0.50*2.5 - 1.95) < 0.001
# r_out-Beispiel (Befund 206): SCC-Anteil am ZUSATZ w_Z = w_scc*2,5/BAF_C44
w_z = 0.25 * 2.5 / 1.675
assert abs(w_z - 0.373) < 0.001
r_out = lambda q: (1 - w_z) + w_z * (1 + q*(1.77-1)) / (1 + 0.070*(1.77-1))
assert abs(r_out(0.14) - 1.019) < 0.001
# Bandgrenzen aus der q_out-Spanne [0; 0,21] statt gesetzt (Befund 219)
assert abs(r_out(0.0) - 0.981) < 0.001 and abs(r_out(0.21) - 1.038) < 0.001
assert abs(r_out(0.070) - 1.0) < 1e-12          # Zentrierung: q = q_quer => 1
# v_verh ist der JAHRESfaktor, nicht der Tageswert (Befund 216)
v_verh = lambda phi, s=1.45: 1 + phi*(s - 1)
assert abs(v_verh(0.0) - 1.0) < 1e-12           # Ebene geparkt => neutral
assert abs(v_verh(0.25) - 1.1125) < 1e-9        # Bandobergrenze ~1,11
```

```python test: beispiel_98_bundessumme
# Bundessummen: Baseline = Anker 2021-2023 (Befund 220); Delta-SSD DE bevoelkerungs-
# gewichtet 8,51 % (Befund 223) => Delta-Dosis 4,54 %; L_quer nach Befund 224.
anker_mm, anker_c44 = (26_140+27_040+27_430)/3, (236_670+243_430+242_820)/3
lam_mm, lam_c44 = (2928+3146+3169)/3/anker_mm, (1178+1275+1332)/3/anker_c44
L_MM, L_C44 = 10.4569, 5.4787
dd = 0.0851 * (4.9/4.6) * 0.6683 * 0.75
assert abs(dd - 0.0454) < 0.0001
d_mm  = anker_mm  * 0.6   * dd
d_c44 = anker_c44 * 1.675 * dd
yll = d_mm * lam_mm * L_MM + d_c44 * lam_c44 * L_C44
behandlung = d_mm * 6724 + d_c44 * 5883
euro = behandlung + yll * 160_800
assert abs(d_mm - 733) < 3 and abs(d_c44 - 18_339) < 90
assert abs(yll - 1404) < 8
assert abs(behandlung / 1e6 - 113) < 2 and abs(yll * 160_800 / 1e6 - 226) < 2
assert abs(euro / 1e6 - 339) < 3
# Sanity: Behandlungsanteil klein gegen KKR C43/C44 (1.823 Mio EUR 2023)
assert behandlung / 1.823e9 < 0.10
# Sanity-Band: untere und obere Parameterkombination (Kap. 4)
def summe(k, a, c_mm, c_c44):
    d = 0.0851 * k * a
    m, c = anker_mm * 0.6 * d, anker_c44 * 1.675 * d
    y = m * lam_mm * L_MM + c * lam_c44 * L_C44
    return m * c_mm + c * c_c44 + y * 160_800
assert abs(summe(0.3622, 0.5, 6724, 5883) / 1e6 - 115) < 2    # 1 sigma unten
assert abs(summe(1.0616, 1.0, 11410, 7436) / 1e6 - 737) < 2   # 1 sigma oben
```

```python test: beispiel_98_beispielzelle
# 1.000 EW im Bundesmix, Region Mitte (Delta-Dosis 4,89 %), P-Defaults
p_de = 15_583_456 + 49_163_992 + 9_569_640 + 6_294_744 + 2_844_213
anker_mm, anker_c44 = (26_140+27_040+27_430)/3, (236_670+243_430+242_820)/3
f_mm, f_c44 = anker_mm/p_de*1000, anker_c44/p_de*1000   # Rohraten je 1.000 EW
assert abs(f_mm - 0.3220) < 0.0005 and abs(f_c44 - 2.8874) < 0.0005
dd_m = 0.0915 * (4.9/4.6) * 0.6683 * 0.75   # Mitte, bevoelkerungsgewichtet [72]
assert abs(dd_m - 0.0489) < 0.0001
d_mm  = f_mm  * 0.6   * dd_m
d_c44 = f_c44 * 1.675 * dd_m
yll = d_mm * ((2928+3146+3169)/3/anker_mm) * 10.4569 \
    + d_c44 * ((1178+1275+1332)/3/anker_c44) * 5.4787
euro = d_mm * 6724 + d_c44 * 5883 + yll * 160_800
assert abs(d_mm - 0.0094) < 0.0002
assert abs(d_c44 - 0.2364) < 0.003
assert abs(euro - 4365) < 60               # ~4.400 EUR je 1.000 EW und Jahr
```

### 3.5 Zeichentabelle (alphabetisch; §3.2-Form)

| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \(a\) | Altersband u20 · 20–64 · 65–74 · 75–84 · 85+ (Ebenen wie #96 §3.2) | — | Zensus-Altersbänder + Ebene u20 |
| \(a_{\text{attr,UV}}\) | klimaattribuierter Anteil des SSD-/Dosistrends | — | **0,75** (0,5–1,0) — gekennzeichnete Abschätzung §3.2; register:98-E20-03 |
| \(\text{BAF}_e\) | biologischer Verstärkungsfaktor (%-Inzidenz je +1 % Dosis) | — | MM **0,6** (±0,4) · C44 **1,675** (1,675–1,95; §3.1) [29,30]; register:98-E20-04 |
| \(c_e\) | Erstjahres-Behandlungskosten je Fall (**Proxy**, §3.4) | €₂₀₂₄ | MM **6.724** (Band –11.410) · C44 **5.883** (–7.436) = [34]-Werte × 119,3/94,5 [19]; register:98-K1-01; herleitung:#c-e |
| \(c_{\text{kal},e}\) | Normierungsskalar der Ablesekette (ein Skalar je Entität; wirkt in der §3.3-Formel auf die Roh-Bandraten; Anker 2021–2023) | — | MM **1,0012** · C44 **0,9910**; herleitung:#i-raten |
| \(F_{e,\text{Zelle}}\) | Baseline-Neuerkrankungen der Zelle | 1/Jahr | berechnet (§3.3) |
| \(I_{e,a}^{\text{roh}}\) | Roh-Neuerkrankungsrate je Entität und Band (Ablesekette; Anlage-CSV) | 1/100.000·a | Tabelle §3.3 [27,48]; register:98-R35-01; herleitung:#i-raten |
| \(k_{\text{UV}}\) | Übersetzung SSD-Trend → erythemwirksame Dosis (Elastizität zeitinvariant angenommen, §3.2) | — | **0,7119** (0,3622–1,0616) = (4,9/4,6) × 0,6683, Brücke über die Globalstrahlung; Band = publizierte Standardfehler (§3.2) [31,73]; register:98-E20-02; herleitung:#k-uv |
| \(\bar L_e\) | verlorene Lebensjahre je Sterbefall (Median-Approximation, gekennzeichnet; Jahresmediane des Ankerfensters) | Jahre | MM **10,4569** · C44 **5,4787** [27,48]; register:98-K1-02; herleitung:#l-quer |
| \(\text{OR}_{\text{out}},\ q_{\text{out}},\ \bar q_{\text{out}},\ r_{\text{out}},\ w^Z\) | Außenberufs-Sensitivität (auf den SCC-Anteil am Zusatz \(w^Z\) = 0,373; nur Bänder 20–64…85+, **nicht** u20; **nicht im Basiswert**, §3.4) | — | OR **1,77** [1,37–2,30] [43]; \(\bar q_{\text{out}}\) = **0,070** [70]; \(r_{\text{out}}\) **0,981–1,038** über \(q_{\text{out}}\) ∈ [0; 0,21]; register:98-OUT-01; herleitung:#q-out |
| \(\text{pop}_a\) | Bevölkerung der Zelle je Band | Personen | Zensus 2022, 100 m (+ u20); register:98-R35-01 |
| \(s\) | Tages-Multiplikator der persönlichen Dosis an einem Komforttag | — | **1,45** (1,25–1,60) [57–59]; register:98-S154-01 |
| \(\text{SSD}\) | Sonnenscheindauer (Normalperioden-Mittel je Zelle) — Kartenebene **neu anzulegen** (angelegt, §3.6) | h/Jahr | DWD-CDC sunshine_duration 1 km [33]; Gebietsmittel-Referenzen [69]; register:98-E20-01 |
| \(T\) | Dauer des Dosisanstiegs (Mittelpunktabstand der Normalperioden) | Jahre | **30** (1961–1990 ⇒ 1991–2020); herleitung:#gleichgewicht |
| \(\text{VOLY}\) | Wert eines verlorenen Lebensjahres | €₂₀₂₄ | **160.800** (Band 136,4–165,6 T€; Kette #95 §3.5) [19]; herleitung:#voly (in #95) |
| \(v_{\text{verh}}\) | Verhaltens-Sensitivität — **Jahres**faktor, **abgeleitet** aus \(s\) und \(\phi_{\text{Komfort}}\) (kein eigener Parameter, §3.2 Kein-Doppelkanal) | — | \(1+\phi_{\text{Komfort}}(s-1)\) = **1,00** (Band 1,00–1,11); herleitung:#v-verh |
| \(w_{\text{SCC}}\) | SCC-Anteil an C44 (altersinvariant, dokumentierte Annahme; Quellen-Widerspruch benannt §3.1) | — | **0,25** (Band 0,25–0,50) [27; obere Stütze 2015er-BfS-Split]; herleitung:#baf-c44 |
| \(Y(a)\) | Inzidenz im Alter \(a\); \(Y(a)\sim\Phi(a)^{c}\) mit \(c\) = BAF | 1/100.000·a | Funktionsform aus [30]; herleitung:#gleichgewicht |
| \(\text{YLL}_{\text{Zelle}}\) | verlorene Lebensjahre — **nativer Ausweis** | Jahre/Jahr | Ergebnis |
| \(\Delta\text{Dosis}_{\text{Zelle}}\) | relative klimaattribuierte Dosisänderung | — | SSD-Normalperioden-Δ × \(k_{\text{UV}}\) × \(a_{\text{attr,UV}}\); DE 4,54 % (§3.2, fallgewichtet [72,73]); berechnet |
| \(\Delta F_{e,\text{Zelle}}\) | klimaattribuierte Zusatzfälle (Teil-Ausweis) | 1/Jahr | berechnet |
| \(\lambda_e\) | Letalitätsanteil (Perioden-Approximation, gekennzeichnet; Anker 2021–2023) | — | MM **0,11466** · C44 **0,005236** [27]; register:98-K1-02 |
| \(\tau\) | Transient-Faktor: Anteil der Lebenszeitdosis-Erhöhung an der Jahresdosis-Erhöhung, \(\tau=(T/2)/a\) | — | **1,00** im Ausweis (Gleichgewichtslesart); Spanne **0,20–0,48** als §4-Achse; gekennzeichnete Abschätzung §3.9; herleitung:#gleichgewicht |
| \(\Phi(a)\) | kumulierte UV-Dosis bis zum Alter \(a\) (Lebenszeitdosis) | relative Einheit | Definitionsgröße der BAF in [30]; herleitung:#gleichgewicht |
| \(\phi_{\text{Komfort}}\) | dosisgewichteter Komforttag-Anteil (Ebene **geparkt**, Neutralwert 0) | — | **0** (Band 0–0,25, gekennzeichnete Abschätzung §3.4); herleitung:#v-verh |
| \(\text{€}_{\text{Zelle}}\) | bewerteter Schaden K1 (Ursache UV) — Teil-Ausweis | €₂₀₂₄/Jahr | Ergebnis (§3.4) |

### 3.6 Kartenebenen und Fallbacks

Die Ebenen laufen auf den **drei** Wegen, die §3.1 kennt — die Kennzeichnung ist
berichtsweit einheitlich (Befund 215):

| Ebene | §3.1-Status | Quelle / Beschaffungsweg (keyless) | Zell-Ableitungsregel | Fallback | Wirkung, wenn nicht verfügbar |
|---|---|---|---|---|---|
| SSD / UV_RADIATION | **neu anzulegen** (angelegt 31.08.2026) | DWD-CDC Jahresraster `sunshine_duration`, 1 km, ab 1961 [33] | zwei Normalperioden-Mittel je Zelle (1961–90, 1991–2020), einmalig vorgemittelt | Bundesland-Gebietsmittel [69] | Verlust der Feinstruktur (SSD variiert v. a. Nord–Süd) |
| u20 | vorhanden (aus #96) | Zensus 2022 | Altersband-Aggregation | — | — |
| Außenbeschäftigten-Anteil \(q_{\text{out}}\) | **geparkt (Datenquelle fehlt)** — Watchlist | INKAR/SVB-Branchenanteile: **keine** keyless Zellquelle | (offen) | — | \(q = \bar q\) ⇒ \(r_{\text{out}}\) = **exakt 1** (Zentrierungs-Neutralwert, §3.1) |
| Komforttag-Anteil \(\phi_{\text{Komfort}}\) | **geparkt (Datenquelle fehlt)** — Watchlist | DWD-Tagesraster Temperatur × Tagesdosis; die **Kombination** ist nicht keyless verfügbar | (offen) | — | \(\phi = 0\) ⇒ \(v_{\text{verh}}\) = **exakt 1** (§3.4; Befund 216) |
| YLL-Rate | Ergebnisebene | — | YLL je 1.000 EW | — | — |

**Fallback bleibt flächengewichtet (Befund 232).** Für Zellen ohne Rasterwert greift
das **Bundesland-Gebietsmittel [69]**, also ein *flächen*gewichteter Wert — bewusst und
abweichend vom nationalen Bezug (§3.2): Gesucht ist dort der Erwartungswert für *eine*
Zelle an unbekannter Stelle im Land, und das ist das Flächenmittel, nicht das
Bevölkerungsmittel des Landes. Betroffen sind 29 der 10.853 Gemeindepunkte mit
zusammen 121.428 EW = **0,15 %** der Bevölkerung. Richtung: In Ländern, deren
bevölkerungsgewichteter Wert über dem flächengewichteten liegt (Saarland 9,42 gegen
6,99 %, Sachsen 10,55 gegen 9,46 %), unterschätzt der Fallback diese wenigen Zellen.

**Stand SSD nach der Integration 31.08.2026:** Das 1-km-Raster ist angebunden
(vorgemittelte Normalperioden-Anlage, §3.2), der Zellwert ist der **Regelfall**; das
Bundesland-Gebietsmittel [69] greift nur noch für Zellen außerhalb des Rasters oder bei
fehlender Anlage. Beide geparkten Ebenen betreffen ausschließlich Sensitivitätsbänder —
der **Basiswert** des Berichts ist von ihnen unabhängig und exakt reproduzierbar.

### 3.7 Schicht A (getrennt; nie auf €-Pfaden)

\(\hat H\)(E20: UV_RADIATION/SSD) × \(\hat E\)(R35: POPULATION_DENSITY / AGE_STRUCTURE) ×
\(\hat V\)(S154/S155/S158: Verhalten/Bewusstsein/Screening; R36: HEALTHCARE_ACCESS);
\(\text{Index} = 100 \cdot \max_p (w_p \hat H_p \hat E_p \hat V_p)\) (Worst-Pathway;
Normierungen editierbar, testseitig von €-Pfaden getrennt).

## 4 Kalibrierung & Validierung (§2.4/§3.4)

- **Gewichtung des Klimasignals = die des Produktionsmodells (§3.4; Befund 223).**
  Die nationale \(\Delta\text{SSD}\) ist **bevölkerungsgewichtet** (8,51 %,
  Gemeindepunkt-Ebene, Anlage [72]), nicht flächengewichtet (7,82 %) — das
  Produktionsmodell summiert bevölkerungsgewichtet über Zellen, und §3.4 erklärt
  Näherungswerte bei bevölkerungsgewichteter Exposition ausdrücklich für unzulässig.
  Alle Ergebnis- und Prüfwerte dieses Kapitels rechnen mit 8,51 %; bis Rev. 2 lagen
  sie um 8,8 % zu niedrig. Die Ressourcen-Regel bleibt gewahrt (10.824 Gemeindepunkte
  statt eines Vollrasters), und die Anlage liest die SSD über dieselbe Produktfunktion
  wie die Schadensfunktion.
- **Kalibrierung = Baseline-Verankerung an der amtlichen Inzidenz:** genau **ein
  Skalar je Entität** (\(c_{\text{kal,MM}}\) = 1,0012; \(c_{\text{kal,C44}}\) = 0,9910,
  §3.3) — die Bundes-Baseline reproduziert den ZfKD-Anker auf der Bezugspopulation der
  Normierung; die Produktions-Baseline liegt wegen der abweichenden Populationsbasis
  um −1,19 % darunter (gekennzeichnete Näherung §3.3, Befund 226).
  **Anker-Zeitreihe und Auswahlregel (§3.4; Befund 220):** Anker ist das arithmetische
  Mittel der Jahre **2021, 2022 und 2023** aus KID 2025 Tab. 3.13.1/3.14.1 —
  **dasselbe Fenster, über das die abgelesenen Altersraten gepoolt sind** (Abb.
  3.13.2/3.14.3). MM 26.140 / 27.040 / 27.430 ⇒ **26.870**; C44 236.670 / 243.430 /
  242.820 ⇒ **240.973**. Revisionsstand: KID 2025; die Neuerkrankungszahlen sind
  vollzähligkeitskorrigierte **Schätzungen** des ZfKD, kein Jahr ist als vorläufig
  ausgewiesen — die Drei-Jahres-Mittelung ist zugleich die Absicherung gegen die
  Restunsicherheit des jüngsten Registerjahrs. Sensitivität der Auswahlregel:
  Einzeljahres-Anker 2023 (Rev. 1) ⇒ \(c_{\text{kal}}\) 1,0221/0,9986 und
  **+2,8 %** auf die €-Summe; Anker 2022 ⇒ +1,5 %; Anker 2021 ⇒ **−4,3 %** — die
  Spanne der Auswahlregel beträgt damit −4,3 … +2,8 %, weit innerhalb der Bänder.
  Genau diese Streuung ist der Grund für die Mittelung. Seit Rev. 3 gilt dieselbe
  Auswahlregel auch für \(\bar L_e\) (Befund 224) — Anker, \(c_{\text{kal}}\),
  \(\lambda_e\) und \(\bar L_e\) stehen jetzt vollständig im selben Fenster.
  Eine Zeitreihen-Kalibrierung des **klimaattribuierten** Anteils ist nicht möglich: es
  existiert keine amtliche Reihe „UV-klimaattribuierte Fälle" (dokumentierte Ausnahme
  analog #96 §4); der Klimaanteil ist stattdessen messungsbasiert (SSD [69], Dosistrend
  [31], BAF [29,30]). **Kalibriermodell = Produktionsmodell** (lineares Modell, keine
  Näherungsläufe).
- **Struktur-Validierung auf der Altersachse — out-of-sample (§3.4; Befund 214).**
  Die kritischste Achse dieses Modells ist die **Altersverteilung**: Die Baseline stammt
  vollständig aus einer Abbildungs-Ablesung, und ein reiner Verteilungsfehler lässt die
  Bundessumme unberührt, verschiebt aber jede Kommune (Nachweis: Befund 212). Ein
  Vergleich der **rohen** Gesamtrate taugt dafür **nicht** — auf sie wird
  \(c_{\text{kal}}\) gefittet, die Prüfung wäre in-sample.
  Geprüft wird deshalb die **altersstandardisierte Neuerkrankungsrate** (alter
  Europastandard): Sie gewichtet die Altersgruppen anders als der deutsche Altersaufbau
  und ist gegen die Normierung invariant — ein Fehler im Altersprofil schlägt auf sie
  durch, auf die rohe Rate nicht. Vergleichswerte: KID 2025 Tab. 3.13.1/3.14.1,
  Mittel 2021–2023.

  **Toleranz hergeleitet statt gesetzt (§3.9 gilt auch für Toleranzen; Befund 229a;
  Log 22).** Bis Rev. 2 standen hier ±10 % ohne Rechenweg, gesetzt in derselben
  Revision, die das Ergebnis erzeugt hat. Die Herleitung: Jede Einzelablesung trägt
  ±15 %; die Fehlerfortpflanzung des gewichteten Mittels
  \(\sigma/\text{ASR} = 0{,}15\cdot\sqrt{\sum(w_i r_i)^2}\,/\,\sum(w_i r_i)\) ergibt im
  ungünstigsten der vier Reihen **σ = ±5,07 %**; die Abnahmetoleranz ist **2σ =
  ±10,1 %** (nicht aufgerundet — §6 verbietet das nachträgliche Weiten einer
  Toleranz, auch um Rundungsbeträge; Befund 234). Die bisherigen ±10 % waren damit sachlich richtig bemessen, nur unbelegt.
  Ein systematischer *Niveau*-Versatz der Ablesung verschiebt die ASR zwar mit, wird im
  Modell aber von \(c_{\text{kal}}\) abgefangen — für die *Profil*prüfung ist der
  zufällige Anteil der richtige Maßstab. Weil das Ist-Ergebnis mit 0,4 σ weit unter der
  Spezifikation liegt, gilt zusätzlich die engere **Regressionsschranke ±3 %**
  (Golden-Test), damit eine künftige Verschlechterung der Ablesekette auffällt.
  Rechenweg: Anlage [71], Golden-Test `beispiel_98_struktur_validierung`.

  | ASR (alter Europastandard), je 100.000 | Modell (Ablesekette) | amtlich 2021–2023 | Abweichung | Verdikt |
  |---|---|---|---|---|
  | MM (C43) Frauen | 20,95 | 20,93 | **+0,1 %** | bestanden |
  | MM (C43) Männer | 22,79 | 22,70 | **+0,4 %** | bestanden |
  | C44 Frauen | 144,28 | 141,87 | **+1,7 %** | bestanden |
  | C44 Männer | 177,38 | 174,07 | **+1,9 %** | bestanden |

  **Ist-Ergebnis: max. 1,9 % — Toleranz ±10,1 % und Regressionsschranke ±3 %
  eingehalten ✓.** Damit ist das Altersprofil der Ablesekette unabhängig bestätigt,
  nicht nur ihr Niveau.

  **Reichweite der Prüfungen (Befund 229b).** Die ASR prüft die **Ablesekette**, also
  die 5-Jahres-Werte. Den Schritt Ablesewerte → **Bandraten**, an dem Befund 212 den
  Fehler hatte, prüft sie **nicht** — er ist der rohen Rate zugeordnet, und zwar
  aussagekräftig: Sie läuft gegen die *unnormierte* Ablesesumme, \(c_{\text{kal}}\)
  wird erst danach gebildet (der 212er-Fehler erschien dort als +5,9 %). Die
  Rev.-2-Formulierung „in-sample, deshalb kein Strukturnachweis" war für diese Prüfung
  zu pauschal. Beide zusammen decken Ableseprofil **und** Aggregation ab:
  rohe Rate MM 32,16 vs. 32,20 (−0,1 %), C44 291,36 vs. 288,74 (+0,9 %) — innerhalb
  ±15 %. *Aggregat-Querprüfung (kein Strukturnachweis):* Mortalität ZfKD-Anker
  4.342,7 Sterbefälle (3.081,0 + 1.261,7) vs. Destatis Todesursachen 2024 ≈ 4.600
  [27,28] ✓.
  *Regionale Achse:* SSD-Regionalwerte sind eigene Messung [69]; eine unabhängige
  Länder-**Inzidenz**-Prüfung (GEKID-Atlas) ist nicht keyless — dokumentierte Lücke
  mit Ersetzungspfad; sie ist nachrangig, weil die Baseline regional nur über
  Bevölkerung und Alter differenziert (kein regionaler Inzidenz-Modifikator im Modell).
- **Verteilschlüssel-Test (§3.1):** strikt bottom-up — Zelle ohne Bevölkerung → 0; das
  Klimasignal ist je Zelle/Region gemessen (kein Deutschland-Nenner). **Baseline-Fälle
  sind bevölkerungs-/altersproportional (kein Klimasignal); der klimaattribuierte
  Zusatz \(\Delta F\) trägt den vollen ΔDosis-Faktor** — Kommune ohne SSD-Anstieg → ~0 ✓
  (der native YLL-Ausweis und € enthalten nur den Zusatz, keinen Sockel).
- **Sanity-Bänder (Unter- und Obergrenze):**
  Bundessummen (Basiswerte): \(\Delta F\) = **733 MM + 18.339 C44 ≈ 19.072 Fälle/Jahr**,
  **YLL ≈ 1.404/Jahr**, **€ ≈ 339 Mio €₂₀₂₄/Jahr** (Behandlung 113 + Mortalität 226).
  *Obergrenzen:* Behandlungs-€ = 6,2 % der amtlichen KKR C43/C44 (1.823 Mio €₂₀₂₃ [28]) ✓;
  klimaattribuierter Inzidenzanteil MM +2,73 %/C44 +7,61 % ≪ beobachteter
  Inzidenzanstieg (standardisierte MM-Rate 1999–2023 deutlich steigend; C44-Hospitali-
  sierungen 2004–2024 +94,5 % [27,28]) ✓; YLL-Anteil = 1.404 / ≈ 39.130 (= \(\sum_e \text{Sterbefälle}_e \times \bar L_e\)
  = 3.081,0 · 10,4569 + 1.261,7 · 5,4787, Anlage [71]; Befund 352) Gesamt-Hautkrebs-
  YLL ≈ **3,6 %** (konsistent zu BAF × ΔDosis) ✓. *Untergrenze:* SSD-Anstieg ist messfest
  > 0 (alle Länder +4,5…+12,1 %, alle Regionen +7,8…+9,2 % [69,72]); untere
  Bandkombination ergibt ≈ 115 Mio € > 0.
- **Bänder je Achse — separat ausgewiesen, nicht kumuliert (§3.9; Befund 221).**
  Rev. 1 behauptete diese Trennung, bezifferte sie aber nicht; hier die Zahlen
  (Anlage [71]):

  | Achse | Spanne | € Mio/Jahr | Δ gegen Basiswert 339 |
  |---|---|---|---|
  | \(k_{\text{UV}} \times a_{\text{attr}}\), untere Kombination | 0,3622 × 0,50 | **115** | −66 % |
  | \(k_{\text{UV}} \times a_{\text{attr}} \times c_e\) oben, obere Kombination | 1,0616 × 1,00 × \(c_e\) oben (**beide** Entitäten) | **737** | +118 % |
  | VOLY | 136.400 / 165.600 € | 304 – 345 | −10,1 % … +2,0 % |
  | \(a_{\text{attr}}\) | 0,50 / 1,00 | 226 – 452 | −33,3 % … +33,3 % |
  | BAF_MM | 0,2 / 1,0 | 241 – 436 | −28,8 % … +28,8 % |
  | \(w_{\text{SCC}}\) (⇒ BAF_C44 1,675/1,95) | 0,25 / 0,50 | 339 – 370 | ±0 % … +9,3 % |
  | **Transient-Faktor \(\tau\)** (Gleichgewichts- ↔ Jahres-Lesart, §3.4) | 0,20 / 1,00 | **67 – 339** | **−80 % … ±0 %** |
  | \(r_{\text{out}}\) (geparkt) | \(q_{\text{out}}\) ∈ [0; 0,21] | 339 | **±0 %** (zentriert) |
  | \(v_{\text{verh}}\) (geparkt) | \(\phi\) ∈ [0; 0,25] | 339 – 377 | ±0 % … +11,3 % |

  **Gesamtband ≈ 115–737 Mio €** = nur die \(k_{\text{UV}}\)/\(a_{\text{attr}}\)/\(c_e\)-Kombination;
  die übrigen Zeilen sind **nicht** hineinmultipliziert. Größte Achse ist der
  einseitige Transient-Faktor \(\tau\) (§3.4); größter **zweiseitiger** Treiber ist die
  \(k_{\text{UV}}\)-Messunsicherheit (±49 %); danach folgen \(a_{\text{attr}}\)
  (±33,3 %) und BAF_MM (±28,8 %) — die Reihenfolge entspricht der Tabelle darüber
  (Befund 282; bis Rev. 8 stand hier eine abweichende Rangfolge). Seit Rev. 3 erzeugt
  die Anlage [71] alle Zeilen; \(a_{\text{attr}}\) ist seit Rev. 8 als eigene Achse
  ausgewiesen (Befund 261).
- **Unsicherheiten (nach Größe geordnet, Befunde 250/268):**
  Aufgezählt wird hier **nach Größe**; die Bändertabelle darüber ist nach Sachgruppen
  geordnet, nicht nach Größe (Befunde 361/370). **Größte Achse ist
  der Transient-Faktor \(\tau\)** (0,20–1,00 ⇒ **−80 %**, §3.4): Er trennt die
  ausgewiesene Gleichgewichtslesart von einer reinen Jahres-Attribution und ist
  einseitig — er kann das Ergebnis nur senken. Danach die
  **k_UV-Messunsicherheit** (Band **0,3622–1,0616** = **±49 %**) — der
  **Stichprobenfehler der publizierten Trendschätzungen**, *nicht* die räumliche
  Übertragbarkeit; letztere steht als Modellgrenze 9. Sie ist der größte
  *zweiseitige* Treiber. Danach: Attribution \(a_{\text{attr}}\) (±33 %);
  **BAF_MM** (±67 % auf den MM-Pfad ⇒ ±28,8 % auf die Summe — Befund 356: die Achse
  steht hier **einmal**, nicht doppelt); die Zeitinvarianz-Annahme der Elastizität
  (§3.2, Befund 222); Ablesekette (±15 % je Ablesung; Altersprofil
  out-of-sample bestätigt, s. o.); Anker-Auswahlregel (−4,3 … +2,8 %);
  **Binnenheterogenität des Bandes 20–64 (≈ ±4 % je Kommune, Bundessumme unberührt —
  §6 Modellgrenze 7, Befund 225)**; **Populationsbasis Kalibrierung ↔ Produktion
  (−1,19 %, §3.3, Befund 226)**; Latenz (§6); Entitäten-Split altersinvariant;
  \(c_e\)-Proxy; Augenschäden fehlen.

## 5 Maßnahmen-Hebel (§2.5/§3.5)

- **Früherkennungs-Förderung / SCS-Teilnahme (S158) — qualitativ** (Befund 203): Die
  DiD-Evidenz [34] belegt das Sparpotenzial (SCS-detektierte MM-Fälle: **−18,8 %
  [−23,1; −8,4]** Erstjahreskosten), aber der **Basiswert setzt bereits für alle Fälle
  die SCS-Kostensätze an** (Untergrenzen-Wahl §3.4) — ein zusätzlicher Hebel auf
  \(c_e\) würde den Maßnahmeneffekt doppeln (LF-4-Klasse: Maßnahmeneffekt schon im
  Basiswert). Quantifizierbar wird der Hebel erst mit einem **Detektionsmix-Parameter**
  (Anteil SCS-detektierter Fälle je Kommune als Basiswert-Größe, Hebel = Mix-Verschiebung
  × Kostendifferenz 11.410 − 6.724 €) — dokumentierter Ersetzungspfad; bis dahin
  qualitativ. Letalitätswirkung früherer Erkennung nicht angesetzt (dokumentiert).
- **UV-Schutz im öffentlichen Raum / Kommunikation (S155) — qualitativ** (§3.5-Regel;
  GP-Befunde 26/34): publizierte Nutzen-Kosten-Verhältnisse 2,2–8,7 : 1 [37] sind keine
  Effektgröße auf Dosis oder Inzidenz; keine deutsche Interventionsstudie [37]. Der Hebel
  läuft ehrlich als „qualitativ" (Verschattung senkt die effektive Dosis exponierter
  Gruppen — Wirkungsort wäre \(v_{\text{verh}}\)/lokale Dosis, sobald quantifiziert).
- **R7-Weiche:** nicht einschlägig (keine K8-Vorsorge-Gegenbuchung in der Netzwerkliste;
  kommunale Programmkosten laufen im Maßnahmen-Modul außerhalb der Schadenskonten).

## 6 Szenario-Anwendung & Modellgrenzen (§3.2/§3.6)

**Szenario-Anwendung 98-A:** Verschoben wird ausschließlich die Zell-SSD (Projektions-
raster bzw. Fortschreibung des Gebietsmittel-Trends; UV-B-Projektion +1,3 %/Dekade [32]
als Plausibilisierungsrahmen). Konstant: BAF, \(k_{\text{UV}}\), \(a_{\text{attr}}\),
Inzidenzraten, \(\lambda_e\), \(\bar L_e\), Kostensätze, Bevölkerung. **M0 weist das
Ist-Klima aus** (Normalperiodenvergleich). **Stationaritätsannahmen (dokumentiert):**
Inzidenz-Baseline stationär (real steigend — Untergrenze); Detektionsmix konstant.

**Modellgrenzen (dokumentiert):**
1. **Latenz:** Hautkrebs entsteht mit einer Verzögerung von **Jahrzehnten** [35]
   (Quellenwortlaut; die verbreitete Angabe „20–40 Jahre" ist dort **nicht**
   beziffert und wird deshalb nicht geführt — §3.9) — \(\Delta F\) ist das
   „eingelaufene Risiko" der heutigen Dosislage, keine Vorhersage der Fälle *dieses*
   Jahres; die Jahres-Attribution ist konzeptionell unscharf (Infokasten-Pflichttext).
2. \(k_{\text{UV}}\)-Übersetzung: **ein** Messpunkt (UV-Dosis Dortmund, GR/SunD
   DWD-Station 1117 Bochum, 10 km entfernt); Band **0,3622–1,0616** (publizierte
   Standardfehler, 1 σ) dominiert die Unsicherheit. Station und Raster
   unterscheiden sich an der Messzelle **metrikabhängig**: bei der
   Sonnenscheindauer um Faktor **1,71** (11,3 gegen 6,62 %/Dek.), bei der
   Globalstrahlung nur um **1,02** (4,6 gegen 4,51 %/Dek., §3.2). Genau deshalb
   überbrückt der Basiswert die Skalen über die Globalstrahlung, die in beiden
   Messfamilien vorliegt. **Gekennzeichnete Annahme (Befund 292):** Die Brücke
   liefert die Rasterelastizität nur, wenn der Quotient Dosis/Globalstrahlung
   **skaleninvariant** ist — gestützt darauf, dass das Raster die Globalstrahlung
   praktisch unverzerrt wiedergibt (Faktor 1,02), aber nicht unabhängig belegt.
   Ersetzungspfad: ein zweiter deutscher Dosis-Messpunkt (Uccle liegt außerhalb DE),
   um die Elastizität nicht an einer Stadt zu hängen.
   **Zeitinvarianz-Annahme (Befunde 222/246):** Die Elastizität ist im Fenster
   1997–2022 gemessen und wird auf den Normalperiodenversatz 1961–90 → 1991–2020
   angewendet. Bis Rev. 5 stand hier, die Messperiode liege „in der Ozon-Erholung",
   woraus eine Unterschätzung folge. [31] misst am selben Ort jedoch einen
   **signifikanten sommerlichen Ozonrückgang von 0,9 %/Dekade im Messfenster** — die
   Ozonentwicklung wirkte dort **dosiserhöhend**. Richtung damit umgekehrt: ΔDosis
   wird eher **überschätzt**; die Untergrenzen-Zusage ist insoweit eingeschränkt.
   Größenordnung klein (0,9 gegen 6,62 %/Dek. SSD) gegen das k_UV-Band.
3. Attribution ohne DE-UV-Attributionsstudie (gekennzeichnete Abschätzung, Band).
4. Verhalten dominiert die reale Exposition (KWRA-Kernaussage) — \(v_{\text{verh}}\)
   bleibt Sensitivitätsband, der Basiswert bildet nur den Ambient-Dosispfad ab
   (Untergrenze der Verhaltens-These, Doppelzählungsschutz §3.4). Die Jahreswirkung
   hängt am dosisgewichteten Komforttag-Anteil \(\phi_{\text{Komfort}}\); diese Ebene ist
   **geparkt**, der Parameter läuft dokumentiert auf \(\phi\) = 0 ⇒ Faktor 1
   (§3.4/§3.6; Befund 216).
5. Ablesekette der Altersraten (±15 % vor Normierung); ZfKD-Datenbank als Ersetzungspfad.
6. Augenschäden (Katarakt) und K2-Produktivität nicht enthalten (Untergrenze).
7. **Binnenheterogenität des Bandes 20–64 (gekennzeichnete Näherung, §3.9;
   Befund 225).** Das Modell führt 20–64 als *eine* Rate, obwohl die abgelesene Evidenz
   innerhalb des Bandes um mehr als eine Größenordnung variiert (geschlechtsgemittelt
   MM 3,5 → 47, C44 5 → 333 je 100.000). Das Band trägt 45 % der MM- und 25 % der
   C44-Baseline. Stützrechnung mit der nationalen 5-Jahres-Struktur (sie reproduziert
   die Bandraten auf 1–2 % und validiert sich damit): Verschiebt sich der 20–34-Anteil
   am Band vom Bundeswert 30,8 % auf 24 % bzw. 40 %, liegt die wahre Bandrate bei
   MM **+8,5 % / −11,6 %** und C44 **+12,0 % / −16,3 %** ⇒ **≈ ±4 %** auf die €-Summe
   einer Kommune, mit dem Vorzeichen an der Altersstruktur; die **Bundessumme bleibt
   unberührt**. Die angesetzte Kreis-Spannweite ist eine gekennzeichnete Abschätzung —
   eine belegte kommunale Verteilung des 20–34-Anteils liegt nicht keyless vor.
   *Ersetzungspfad:* Das Produkt lädt die Zensus-2022-Spalten `a20bis24 … a60bis64`
   bereits je 100-m-Zelle (`zensus_loader.AGE_BAND_COLUMNS`); sie werden nur zu `u65`
   addiert. Eine feinere Bänderung (20–44 / 45–64) ist damit ohne neue Datenquelle
   möglich, greift aber in die von #96 mitgenutzte Bandkette ein und ist deshalb als
   produktweiter Schritt zu führen, nicht als #98-Alleingang (Log 21).
8. **Populationsbasis Kalibrierung ↔ Produktion** (−1,19 %, §3.3, Befund 226).
9. **Räumliche Streuung des \(k_{\text{UV}}\)-Rasterquotienten (Befunde 255/256).**
   Der Quotient ΔGlobal/ΔSSD variiert über die Gemeindepunkte erheblich (5. Perzentil
   0,3225 · Median 0,6305 · 95. Perzentil 1,1671; gewichteter Bundeswert **0,6683**).
   Das verschiebt **einzelne Kommunen** gegeneinander. Die Bundessumme ist davon
   **nahezu** unberührt, weil sie den mit Baseline-Fällen × ΔSSD gewichteten Wert
   verwendet — dasselbe Gewicht, mit dem das Produktionsmodell summiert (Befunde
   266/278). „Nahezu" statt „exakt", weil die beiden Entitäten leicht verschiedene
   Gewichte hätten (MM 0,6674 · C44 0,6689 gegen den geführten Mittelwert 0,6683);
   die Restdifferenz von < 0,2 % ist als Näherung gekennzeichnet. Deshalb
   steht die Streuung hier als Modellgrenze und **nicht** im Sanity-Band (dieselbe
   Buchung wie bei \(r_{\text{out}}\) und Modellgrenze 7). Richtung: In Kommunen mit
   überdurchschnittlichem Quotienten unterschätzt das Modell den Zusatz, in
   unterdurchschnittlichen überschätzt es ihn. *Ersetzungspfad:* \(k_{\text{UV}}\)
   als Zellgröße aus dem Quotienten der beiden Raster — die Daten liegen vor, es wäre
   eine neue Ebene nach §3.1.

**Infokasten-/UI-Texte (§3.6 — Teil des Berichts):**

> **Infokasten 1 — am Gesamtwert:** „Dieser Wert ist der *bewertete Schaden im Konto K1
> Gesundheit (Ursache: UV)* (Modellstand M0). Er umfasst die klimaattribuierten
> zusätzlichen Hautkrebs-Behandlungskosten und den Wert verlorener Lebensjahre — nicht
> enthalten sind u. a. Augenerkrankungen, Arbeitsproduktivität (Stufe M3) und
> Vorsorgekosten. Der ausgewiesene Betrag ist deshalb eine bewusste **Untergrenze**; er
> wird mit jeder Ausbaustufe vollständiger. Innerhalb des heutigen Kontos K1 können
> einzelne Rechenschritte den Wert auch nach unten korrigieren: Die Methodik weist
> fünf bewusst *überschätzende* Näherungen aus. Die größte ist die
> **Gleichgewichtslesart der Latenz**: Ausgewiesen wird das mit der heutigen
> Dosislage *eingelaufene* Risiko; eine Zuordnung allein auf dieses Jahr läge
> um bis zu 80 % niedriger (Transient-Faktor 0,20–1,00, §3.4). Dazu kommen
> PAF-Linearisierung +2,7/+7,6 %, Perioden-Letalität,
> Median-Restlebenserwartung und Ozon-Zeitinvarianz — und mehrere
> *unterschätzende* (nur Konto K1, nur Erstjahreskosten, geparkte Sensitivitäten).
> Die Bilanz ist im Bericht §4/§6 beziffert. Berechnet mit Modellstand M0,
> Stand ⟨Datum⟩."
>
> **Infokasten 3 — zur Bewertung der Sterbefälle (Pflichttext, §3.2):** „Todesfälle
> werden mit den *verlorenen Lebensjahren* bewertet, nicht mit einem Pauschalbetrag je
> Todesfall. Hautkrebs trifft überwiegend hohe Altersgruppen — im Mittel gehen je
> Sterbefall 5 bis 11 Lebensjahre verloren. Der ausgewiesene Betrag liegt deshalb rund
> **3- bis 5-mal niedriger** als bei einer Bewertung je Todesfall. Beim Vergleich mit
> Risiken, die jüngere Menschen treffen, ist das zu beachten."
>
> **Infokasten 2 — zur Latenz (Pflichttext):** „UV-bedingter Hautkrebs entsteht mit
> Verzögerung von Jahrzehnten. Die ausgewiesenen Zusatzfälle beschreiben das mit der
> heutigen, klimabedingt erhöhten UV-Belastung ‚eingelaufene' Erkrankungsrisiko — nicht
> die exakten Fälle des laufenden Jahres."
>
> **Pflicht-Elemente:** Benennung „bewerteter Schaden — Konto K1 (Ursache: UV)" (nie
> „Gesamtschaden"); Vollständigkeitsanzeige „Stufe M0: 1 von 8 Konten aktiv" mit
> Roadmap-Aufklappliste; Versionsstempel „berechnet mit Modellstand M0 — Untergrenze".

**Raten-Darstellung und Aggregation** (§3.6): nativ **YLL je 1.000 EW und Jahr**;
Teil-Ausweise: Zusatzfälle je 1.000 EW (je Entität), € je EW und Jahr; Quartier-Aggregat;
Kommune = Summe der Zellen.

## 7 Parameter-Blöcke (maschinenlesbar, §4)

```yaml
parameter:
  id: uv.ssd_delta_region
  wert: "backend/data/kalibrierung/ssd_povw.csv"
  einheit: "%"
  band: null   # Normalperioden-Vergleich 1961-90 vs. 1991-2020 (GP-Befund 37).
               # Befund 223: BEVOELKERUNGSgewichtet auf Gemeindepunkt-Ebene (DE 8,51 %;
               # nord/mitte/sued 7,82/9,15/7,77), weil das Produktionsmodell
               # bevoelkerungsgewichtet ueber Zellen summiert (Aufgabe §3.4). Die
               # flaechengewichteten Gebietsmittel in ssd_trend_region.csv [69] bleiben
               # Kontroll- und Trendgroesse (NRW-Trend fuer k_uv).
  herkunft: register:98-E20-01
  quelle: dwd_cdc_ssd_raster_x_vg250_x_zensus2022   # Befund 231: nicht das
          # Gebietsmittel, sondern DWD-Raster x VG250-Gemeindepunkte x Zensus-Gewichtung
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.k_uv
  wert: 0.7119
  einheit: "-"
  band: [0.3622, 1.0616]   # PUBLIZIERTE STANDARDFEHLER beider Stationstrends,
                        # unkorreliert fortgepflanzt: SE 1,8/4,9 und 1,5/4,6 => +/-49,1 %
                        # (1 sigma). Konservativ, weil beide Reihen bewoelkungsgetrieben
                        # und damit positiv korreliert sind (Befunde 255/256). Die
                        # RAEUMLICHE Streuung des Rasterquotienten ist Modellgrenze 9,
                        # KEIN Band der Bundessumme.
                        # HERLEITUNGSWERT (4,9/4,6) x 0,6683 = 0,7119 - Bruecke ueber
                        # die Globalstrahlung, weil Zaehler (Stations-Dosis) und Nenner
                        # (Raster-SSD) aus zwei Messfamilien stammen und die Skalendifferenz
                        # METRIKabhaengig ist: an der Messzelle Bochum gibt das Raster die
                        # Globalstrahlung zu 0,98 wieder, die Sonnenscheindauer nur zu 0,59
                        # (Anlage k_uv_herleitung.py, Befunde 238/252). Beide Quotienten der
                        # Kette sind skalenfrei, ihr Produkt ist die Elastizitaet auf
                        # RASTERskala. Stationsquotient 4,9/4,6 aus [31] Tab. 2 und Tab. 4
                        # (Volltext); Rasterquotient 0,6683 bevoelkerungsgewichtet ueber
                        # 10.682 Gemeindepunkte (Baseline-Fall-Gewichtung).
                        # Historie: Rev. 3 4,9/5,81 = 0,8434 (NRW-Gebietsmittel, Befund 230);
                        # Rev. 4 4,9/6,48 = 0,7562 (halber Mismatch, Befund 238); Rev. 5  <!--hist-->
                        # Rev. 5: 0,5782; Rev. 6: 0,6667 (Stationsquotient geschaetzt, Befund 252).  <!--hist-->
                        # Elastizitaet zeitinvariant angenommen (Befund 222).
  herkunft: register:98-E20-02
  quelle: lorenz2024_dwd_ssd_trend
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.a_attr
  wert: 0.75
  einheit: "-"
  band: [0.5, 1.0]   # gekennzeichnete Abschaetzung (§3.2; GP-Befund 15)
  herkunft: register:98-E20-03
  quelle: lorenz2024_einordnung
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.baf
  wert: {mm: 0.6, c44: 1.675}
  einheit: "-"
  band: {mm: [0.2, 1.0], c44: [1.675, 1.95]}   # ueber w_scc-Band 0,25-0,50 (Befund 202)
  herkunft: register:98-E20-04
  quelle: slaper1996_rivm2023_madronich2021
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.w_scc
  wert: 0.25
  einheit: "-"
  band: [0.25, 0.50]   # KID-2025-Primaerangabe; obere Stuetze BfS-2015-Split (Widerspruch benannt §3.1)
  herkunft: herleitung:#baf-c44
  quelle: zfkd_kid2025_bfs2015
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.i_raten_roh
  wert: {mm: {u20: 0.5, 20-64: 24.7, 65-74: 64.0, 75-84: 94.9, 85+: 88.5},
         c44: {u20: 2.0, 20-64: 125.9, 65-74: 617.6, 75-84: 1267.2, 85+: 1479.5}}
  einheit: "1/100000a"
  band: null   # ROH-Ablesewerte, gepoolt 2021-2023 (Anlage kid2025_ablesewerte.csv);
               # Normierung via uv.c_kal in der Formel (Befund 201); Altersprofil
               # out-of-sample gegen die amtliche ASR bestaetigt (Befund 214);
               # ZfKD-Datenbankabfrage als Ersetzungspfad
  herkunft: register:98-R35-01
  quelle: zfkd_kid2025
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.lambda
  wert: {mm: 0.11466, c44: 0.005236}
  einheit: "-"
  band: null   # Perioden-Approximation, gekennzeichnet (GP-Befund 43); Zaehler und
               # Nenner im Ankerfenster 2021-2023 (Befund 220)
  herkunft: register:98-K1-02
  quelle: zfkd_kid2025
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
parameter:
  id: uv.l_rest
  wert: {mm: 10.4569, c44: 5.4787}
  einheit: "Jahre"
  band: null   # Median-Approximation, gekennzeichnet (GP-Befund 43). Befund 224:
               # sterbefallgewichtet ueber ALLE Jahre UND Geschlechter des Ankerfensters
               # (Stuetzstelle = medianes Sterbealter DES JEWEILIGEN JAHRES), nicht mehr
               # aus dem Einzeljahr 2023 (10,58/5,30) — einheitliche Jahres-Auswahlregel
               # wie Anker, c_kal und lambda (Aufgabe §3.4)
  herkunft: register:98-K1-02
  quelle: zfkd_kid2025_sterbetafel2224
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
parameter:
  id: uv.c_fall
  wert: {mm: 6724, c44: 5883}
  einheit: "EUR/Fall"
  band: {mm: [6724, 11410], c44: [5883, 7436]}   # SCS- vs. nicht-SCS-detektiert; Proxy §3.4
  herkunft: register:98-K1-01
  quelle: speckemeier2022
  preisstand: "2024"
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: morbiditaet
parameter:
  id: uv.voly
  wert: 160800
  einheit: "EUR/Jahr"
  band: [136400, 165600]
  herkunft: herleitung:#voly   # Kette in #95 §3.5 (P52)
  quelle: uba_mk40_amann2020a
  preisstand: "2024"
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: mortalitaet
parameter:
  id: uv.c_kal
  wert: {mm: 1.0012, c44: 0.9910}
  einheit: "-"
  band: null   # Normierungsskalar je Entitaet; wirkt in der §3.3-Formel auf uv.i_raten_roh
               # (Befund 201). Anker = Mittel 2021-2023 (MM 26.870 / C44 240.973), also
               # dasselbe Fenster, ueber das die Ablesewerte gepoolt sind (Befund 220).
               # Auswahlregel-Sensitivitaet: Einzeljahre -4,3 ... +2,8 % auf die EUR-Summe
  herkunft: herleitung:#i-raten
  quelle: zfkd_kid2025
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.r_out_sensitivitaet
  wert: 1.0
  einheit: "-"
  band: [0.981, 1.038]   # HERGELEITET aus q_out in [0; 0,21] statt gesetzt (Befund 219);
                         # 0,21 = 3x Bundesmittel, gekennzeichnete Abschaetzung solange die
                         # Ebene geparkt ist. Basiswert-Default 1 (GP-Befund 9, Ebene
                         # geparkt => q = q_quer); Formel §3.4 (w_Z = 0,373; Befund 206)
  herkunft: register:98-OUT-01
  quelle: schmitt2011_destatis_vgr
  preisstand: null
  bandzuordnung: [20-64, 65-74, 75-84, 85+]   # NICHT u20: die Evidenz ist eine Meta-Analyse
                                              # BERUFLICHER Exposition, zentriert auf den
                                              # Erwerbstaetigen-Anteil (Befund 218). Fuer 65+
                                              # gekennzeichnete Kohorten-Approximation.
  endpunkt: beide
# Kein-Doppelkanal (§3.2): v_verh ist KEIN eigener Parameter, sondern wird aus den
# beiden unabhaengigen Groessen s (Tageswert) und phi (Komforttag-Anteil) gerechnet:
# v_verh = 1 + phi*(s-1); bei geparkter phi-Ebene exakt 1 (Befund 216).
parameter:
  id: uv.s_komforttag
  wert: 1.45
  einheit: "-"
  band: [1.25, 1.60]   # TAGES-Multiplikator der persoenlichen Dosis an einem Komforttag:
                       # +1,2 min/degC Aussenzeit (ATUS, Basis 44 min) x DeltaT 10 degC
                       # = +27 %; Dosis-Zeit-Kopplung R^2 0,75-0,79; Kleidung +15 %
  herkunft: register:98-S154-01
  quelle: graffzivin_neidell2014
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide
parameter:
  id: uv.phi_komfort
  wert: 0.0
  einheit: "-"
  band: [0.0, 0.25]   # dosisgewichteter Komforttag-Anteil; Ebene GEPARKT (Datenquelle
                      # fehlt: DWD-Tagestemperatur x Tagesdosis nicht keyless in dieser
                      # Kombination). Neutralwert 0 => v_verh exakt 1 (§3.1/§3.6).
                      # Obergrenze 0,25 gekennzeichnete Abschaetzung (§3.4)
  herkunft: herleitung:#v-verh
  quelle: graffzivin_neidell2014
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide

parameter:
  id: uv.i_mm
  wert: {u20: 0.5, a20_64: 24.7, a65_74: 64.0, a75_84: 94.9, a85p: 88.5}
  einheit: "1/100.000·a"
  band: null   # Ableseunsicherheit der Kette ist in der Struktur-Validierung
               # abgebildet (2 sigma = +/-10,1 %, Anlage [71]), nicht als
               # Parameter-Band: die Raten sind gemeinsam abgelesen und korreliert.
  herkunft: herleitung:#anker
  quelle: zfkd_kid2025   # Abb. 3.13.2, altersspezifische Rohraten Melanom (C43)
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]   # bandweise Raten;
               # die Ableseunsicherheit wirkt ueber die Struktur-Validierung,
               # nicht als eigenes Ergebnisband (Befund 373)
  endpunkt: beide

parameter:
  id: uv.i_c44
  wert: {u20: 2.0, a20_64: 125.9, a65_74: 617.6, a75_84: 1267.2, a85p: 1479.5}
  einheit: "1/100.000·a"
  band: null   # wie uv.i_mm — gemeinsame Ablesekette, Toleranz in der
               # Struktur-Validierung (Anlage [71]).
  herkunft: herleitung:#anker
  quelle: zfkd_kid2025   # Abb. 3.14.2, altersspezifische Rohraten heller Hautkrebs (C44)
  preisstand: null
  bandzuordnung: [u20, 20-64, 65-74, 75-84, 85+]
  endpunkt: beide

parameter:
  id: uv.or_out
  wert: 1.77
  einheit: "Odds Ratio"
  band: [1.37, 2.30]   # 95-%-KI der Meta-Analyse; Kohorten-Teilmenge 1,68 [1,08-2,63]
  herkunft: register:98-OUT-01
  quelle: schmitt2011_destatis_vgr   # Meta-Analyse, SCC bei Aussenberufen
  preisstand: null
  bandzuordnung: [20-64, 65-74, 75-84, 85+]   # Aussenberufe: nicht u20
               # (Befunde 218/373); wirkt nur ueber r_out, nicht im Basiswert (§3.4)
  endpunkt: beide

parameter:
  id: uv.qbar_out
  wert: 0.07
  einheit: "Anteil"
  band: [0.0, 0.21]   # 0 = Ebene geparkt; 0,21 = dreifacher Bundesanteil als
                      # Obergrenze fuer stark landwirtschaftlich gepraegte Kommunen
  herkunft: herleitung:#q-out
  quelle: schmitt2011_destatis_vgr   # (572+2.643)/45.909 Tsd. = 0,070
  preisstand: null
  bandzuordnung: [20-64, 65-74, 75-84, 85+]   # nicht u20 (Befund 218)
  endpunkt: beide

parameter:
  id: uv.r_out_enabled
  wert: 0.0
  einheit: "Schalter"
  band: [0.0, 1.0]   # 0 = aus (Basiswert, §3.4: Aussenberufs-Ebene ist geparkt);
                     # 1 = an, sobald eine kommunale Aussenberufs-Quote vorliegt
  herkunft: register:98-OUT-01
  quelle: schmitt2011_destatis_vgr   # Schalter der r_out-Ebene; Evidenz wie or_out
          # (Befund 374: keine Selbstreferenz auf den eigenen Bericht)
  preisstand: null
  bandzuordnung: [20-64, 65-74, 75-84, 85+]   # nicht u20 (Befund 218)
  endpunkt: beide
```


## 8 Quellen (§3.8 — #98-relevanter Auszug; Nummern = M0-Zählung, [69]–[74] neu)

Zugriff 17./18.08.2026 ([27], [31], [34], [43], [70]: 30.08.2026 primär
verifiziert/neu gezogen). **Archiv-Snapshots:** wie #95 Kap. 8 (Ratchet bei Integration).

- **[19]** UBA, „Methodenkonvention 4.0" (umweltbundesamt.de); Amann u. a. 2020a
  (VOLY-Kette vollständig in #95 §3.5, Archiv-Link dort); Destatis-VPI lange Reihen,
  destatis.de (2020 = 100: 2015 = 94,5 · 2024 = 119,3; geprüft gegen die
  Basis-2020-Tabelle).
- **[27]** Zentrum für Krebsregisterdaten (ZfKD)/GEKID, „Krebs in Deutschland für
  2021–2023" (KID 2025), Kap. 3.13 (C43) und 3.14 (C44), krebsdaten.de —
  PDF-Kapitel **primär verifiziert 31.08.2026** (Rev. 2):
  `.../Krebs_in_Deutschland/kid_2025/kid_2025_c43_melanom.pdf` und
  `.../kid_2025_c44_nicht-melanotischer-hautkrebs.pdf`.
  **Tab. 3.13.1 (C43)**, Frauen/Männer je Jahr — Neuerkrankungen 2021 12.350/13.790 ·
  2022 12.810/14.230 · 2023 12.960/14.470; standardisierte Neuerkrankungsrate
  (alter Europastandard) 20,7/22,3 · 21,0/22,9 · 21,1/22,9; mittleres (medianes)
  Erkrankungsalter 63/68 · 64/69 · 64/69; Sterbefälle 1.236/1.692 · 1.293/1.853 ·
  1.318/1.851; mittleres Sterbealter 78/76 · 78/77 · 78/76.
  **Tab. 3.14.1 (C44)** — Neuerkrankungen 111.030/125.640 · 115.490/127.940 ·
  116.610/126.210; standardisierte Rate 139,0/173,7 · 142,8/175,8 · 143,8/172,7;
  mittleres Erkrankungsalter 74/76 (alle Jahre); Sterbefälle 464/714 · 521/754 ·
  541/791; mittleres Sterbealter 88/84 · 88/84 · 88/85.
  Fußnoten: „je 100.000 Personen · altersstandardisiert nach **alter Europabevölkerung**
  · **Median**". Kap. 3.14 Fließtext (wertetragend für \(w_{\text{SCC}}\), Befund 202):
  „Knapp drei Viertel der nicht-melanotischen Hautkrebsformen … sind Basalzellkarzinome …
  Etwa ein Viertel der Fälle sind Plattenepithelkarzinome, die vor allem ältere Personen
  betreffen"; ebenda der Vermerk, die Jahresfallzahlen seien **geschätzt**
  (Vollzähligkeitskorrektur — Revisionsstand §4).
  Abb. 3.13.2/3.14.3: „Altersspezifische Neuerkrankungsraten nach Geschlecht …,
  Deutschland **2021 – 2023**" — die Ablesekette (§3.3) ist damit über drei Jahre
  gepoolt, was das Ankerfenster festlegt (Befund 220); Entitäten-Split 2015
  (BCC 158.840 · SCC 98.950 · MM 35.495) nach S. Baldermann, C. Lorenz,
  Bundesgesundheitsbl 62:639–645, 2019, doi:10.1007/s00103-019-02934-w
  (**Sekundärangabe**, Volltext-Verifikation als Ersetzungspfad).
- **[28]** Destatis, Krankheitskostenrechnung C43–C44: 2023: 1.823 Mio. € (GENESIS
  23631-0003); Destatis PM N036 (28.05.2026): stationäre Hautkrebsfälle 2004–2024
  +94,5 %, Sterbefälle 2024: 4.600.
- **[29]** H. Slaper, G. J. M. Velders, J. S. Daniel, F. R. de Gruijl, J. C. van der Leun,
  „Estimates of ozone depletion and skin cancer incidence to examine the Vienna Convention
  achievements", Nature 384:256–258, 1996. doi:10.1038/384256a0; BAF-Werte (SCC 2,5 ± 0,7 ·
  BCC 1,4 ± 0,4 · CM 0,6 ± 0,4) dokumentiert in RIVM Letter Report 2023-0426, S. 21 f.
- **[30]** S. Madronich u. a., ACS Earth Space Chem 5(8):1876–1888, 2021.
  doi:10.1021/acsearthspacechem.1c00183 (unabhängige BAF-Bestätigung 2,6/1,4/0,6).
- **[31]** S. Lorenz, F. Heinzl, S. Bauer, M. Janßen, V. De Bock, A. Mangold,
  P. Scholz-Kreisel, D. Weiskopf, „Increasing solar UV radiation in Dortmund, Germany:
  data and trend analyses and comparison to Uccle, Belgium", Photochem Photobiol Sci
  23(12):2173–2199, 2024. doi:10.1007/s43630-024-00658-8 — **Volltext primär
  verifiziert 01.09.2026** (Open Access). Wertetragende Fundstellen:
  **Tab. 2** (UV-Messung Dortmund, 1997–2022, mit Imputation): UVI_max +3,2 %/Dek.
  (SE 1,4; CI 0,4–6,0) · **H_er,day +4,9 %/Dek. (SE 1,8; CI 1,4–8,4)**; Uccle
  +5,8/+7,5. **Tab. 4** (DWD-Station **1117 Bochum**, 10 km von der UV-Station —
  Messort von Globalstrahlung und Sonnenscheindauer): GR_max +3,0 (SE 0,9) ·
  **GR_int +4,6 %/Dek. (SE 1,5; CI 1,6–7,7)** · **SunD +11,3 %/Dek. (SE 2,3;
  CI 6,7–15,9)** · TCO ganzjährig +0,1 (n. s.) · **TCO Apr–Sept −0,9 %/Dek.
  (SE 0,4; CI −1,75…−0,03, signifikant)**. **Kap. 2** (Messaufbau): „For the location
  Dortmund, a GR and SunD data set was used measured by the DWD at a meteorological
  station (DWD ID 1117) in the city of Bochum (10 km from the UV monitoring station)";
  „GR is largely unaffected by current TCO levels but is primarily influenced by
  factors, such as aerosol optical depth (AOD) and cloudiness. SunD, on the other
  hand, is mainly influenced by cloudiness alone." **Abstract**: „Global radiation
  increases similarly to the UV data, and sunshine duration in Dortmund increases
  about twice as much as global radiation, suggesting a strong influence of change in
  cloud cover." BfS-PM 017/2024.
- **[32]** R. Vitt u. a. (2020): UV-Index satellitengestützt +1,2–3,6 %/Dekade; K.
  Eleftheratos u. a. (2020): UV-B-Projektion +1,3 %/Dekade 2050–2100 — beide zit. n.
  KWRA 2021 TB5, umweltbundesamt.de (lokal: `docs/KWAR/`); nur Band-/Rahmenstützen,
  nicht wertetragend.
- **[33]** DWD Climate Data Center (CDC): Raster sunshine_duration (1 km);
  Gebietsmittel Sonnenscheindauer (regional_averages_sd_year.txt) — Grundlage von [69];
  Lizenz DL-DE->Zero-2.0.
- **[34]** C. Speckemeier u. a., „One-year follow-up healthcare costs of patients
  diagnosed with skin cancer in Germany: a claims data analysis", BMC Health Serv Res
  22:749, 2022. doi:10.1186/s12913-022-08141-9 (PMC9188701, Volltext-Abstract primär
  verifiziert 30.08.2026: AOK-Routinedaten, Diagnosekohorte 2014/2015; MM 5.326
  [SCS-detektiert] vs. 9.038 € [nicht-SCS]; NMSC 4.660 vs. 5.890 €; DiD: SCS senkt
  MM-Erstjahreskosten um 18,8 % [8,4–23,1]).
- **[35]** Leitlinienprogramm Onkologie, „S3-Leitlinie Prävention von Hautkrebs",
  Version 2.1, Sept. 2021, leitlinienprogramm-onkologie.de (Latenz „Jahrzehnte").
- **[36]** BfS, PM 005/2022, bfs.de; S. Baldermann, C. Lorenz, Bundesgesundheitsbl
  62:639–645, 2019. doi:10.1007/s00103-019-02934-w (Erratum doi:10.1007/s00103-019-03001-0;
  keine quantifizierte Mehr-Exposition je Komforttag publiziert).
- **[37]** S. T. Shih u. a. (2009/2017, Prev Med); C. M. Doran u. a. (2016, PLOS ONE);
  L. G. Collins u. a. (2024, Health Promot Int): Benefit-Cost 2,2–8,7 : 1 (AUS/USA/EU;
  Fundstellen via PubMed dokumentiert); Baldermann & Weiskopf 2020: keine deutsche
  Kosten-Nutzen-Studie — **keine Effektgrößen, nicht wertetragend** (§5; qualitativer
  Hebel).
- **[43]** J. Schmitt u. a., „Occupational ultraviolet light exposure increases the risk
  for the development of cutaneous squamous cell carcinoma: a systematic review and
  meta-analysis", Br J Dermatol 164(2):291–307, 2011. doi:10.1111/j.1365-2133.2010.10118.x
  — Abstract primär verifiziert 30.08.2026: Fall-Kontroll-Pool OR 1,77 [1,37–2,30],
  Kohorten 1,68 [1,08–2,63]; Grundlage BK 5103.
- **[48]** Destatis, Sterbetafel 2022/2024 (Blätter 12613-b01/-b02, destatis.de), Spalte
  „Durchschnittliche Lebenserwartung“ — **alle sechs im Ankerfenster benötigten
  Stützstellen** (Befund 236): e(78)F = **10,9187** · e(76)M = **10,3350** ·
  e(77)M = **9,7311** · e(88)F = **5,0374** · e(84)M = **5,9397** · e(85)M = **5,4745**; Bevölkerung 31.12.2023 nach
  Altersjahren (Statistischer Bericht 5124108237005, Tab. 12411-06) — Gewichte §3.3;
  Männeranteil 85+ = 990.292/2.844.213 = 0,348.
- **[57]** J. Graff Zivin, M. Neidell, „Temperature and the Allocation of Time",
  J Labor Econ 32(1):1–26, 2014. doi:10.1086/671766 (ATUS; Outdoor-Freizeit ≈ +1,2 min/°C).
- **[58]** „Intraday adaptation to extreme temperatures in outdoor activity", Sci Rep 2023,
  ncbi.nlm.nih.gov/pmc/PMC9832153 (−5 % > 30 °C, −13 % > 35 °C); US-Dosimeterkohorte
  ncbi.nlm.nih.gov/pmc/PMC3566166.
- **[59]** J. Sun u. a., J Photochem Photobiol B 2014 (Kleidung, nur Richtung);
  A. W. Schmalwieser u. a., Br J Dermatol 2021, doi:10.1111/bjd.20703 (Zeit im Freien
  erklärt persönliche Dosis, R² 0,75–0,79).
- **[69]** SSD-Trend-Auswertung: `backend/scripts/kalibrierung/dwd_ssd_trend.py` +
  `backend/data/kalibrierung/ssd_trend_region.csv` (Normalperioden-Mittel je Bundesland
  **und** Region + linearer Trend 1997–2022; Lauf 30.08.2026; DE 1.544,0 → 1.664,8 h
  = +7,82 %; NRW-Trend 5,81 %/Dekade); Ablese-Anlage:
  `backend/data/kalibrierung/kid2025_ablesewerte.csv` (Befund 204).
- **[70]** Destatis, „Erwerbstätige und Arbeitnehmer nach Wirtschaftsbereichen
  (Inlandskonzept)", destatis.de (Abruf 30.08.2026): 2023 gesamt 45.909 Tsd.;
  Land-/Forstwirtschaft/Fischerei 572 Tsd.; Baugewerbe 2.643 Tsd. ⇒
  \(\bar q_{\text{out}}\) = 0,0700.
- **[74]** S. Lorenz u. a., „Increasing Solar UV Radiation in Dortmund, Germany, and
  Uccle, Belgium", **Konferenz-Abstract** IUPB/MEPSA 2024,
  iupb-mepsa-2024.m.asnevents.com.au/schedule/session/23372/abstract/104789
  (Zugriff 01.09.2026). **Nicht mehr wertetragend** (Rev. 7): Alle in Rev. 5/6 von
  hier bezogenen Angaben stehen im **Volltext** von [31] (Tab. 2/4, Kap. 2), der seit
  01.09.2026 vorliegt. Der Konferenz-Abstract bleibt als Zweitfundstelle zitiert.
- **[73]** \(k_{\text{UV}}\)-Herleitung auf Rasterskala (Befunde 230/238/239/245/252/255/256):
  `backend/scripts/kalibrierung/k_uv_herleitung.py` →
  `backend/data/kalibrierung/k_uv_herleitung.{csv,md}` (Lauf 01.09.2026):
  SSD- **und** Globalstrahlungstrend 1997–2022 aus den DWD-CDC-1-km-Jahresrastern
  ([33] bzw. `grids_germany/annual/radiation_global`, DL-DE→Zero-2.0), abgelesen an
  der **Messzelle Bochum** (SSD 6,62 · GR 4,51 %/Dek.) und an **10.682
  Gemeindepunkten** (BKG VG250 × Zensus 2022). Der geführte Quotient **0,6683**
  ist **fallgewichtet** (Baseline-Fälle × ΔSSD, Befund 278) — *nicht*
  bevölkerungsgewichtet; Median der Punktverteilung 0,6305. Beide Raster sind
  einzeln verzeichnet: Sonnenscheindauer [33] für den Nenner, Globalstrahlung
  (Registry-Quelle `DWD_CDC_Globalstrahlung_Raster`, Zugriff 03.09.2026, Archiv
  dort) für den Zähler. \(k_{\text{UV}}\) = (4,9/4,6) × 0,6683 = **0,7119**;
  Band **0,3622–1,0616** aus den publizierten Standardfehlern (±49,1 %, 1 σ).
  Ersetzt die Rev.-4-bis-6-Anlage `ssd_dortmund_k_uv.py`.
- **[72]** Bevölkerungsgewichtete SSD-Normalperiodenänderung (Befund 223):
  `backend/scripts/kalibrierung/ssd_povw.py` →
  `backend/data/kalibrierung/ssd_povw.{csv,md}` (Lauf 01.09.2026). Gewichtung auf der
  **Gemeindepunkt-Ebene** (§3.4 ausdrücklich zulässig): 10.824 amtliche Gemeindepunkte
  aus **BKG VG250** — Bundesamt für Kartographie und Geodäsie, „Verwaltungsgebiete
  1:250 000 (VG250), Ebene `vg250_pk` (Verwaltungspunkte)", **Stand 01.01.2025**, UTM32s-GPKG,
  gdz.bkg.bund.de (Zugriff 07.07.2026; Lizenz **DL-DE→BY-2.0**; lokal
  `backend/data/vg250/DE_VG250.gpkg`) —, gewichtet mit der **Zensus-2022**-Gemeinde-
  bevölkerung (Destatis, Zensus 2022 Gemeindeergebnisse, Stichtag 15.05.2022,
  zensus2022.de; Produkt-Aggregat `backend/data/lite/zensus_gemeinde.json`); die
  SSD-Normalperioden werden über die **Produktfunktion**
  `app.services.climate.ssd_normalperioden.ssd_at` gelesen, damit Kalibrier- und
  Produktionspfad nicht divergieren können. Ergebnis: DE **8,51 %**
  bevölkerungsgewichtet gegen 7,82 % flächengewichtet (+8,8 %); ungewichtetes
  Punktmittel 7,76 % als Kontrolle; Regionen nord/mitte/süd 7,82/9,15/7,77 %;
  Länder 4,79 % (MV) … 12,09 % (ST). **Gekennzeichnete Näherungen (§3.9; Befund 235):**
  (a) Gewichtet wird mit **Köpfen**, das Produktionsmodell summiert **Baseline-Fälle** —
  weil die Altersstruktur regional variiert, ist der exakte Bezug die fallgewichtete
  ΔSSD (Abweichung auf Landesebene **+0,11 %** MM / **+0,19 %** C44 relativ);
  (b) die Gemeindebevölkerung wird an **einem** Punkt abgelesen (Berlin 3,59 Mio an
  einer 1-km-Zelle) — gegen ein Boxmittel gerechnet **−0,28 %** relativ. Beide sind
  klein und teils gegenläufig; der Wert 8,51 % trägt. Die Kontrollgröße
  „Punktmittel ≈ Flächenmittel" belegt sie **nicht** (sie mittelt über Gemeinden, nicht
  über Fläche: RP 2.266 Punkte für 4,1 Mio EW gegen NRW 395 Punkte für 17,8 Mio EW) —
  sie zeigt nur, dass die Punktablesung als solche unverzerrt ist.
- **[71]** Baseline-Verankerung und Struktur-Validierung:
  `backend/scripts/kalibrierung/kid2025_baseline.py` →
  `backend/data/kalibrierung/kid2025_baseline.md` (Lauf 31.08.2026): Anker 2021–2023,
  \(c_{\text{kal}}\), \(\lambda_e\), \(\bar L_e\), ASR-Vergleich gegen [27],
  Bundessummen und die Einzelbänder (§4). Standardbevölkerung: **alter Europastandard**
  (0–19 = 29.000; 20–54 je 7.000; 55–59 6.000; 60–64 5.000; 65–69 4.000; 70–74 3.000;
  75–79 2.000; 80–84 und 85+ je 1.000 — Summe 100.000), wie in der [27]-Fußnote
  bezeichnet.

## 9 Familien-Einordnung & Verworfen-Liste (§2.6 — kein erneuter Drei-Ansätze-Vergleich)

#98 ist Folge-Risiko der Familie **„K1-Gesundheit bottom-up"** (Prototyp #95; vollständiger
Ansatz-Vergleich für #98 in M0 Rev. 5 Kap. 4/5). Verworfene Alternativen (§2.6):

- **98-B — Reine Dosis-Wirkungs-Kette (BfS-/Satelliten-UV-Klimatologie):** methodisch
  strengste Kette, aber die UV-Rasterbeschaffung ist ein eigenes Datenprojekt (keine freie
  Rasterklimatologie gefunden [31,36]) und der KWRA-Verhaltenspfad entfiele —
  dokumentierte Alternative für M1+ (Parameter bis zur Quelle in M0 Kap. 4).
- **98-C — Nationaler Kostenanker, top-down:** per §3.1 ausgeschieden (Verteilschlüssel;
  normatives \(a_{\text{klima}}\); Deutschland-Nenner) — nur Negativ-Beispiel.

## Entscheidungslog

Einträge 1: M0-Entscheidung (rückwirkend dokumentiert). Einträge 2–15: Rev.-1-
Entscheidungen (`/risiko-auto 98`, Gate 1, 30.08.2026); Aktualisierungen nach
Review-Runde 1 (Befunde 202/203) in den Zeilen 5, 9, 12 vermerkt.
**Einträge 16–18: Rev.-2-Entscheidungen** (Review-Runde 4, Gate 1, 31.08.2026).
**Einträge 19–22: Rev.-3-Entscheidungen** (Review-Runde 5, Gate 1, 01.09.2026;
Entscheidungsregeln W1–W6 aus `.claude/methodik-loop.md` zitiert).
**Eintrag 23: Rev.-4-Entscheidung** (Review-Runde 6, Gate 1, 01.09.2026).
**Eintrag 24: Rev.-5-Entscheidung** (Review-Runde 7, Gate 1, 01.09.2026).
**Eintrag 25: Rev.-6-Entscheidung** (Review-Runde 8, Gate 1, 01.09.2026).
**Eintrag 26: Rev.-7-Entscheidung** (Review-Runde 9, Gate 1, 01.09.2026).
**Eintrag 27: Rev.-8-Entscheidung** (Review-Runde 10, Gate 1, 01.09.2026).
**Eintrag 28: Rev.-9-Entscheidung** (Review-Runde 11, Gate 1, 01.09.2026).
**Eintrag 29: Rev.-11-Entscheidung** (Review-Runde 13, Gate 1, 01.09.2026).
**Überstimmungsweg:** „Entscheidung Nr. X ändern auf …" → Delta-Lauf (Neurechnung +
Re-Review + PDF-Neuexport). ⚠ = Ermessensfall.

| Nr | Frage | angewendete Entscheidung | Begründung | Alternative | Auswirkung |
|---|---|---|---|---|---|
| 1 | Methodischer Ansatz für #98? | **98-A** amtliche Inzidenz + BAF-Trend-Attribution (Familie K1-Gesundheit bottom-up) | jede Komponente amtlich/publiziert; minimale Datenanbindung (M0 Kap. 5) | 98-B (UV-Datenprojekt, M1+); 98-C ausgeschieden | Gesamtmodell |
| 2 ⚠ | k_UV-Paarung? | **abgelöst durch Nr. 23** (Rev. 4). Stand Rev. 3: 0,8434 = Dosistrend 4,9 [31] ÷ NRW-Gebietsmittel 5,81 [69] (gleiches Fenster, gleiche Datenfamilie wie das Produkt); Band 0,4–1,0 | M0-Kette 4,9/11,3 = 0,43 beruhte auf unbelegtem Stationstrend (GP-Befund 10/16); Raster-konsistente Paarung; Satelliten-Plausibilisierung ✓ | 0,43 (Stations-Paarung — untere Bandstütze; Volltext-Fundstelle als Ersetzungspfad) | Klimasignal ×1,95 ggü. M0; dominanter Bandtreiber |
| 3 ⚠ | Attribution des SSD-Trends? | **a_attr,UV = 0,75** (0,5–1,0), gekennzeichnete Abschätzung | GP-Befund 15 (Konsistenz zur #96-Logik); Lorenz-Wolkenbefund hoch, Aerosol-Brightening < 1,0 | 1,0 (M0, unattribuiert — verworfen) | −25 % ggü. M0-Logik; Band ±33 % |
| 4 | SSD-Fenster? | **Klimanormalperioden je Zelle** (1961–90 vs. 1991–2020) | GP-Befund 37; Einzeljahre zu variabel | gleitende Fenster | reproduzierbar |
| 5 ⚠ | Altersspezifische Inzidenz? | **Ablesekette aus KID-Abb.** (Roh-Ablesewerte als Anlage-CSV; geschlechtsspezifische Bevölkerungsgewichte [48]) + Normierung auf amtliche Rohraten (ein Skalar je Entität, wirkt in der Formel — Befunde 201/204) | ZfKD-Datenbank nicht keyless (dokumentierte Lücke); Winklmayr-Ablese-Präzedenz #95; Validierung −2,2 %/+0,1 % ∈ ±15 % (nach Befund 212) | warten auf ZfKD-Abfrage (blockiert M0) | Baseline exakt ZfKD-verankert |
| 6 | Native Ergebnisgröße? | **YLL/Jahr**; ΔFälle je Entität, € Teil-Ausweise | GP-Befund 28; K1-Mortalität + Morbidität | ΔFälle nativ | Ausweis |
| 7 ⚠ | Fallkosten-Basis? | **SCS-detektierte Erstjahreskosten** (MM 6.724 / C44 5.883 €₂₀₂₄); nicht-SCS als Obergrenze; Proxy gekennzeichnet; Preisstand-Annahme 2015 | Untergrenzen-Zusage (#95-Befund-62-Lehre); Gesamt- vs. inkrementelle Kosten diskutiert (§3.4) | nicht-SCS-Werte (M0-Wahl 9.038/5.890) | Behandlungs-€ −21 % ggü. M0-Wahl |
| 8 | λ_e / L̄_e? | Quotienten **im Ankerfenster 2021–2023** + Sterbetafel-Kette (aktualisiert nach Nr. 16 und Nr. 20); **Approximationen gekennzeichnet** | GP-Befund 43 (Perioden-/Median-Approximation, Richtung benannt) | Kohorten-Letalität (Datenprojekt) | Mortalitätspfad ehrlich |
| 9 ⚠ | Entitäten-Split C44? | **SCC 25 % altersinvariant** (aktualisiert nach Befund 202: KID-2025-Primärangabe; Band 0,25–0,50 mit BfS-2015-Split 0,384 als oberer Stütze; Widerspruch benannt §3.8) | Primärquelle vor Sekundärangabe; GP-Befund 41 (Altersinvarianz dokumentiert) | 0,384 (BfS 2015 — M0-Wahl) | BAF_C44 1,675 statt 1,82; C44-Zusatz −8 % |
| 10 ⚠ | Außenberufe (kein Ketten-Knoten)? | **Sensitivitätsband, Basiswert-Default 1**; Evidenz + q̄_out = 0,070 vollständig hergeleitet; Ersetzungsweg = Arbeitsmappen-Fortschreibung + AP-Punkt | GP-Befund 9 (Kettentreue „nicht mehr, nicht weniger"); Aufnahme in den Basiswert erfordert Quellen-Fortschreibung (§1/LF 14) — nicht still ergänzen | dokumentierte Kettenerweiterung mit sofortiger xlsx-Fortschreibung | Bundessumme unverändert (zentriert); Zell-Differenzierung ±2 % entfällt vorerst |
| 11 | Verhaltens-Modulation (S154)? | **Default 1**, Band +0,25…+0,60 je Komforttag dokumentiert | keine DE-Effektgröße [36]; US-Evidenz nur Band; Ambient-Anteil schon in ΔDosis (Doppelzählungsschutz) | v_verh im Basiswert | Untergrenze der KWRA-Verhaltens-These |
| 12 | Maßnahmen-Hebel? | **beide qualitativ** (aktualisiert nach Befund 203): UV-Schutz/Kommunikation ohne Effektgröße; SCS-Förderung mit belegtem Sparpotenzial, aber Kostenwirkung bereits im Basiswert (Untergrenzen-\(c_e\)) | GP-Befunde 26/34 + Befund 203 (LF-4-Wächter); Detektionsmix-Parameter als Ersetzungspfad | Mix-Parameter sofort einführen (Datenlücke: kommunale SCS-Quoten) | Hebelliste ehrlich; kein Doppelzählungsrisiko |
| 13 | R36 im Basiswert? | **Default 1** (nur Schicht A) | keine Evidenz; Zugangseffekt steckt im SCS-Hebel | Distanz-Sensitivität | Basiswert schlanker |
| 14 ⚠ | Latenz-Behandlung? | **Gleichgewichtslesart** („eingelaufenes Risiko") + Pflicht-Infokasten; kein Latenz-Discounting | [35] nennt „Jahrzehnte" ohne Bezifferung; der Rechenschritt kumulative → jährliche Dosis steht in §3.4 mit Transient-Faktor \(\tau\) = 0,20–0,48 | Kohorten-Latenzmodell (M2+) | **Ergebnis wird gegenüber einer Jahres-Attribution überschätzt** — größte Einzelachse der §4-Bändertabelle (67–339 Mio) |
| 15 ⚠ | Kalibrierung? | **ein Normierungsskalar je Entität** an der ZfKD-Inzidenz (Werte s. Nr. 16); keine Zeitreihen-Kalibrierung des Klimaanteils (keine amtliche Reihe existiert — dokumentierte Ausnahme analog #96) | §3.4 („EIN Skalar"); Klimaanteil messungsbasiert (SSD/Dosis/BAF) | Fit an KKR-Kostenreihe (konfundiert durch Screening/Kodierung — verworfen) | Baseline amtlich exakt; Klimaanteil über Bänder |
| 16 ⚠ | Ankerfenster der Baseline? | **Mittel 2021–2023** (MM 26.870 · C44 240.973) statt Einzeljahr 2023 ⇒ c_kal 1,0012/0,9910, λ 0,11466/0,005236 | Befund 220: Die abgelesenen Altersraten sind laut Abbildungstitel über **genau diese drei Jahre gepoolt** — ein Einzeljahres-Anker hätte Zähler und Nenner in verschiedenen Fenstern geführt (§3.4 einheitliche Auswahlregel, §3.9 keine Kategorienfehler). Nebenbefund: Die Ablese-Validierung verbessert sich von −2,2 %/+0,1 % auf −0,1 %/+0,9 % | Einzeljahr 2023 beibehalten und die Differenz nur als Sensitivität ausweisen (Vorschlag des Befunds) | **€-Summe 378 → 367 Mio (−2,8 %)**; ΔF 20.900 → 20.760; YLL 1.580 → 1.521; alle Golden-Tests und die Registry nachgezogen |
| 17 ⚠ | Wirkungsort von v_verh? | **Jahresfaktor** \(v_{\text{verh}} = 1+\phi_{\text{Komfort}}(s-1)\); der Tageswert s = 1,45 bleibt Register-Zeile und ist **kein** Registry-Parameter; \(\phi\)-Ebene **geparkt**, Neutralwert 0 | Befund 216: Rev. 1 stellte ein Registry-Band [1,0–1,6] bereit, das als Tageswert definiert, im Modell aber auf die **Jahres**-ΔDosis multipliziert wurde — bei ~40 Komforttagen rund Faktor 9 zu hoch. §3.5 verlangt einen definierten Wirkungsort, §3.6 einen editierbaren Parameter mit gültiger Semantik | \(\phi\) sofort als Zellgröße bauen (DWD-Tagestemperatur × Tagesdosis — kein keyless Kombinationsdatensatz); oder v_verh ganz aus der Registry nehmen | Basiswert unverändert (Default 1); Band jetzt einstellbar und korrekt: 1,00–1,11 ⇒ € bis 409 Mio |
| 18 | k_UV in der Registry? | **0,8434** (Herleitungswert 4,9/5,81) statt gerundet 0,84 — **abgelöst durch Nr. 23–25 und 27; geltend ist 0,7119** (Befund 380) | Befund 213: Die gerundete Registry-Zahl erzeugte 0,5 % relative Divergenz zwischen Bericht und Produktion. §3.9 verlangt den Rechenschritt; die Gegenvariante (alle Prosa-Ergebniswerte auf die gerundete Kette umstellen) wäre teurer und ungenauer | Prosa auf 0,84 umstellen | Divergenz geschlossen; Ergebniswerte des Berichts sind aus der Registry exakt reproduzierbar |
| 19 ⚠ | Gewichtung der nationalen ΔSSD? | **Bevölkerungsgewichtet auf Gemeindepunkt-Ebene** (DE 8,51 % statt flächengewichtet 7,82 %); neue Anlage [72], die die SSD über die Produktfunktion liest | Befund 223 (**A**): Das Produktionsmodell summiert bevölkerungsgewichtet über Zellen; §3.4 erklärt Näherungswerte bei bevölkerungsgewichteter Exposition für unzulässig. **W1** (saubere Lösung erreichbar) + **W4** (Gemeindepunkt-Ebene statt Vollraster, Lesen über die Produktfunktion) | Flächenmittel beibehalten und die Abweichung nur als Näherung ausweisen — verworfen, weil §3.4 die Klasse ausdrücklich ausschließt und #95 sie in Rev. 8 bereits gelöst hat | **€ 367 → 401 Mio (+8,8 %)**; YLL 1.521 → 1.664; ΔF 20.763 → 22.595; Band 116–636 → 127–694 Mio |
| 20 | Fenster von L̄_e? | **Jahresmediane des Ankerfensters**, sterbefallgewichtet über alle Jahre und Geschlechter ⇒ MM 10,4569 · C44 5,4787 | Befund 224 (**B**): Bis Rev. 2 stand das Sterbealter des Einzeljahrs 2023 dort, begründet mit einer Konstanz, die Tab. 3.13.1/3.14.1 nicht hergeben (M 76/**77**/76 bzw. 84/84/**85**). §3.4 verlangt eine einheitliche Jahres-Auswahlregel, §3.9 die Neurechnung bei geänderter Basis. **W1** (Sterbetafel liegt vor) | 2023-Wahl beibehalten und als Auswahlregel begründen — verworfen, weil sie dann von Anker/c_kal/λ abwiche | L̄_MM −1,16 %, L̄_C44 **+3,37 %**; YLL netto +0,5 % |
| 21 ⚠ | Band 20–64 feiner führen? | **Nein — Restfehler beziffert und als Modellgrenze 7 geführt** (≈ ±4 % je Kommune); Bänderung unverändert | Befund 225 (**B**): Die feinere Lösung wäre fachlich richtig und die Daten liegen je Zelle vor — sie greift aber in `pollen_age_bands`/`zensus_loader`, also in die von #96 mitgenutzte Kette. **W2** (risikolokal vor Produktumbau) verlangt hier die risikolokale Variante; ein #98-eigener Zellsplit ohne Loader-Eingriff ist nicht möglich, weil die 5-Jahres-Gruppen nicht im CellContext ankommen. §3.9 deckt die bezifferte Näherung | Bänderung produktweit auf 20–44/45–64 umstellen (Ersetzungspfad, §6 Modellgrenze 7) — als **produktweiter** Schritt zu führen, nicht als #98-Alleingang | Bundessumme unberührt; kommunale Differenzierung ±4 % dokumentiert statt still |
| 22 | ASR-Toleranz? | **Hergeleitet: 2σ = ±10,1 %** (Rundung auf ±10,5 % in Rev. 4 zurückgenommen, Befund 234) aus der Ablesegenauigkeit, plus **Regressionsschranke ±3 %** im Golden-Test | Befund 229 (**C**): ±10 % waren in derselben Revision gesetzt worden, die das Ergebnis erzeugte. Die Fehlerfortpflanzung (σ = ±5,07 %) zeigt: der Wert war sachlich richtig, nur unbelegt. §3.9 gilt auch für Toleranzen | Toleranz willkürlich enger setzen — verworfen, weil sie dann nicht mehr die Ablesegenauigkeit abbildet | Toleranz belegt; zusätzlich eine Schranke, die eine Verschlechterung sichtbar macht |
| 23 ⚠ | Nenner von k_UV? (**abgelöst durch Nr. 24**) | **Ortsgleicher Raster-SSD-Trend** an der Dortmunder Messzelle (6,48 %/Dek., Mittel dreier Standorte, Anlage [73]) ⇒ \(k_{\text{UV}}\) = 4,9/6,48 = **0,7562**; Band **0,4336–1,0** mit der jetzt **belegten** Stations-Paarung als unterer Stütze | Befund 230 (**A**): (1) Der bis Rev. 3 verwendete Nenner war das **Bundesland**-Gebietsmittel NRW — Punktmessung im Zähler gegen Landesflächenmittel im Nenner, also derselbe Skalen-Mismatch, den Befund 223 für die nationale ΔSSD behoben hat, hier im ergebnissteigernden Sinn. (2) Der fünffach als „unbelegt" bezeichnete Stationstrend 11,3 %/Dek. steht im **Abstract der eigenen Primärquelle** [31] („Sunshine duration in Dortmund increases by 11.3 % per decade") — die tragende Begründung der alten Paarung war damit widerlegt. **W1** (saubere Lösung mit vorhandenen Daten erreichbar: 62 gecachte Jahresraster) + **W4** (drei Punktablesungen statt Vollraster) | Quellinterne Paarung 4,9/11,3 = 0,4336 — verworfen als **Basiswert**, weil das Produkt Raster-ΔSSD liest und ein Stationsnenner die Dosis systematisch unterschätzte; sie ist die untere Bandstütze | **€ 401 → 360 Mio (−10,3 %)**; YLL 1.664 → 1.492; ΔF 22.595 → 20.258; Band 127–694 → **138–694 Mio**; Ledger-Befund 16 (≡ GP-10) wieder geöffnet und neu geschlossen |
| 24 ⚠ | Skalenbruch zwischen k_UV-Zähler und -Nenner? (**Stationsquotient abgelöst durch Nr. 25**) | **Brücke über die Globalstrahlung**: \(k_{\text{UV}}\) = (Dosis/Global)\|Station × (Global/SSD)\|Raster = (4,9/5,65) × (4,32/6,48) = **0,5782**; Bandstützen **0,4336** (alles Station) und **0,6667** (alles Raster), beide gerechnet | Befund 238 (**A**) + 239 (**B**): Nr. 23 hatte nur den Nenner auf Rasterskala gezogen; Zähler und Nenner blieben in zwei Messfamilien, und die Register-Zeile behauptete fälschlich „gleiche Datenfamilie". Eigene Messung aus denselben 1-km-Rastern (26 Jahre, drei Standorte): Globalstrahlung **4,32 %/Dek.** gegen SSD 6,48 %/Dek. — das Raster gibt den Stations-**Globalstrahlungs**trend auf 0,76 wieder, den **SSD**-Trend nur auf 0,57. Die Differenz ist also metrik-, nicht glättungsbedingt, und die Primärquelle nennt die Brücke selbst („roughly twice as much as global radiation"; „primarily driven by changes in global radiation"). Beide Quotienten sind skalenfrei ⇒ ihr Produkt ist die Elastizität auf Rasterskala. **W1** (mit 26 Jahresrastern und drei Punktablesungen erreichbar) | (a) Quellinterne Stations-Paarung 4,9/11,3 = 0,4336 als Basiswert — verworfen, weil sie die Stationsskala auf die Zelle überträgt; sie ist die **untere** Stütze. (b) Reine Rasterkette 4,32/6,48 = 0,6667 (Dosis ≡ Globalstrahlung) — verworfen als Basiswert, weil sie die gemessene Dosis (4,9) verwirft; sie ist die **obere** Stütze | **€ 360 → 275 Mio (−23,6 %)**; YLL 1.492 → 1.141; ΔF 20.258 → 15.490; Band 138–694 → **138–463 Mio** (die obere Stütze 1,0 war nirgends hergeleitet und widersprach [31] — Befund 239) |
| 25 ⚠ | Stationsquotient Dosis/Globalstrahlung und k_UV-Band? (**abgelöst durch Nr. 26**) | **1,0 aus der Quelle** statt 0,867 geschätzt ⇒ k_UV = 1,0 × (4,32/6,48) = **0,6667**; **Band 0,3656–0,9187** aus der räumlichen Streuung über acht Standorte statt aus zwei Skalen-Grenzfällen | Befund 245 (**A**) + 239: [31] beziffert den Quotienten direkt — »Global radiation increases similarly to the UV data« —, Rev. 5 hatte ihn aus »roughly twice as much« zu 4,9/5,65 geschätzt und beide Sätze zudem dem **Abstract** zugeschrieben; sie stehen im Fließtext. **W1** verlangt die belegte Größe statt der Ersatzkonstruktion. Das alte Band bildete die tatsächlich dominierende Unsicherheit — die räumliche Übertragbarkeit — nicht ab: Über acht Standorte streut Global/SSD von 0,366 (Stuttgart) bis 0,919 (Freiburg) | Bundesweiter Median 0,700 als Basiswert — verworfen, weil der Stationsquotient nur in Dortmund belegt ist und die Ortsgleichheit die Kette trägt; die Streuung steht stattdessen im Band | **€ 275 → 317 Mio (+15,3 %)**; YLL 1.141 → 1.315; ΔF 15.490 → 17.860; Band 138–463 → **116–638 Mio**; die reine Stations-Paarung 0,4336 liegt innerhalb des Bandes |
| 26 ⚠ | k_UV nach Vorliegen des Volltexts? (**Gewichtung korrigiert in Nr. 27**) | **Stationsquotient 4,9/4,6 = 1,0652** aus [31] Tab. 2 und Tab. 4; **Rasterquotient 0,6683 bevölkerungsgewichtet** über 10.682 Gemeindepunkte an der richtigen Messzelle (**Bochum**) ⇒ k_UV = **0,7119**. Band aus den **publizierten Standardfehlern** (±49,1 %, 1 σ ⇒ 0,3622–1,0616); die räumliche Streuung wird **Modellgrenze 9** | Befunde 252 (**A**) und 255/256 (**B**): Der Nutzer hat den Volltext beschafft. Er beziffert beide Größen, die Rev. 5/6 geschätzt hatten, und zeigt, dass GR und SunD **nicht in Dortmund**, sondern an DWD-Station 1117 Bochum gemessen wurden. Die Metrikabhängigkeit ist damit direkt belegt: Das Raster gibt an der Messzelle die Globalstrahlung zu **0,98**, die Sonnenscheindauer nur zu **0,59** wieder. Das alte Band (Min/Max über acht handverlesene Städte) buchte eine *räumliche* Streuung als Band der *Bundes*summe — dieselbe Klasse, die der Bericht bei r_out korrekt als »Bundessumme unberührt« führt. **W1** | Rasterquotient an der Messzelle allein (0,6811 ⇒ k_UV 0,7256) — verworfen, weil für die **Bundessumme** der bevölkerungsgewichtete Wert zählt (Logik von Befund 223); der Messzellenwert steht als Vergleich in der Anlage | **€ 317 → 320 Mio (+1,0 %)**; YLL 1.315 → 1.329; Band 116–638 → **109–697 Mio**; Modellgrenze 9 neu; Befunde 16 und 252 endgültig geschlossen |
| 27 ⚠ | Womit wird der Rasterquotient gewichtet? (**präzisiert in Nr. 28**) | **pop × ΔSSD_Normalperiode** statt pop × SSD-Trend ⇒ q = **0,6683** (statt 0,6320), k_UV = **0,7119** | Befund 266 (**A**): Das Produktionsmodell multipliziert k_UV mit der Normalperioden-ΔSSD (1961–90 → 1991–2020), nicht mit dem Trend 1997–2022. Der nationale k_UV muss deshalb mit genau diesem Feld gewichtet sein — sonst summiert die Kalibrierung anders als die Produktion (§3.4). Die beiden SSD-Felder korrelieren nur mit **r = 0,24**, die Wahl ist also nicht neutral: +7,2 % auf den Quotienten. **W1** (mit den vorhandenen Rastern und `ssd_at` in einem Lauf erreichbar) | Gewichtung mit dem SSD-Trend beibehalten und die Differenz als Näherung ausweisen — verworfen, weil §3.4 die Übereinstimmung von Kalibrier- und Produktionsgewicht verlangt und die Lösung verfügbar ist | **€ 320 → 343 Mio (+7,2 %)**; YLL 1.329 → 1.423; ΔF 18.045 → 19.332; Band 109–697 → **116–747 Mio**; Modellgrenze 9 auf das richtige Gewicht gezogen |
| 28 | Kopf- oder Fallgewichtung des Rasterquotienten? | **Baseline-Fälle × ΔSSD** statt pop × ΔSSD ⇒ q = **0,6843**, k_UV = **0,7289**; die Entitätsdifferenz (MM 0,6674 · C44 0,6689) wird als €-gewichtetes Mittel geführt und die Restdifferenz < 0,2 % als Näherung gekennzeichnet | Befund 278 (**B**): Das Produktionsmodell summiert ΔF = Σ F_z · BAF · ΔDosis_z — gewichtet wird also mit **Fällen**, nicht mit Köpfen. Weil die Altersstruktur regional variiert, sind beide nicht identisch (+0,8 % MM / +1,2 % C44). Damit trägt auch die Exaktheitszusage in Modellgrenze 9 wieder (»nahezu unberührt« statt »unberührt«). **W1** | Zwei entitätsspezifische k_UV führen — verworfen, weil die Differenz (< 0,2 %) gegen das Band (±49 %) verschwindet und der Modellaufbau je Entität einen zweiten Parameter bräuchte | **€ 343 → 347 Mio (+1,0 %)**; YLL 1.423 → 1.438; Band 116–747 → **118–754 Mio** |
| 29 | Aggregationsregel des Rasterquotienten? | **Punkte mit SSD-Trend < 1 %/Dekade ausgeschlossen**; Regel in der Anlage dokumentiert und die Ergebnis-Sensitivität ausgewiesen ⇒ q = **0,6683**, k_UV = **0,7119** | Befund 297 (**B**): Seit der Fallgewichtung (Nr. 28) ist q ein gewichtetes **Mittel der Punktquotienten**, nicht mehr ein Quotient getrennt summierter Zähler und Nenner. Der Code-Kommentar rechtfertigte die Einbeziehung instabiler Punkte noch mit der alten Formel. 57 Punkte (0,08 % Gewicht) erreichen q bis **196** und hoben den Bundeswert um **+2,3 %** — ein numerisches Artefakt, kein Messergebnis. §3.9 verlangt die Aggregationsregel ausdrücklich | Instabile Punkte behalten und die Verzerrung als Näherung ausweisen — verworfen, weil q dort durch Division durch ~0 entsteht und keine physikalische Bedeutung hat | **€ 347 → 339 Mio (−2,3 %)**; YLL 1.438 → 1.404; Band 118–754 → **115–737 Mio** |

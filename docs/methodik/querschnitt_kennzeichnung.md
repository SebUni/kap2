# Querschnitt: Kennzeichnung berechneter Parameter

Querschnittsdatei der Methodik, gültig für alle 102 Klimawirkungen der KWRA 2021. Angewendet wird sie heute nur auf
#95, #96 und #98 (A-0048; Vorhaben T-1808-cmo, Eltern T-1795-ceo). Schritt 1 (Ticket T-1812-methodik_manager) legt
die Regel fest und rechnet sie an den 11 Blöcken nach, die heute `kennzeichnung: berechnet` tragen. Schritt 2 schreibt
die Übernahmeliste an den CTO und die Befunde an die Berichte. Anlass ist Befund 224 im Ledger #95: Die
Parameterliste zeigt heat.c_kal als „berechnet aus anderen Parametern“, und das Produkt zählt das wie „belegt“,
obwohl in c_kal zwei Abschätzungen von KAP3 stecken (Bericht 95, Kap. 7, Absatz „Kennzeichnung `berechnet`“).

Begriffe: **Block** = Parameter-Block in Kapitel 7 eines Berichts (Aufgabe §4, „Parameter-Block-Format“).
**Eingang** = ein Eintrag im Feld `abgeleitet_aus` eines Blocks. **Parameter-ID** = Eingang, der selbst ein Block
desselben Berichts ist. **Quellenschlüssel** = Eingang ohne eigenen Block, etwa `zfkd_kid2025`; er steht im Feld
`quelle:` eines Blocks. **Setzung** = eine Zahl oder Wahl, die KAP3 trifft und die so in keiner Quelle steht; ob ein
Block eine enthält, prüft der Bericht nach dem Prüfstein in #95 Log 40 (Proxy für eine andere Größe, Punkt statt
Bandmittel).

## Festlegung

**Regel K (Kennzeichnung eines Parameters).** Für jeden Block beantwortet die Parameterliste drei Fragen in dieser
Reihenfolge. Die erste Antwort „ja“ entscheidet.

1. **Steckt im Wert des Blocks selbst eine Setzung von KAP3?** Ja: Kennzeichnung `abschaetzung_kap3`, Anzeigetext
   „Abschätzung von KAP3“. Das gilt auch, wenn der Block zusätzlich andere Blöcke nutzt.
2. **Nennt `abgeleitet_aus` keine Parameter-ID?** Ja: Kennzeichnung `quelle`, Anzeigetext „Quelle“. Das umfasst den
   Wert, der so in der Quelle steht, und die Rechnung aus Zahlen einer Quelle ohne Setzung (Quotient, Summe,
   ausgezähltes Quantil, eigene Auswertung amtlicher Rohdaten).
3. **Sonst** (mindestens eine Parameter-ID): Kennzeichnung `berechnet`. Der Anzeigetext richtet sich nach dem
   schwächsten Eingang über alle Rechenstufen:
   - trägt kein Eingang, auch nicht über einen berechneten Eingang hinweg, eine Abschätzung von KAP3:
     „berechnet aus Quellen“;
   - trägt mindestens ein Eingang eine Abschätzung von KAP3, direkt oder weitergereicht: „berechnet, enthält
     Abschätzung von KAP3“.

Die Parameterliste zeigt neben einem berechneten Parameter seine Eingänge mit deren Anzeigetext, damit der Leser
die Herleitung bis zur Quelle oder zur Abschätzung verfolgen kann. **Gezählt** wird so: „Quelle“ und „berechnet aus
Quellen“ zählen als belegt, „Abschätzung von KAP3“ und „berechnet, enthält Abschätzung von KAP3“ als abgeschätzt.
Die drei Werte aus Aufgabe §4 und das Feld `abgeleitet_aus` bleiben, wie sie sind; die Verbindung steht nur im
Anzeigetext. Das Feld `rolle` (etwa `kalibrierung`) ändert an der Kennzeichnung nichts.

**Prüfstein (P1).** Die Parameterliste zeigt eine Setzung von KAP3 nie als Quelle, auch dann nicht, wenn sie über
eine Rechnung weitergereicht wird. Regel K hält das in zwei Schritten ein: Frage 1 hält jede Setzung im Block selbst
aus `quelle` und aus „berechnet aus Quellen“ heraus, Frage 3 reicht jede Setzung eines Eingangs über alle Stufen bis
zum Anzeigetext durch.

### (a) Grenze zwischen `quelle` und `berechnet`

`berechnet` ist ein Block genau dann, wenn `abgeleitet_aus` mindestens eine Parameter-ID nennt. Eine Rechnung, die
nur Zahlen einer Quelle verarbeitet, ist `quelle`, auch wenn KAP3 sie selbst ausführt. Der Wortlaut von Aufgabe §4
trägt diese Grenze: „`berechnet`: der Wert folgt rechnerisch aus anderen Parametern“, und `abgeleitet_aus` nennt
„die Parameter-IDs, aus denen der Wert entsteht“. Das ist die Grenze von #95 Log 40 („`berechnet` nur, wo der Wert
aus anderen Blöcken folgt“) und #96 Log 25 (ΔS als ausgewertete amtliche Messreihe = `quelle`). #98 Log 36 zieht die
Grenze anders („schwächste Herkunft im Block“, eigene Auswertung = `berechnet`); nach Regel K gilt sie nicht mehr.

- **uv.ssd_delta_region** (eigene Auswertung DWD-Raster × VG250 × Zensus 2022): einziger Eingang ist der
  Quellenschlüssel `dwd_cdc_ssd_raster_x_vg250_x_zensus2022`, keine Parameter-ID, keine Setzung laut Bericht. Nach
  Regel K `quelle`, Anzeigetext „Quelle“.
- **uv.lambda** (Sterbefälle ÷ Neuerkrankungen im Fenster 2021–2023 aus ZfKD [27]): einziger Eingang ist
  `zfkd_kid2025`. Nach Regel K `quelle`, Anzeigetext „Quelle“, wie der Quotient amtlicher Summen in #95
  (heat.m_basissterberate).
- **Folge außerhalb der 11 Blöcke:** heat.beta_iso steht in #95 als `quelle`, nennt in `abgeleitet_aus` aber den Block
  heat.qbar_1p. Nach Regel K ist er `berechnet`, Anzeigetext „berechnet aus Quellen“; er zählt weiter als belegt.

### (b) Eingang ohne eigenen Block (Quellenschlüssel in `abgeleitet_aus`)

Ein Quellenschlüssel zählt als Eingang mit der Kennzeichnung `quelle`. Allein macht er einen Block nicht zu
`berechnet`, denn dafür verlangt §4 eine Parameter-ID. Steht er neben einer Parameter-ID, zählt er bei Frage 3 als
`quelle`. Bedingung: Der Schlüssel steht im Feld `quelle:` eines Blocks desselben Berichts, und hinter ihm stehen nur
Zahlen der Quelle. Eine Zahl, die KAP3 setzt, braucht einen eigenen Block, weil P1 jeden Parameter in der Liste
verlangt; hinter einem Schlüssel darf sie nicht stehen. Ob ein Schlüssel später einen eigenen Block bekommt (#98,
Befund 463), ändert das Ergebnis nicht, solange dieser Block eine reine Auswertung der Quelle ist.

### (c) Kalibrierskalar, gefittet gegen eine amtliche Reihe

Ein Kalibrierskalar ist ein berechneter Block wie jeder andere. Seine Eingänge sind die Blöcke des Modells, das er an
die Reihe anpasst, und die Reihe selbst. Die Reihe zählt als `quelle`, gleich ob sie in `abgeleitet_aus` oder nur im
Feld `quelle:` steht; sie kann den schwächsten Eingang nicht anheben. Grund: Der Fit gleicht genau das aus, was die
Setzungen im Modell verschieben. Ändert sich eine Setzung, ändert sich der Skalar. Belegt ist nach dem Fit die Summe
aus Modell und Skalar, die an die Reihe angepasst ist, nicht der Skalar.

- **heat.c_kal** = 0,581, Fit gegen die RKI-Reihe 2012–2024 (`rki_eb19_2025`). Eingänge: heat.t0_region,
  heat.m_basissterberate und heat.q_wochenquantile (`quelle`), heat.beta_85plus_region (Süd-Nachschätzung) und
  heat.f_alter (lineare Näherung), beide `abschaetzung_kap3`. Nach Regel K `berechnet`, Anzeigetext „berechnet,
  enthält Abschätzung von KAP3“. Dass die Setzung im Wert steckt, zeigt das Band des Blocks: Mit s_Süd = 1,85 statt
  1,65 ergibt der Fit 0,559, ohne die Region Süd 0,661.
- **uv.c_kal** = ZfKD-Anker ÷ Modellsumme der Rohraten. Eingänge: uv.i_raten_roh (`quelle`) und `zfkd_kid2025`
  (Quellenschlüssel). Nach Regel K `berechnet`, Anzeigetext „berechnet aus Quellen“.

Regel K wertet `abgeleitet_aus` so aus, wie der Bericht es führt. Ob die Liste vollständig ist, prüft der Bericht
(Aufgabe §4: Pflichtfeld bei `berechnet`).

### (d) Zählung als belegt in Gewissheitsstufe und Unsicherheits-Zusammenschau

**Ja, Regel K ändert, was als belegt zählt.** Ein berechneter Block zählt nur dann als belegt, wenn kein Eingang über
alle Stufen eine Abschätzung von KAP3 trägt. Heute zählt das Produkt jeden berechneten Parameter als belegt:
`BELEGTE_KLASSEN = frozenset({"belegt", "berechnet"})` (`backend/app/services/parameter_registry.py`, Z. 102), genutzt
in `gewissheit.py` (Z. 86) und `unsicherheits_zusammenschau.py` (Z. 99), festgeschrieben in
`backend/tests/test_evidence_class_berechnet.py`, Teil (c). **Begründung:** Die Zählung „x von y Parametern mit
Quelle“ ist dieselbe Aussage wie die Parameterliste, nur verdichtet. Zählte heat.c_kal dort als belegt, zeigte die
Zählung eine Setzung als Quelle, gegen den Prüfstein. Wie viel sich verschiebt, zeigt die Zählung über die Blöcke in
Kapitel 7 (nachgerechnet im Beispiel-Block):

| Bericht | Blöcke | belegt bisher | belegt nach Regel K |
|---|---|---|---|
| 95 | 30 | 13 | 12 |
| 96 | 14 | 5 | 3 |
| 98 | 22 | 11 | 11 |

Bei #95 fällt heat.c_kal heraus, bei #96 fallen pollen.d_saison und pollen.c_tag heraus. Bei #98 wechseln drei Blöcke
von `berechnet` nach `quelle`, die Zahl der belegten Blöcke bleibt gleich. **Die Gewissheit nach Regel G ändert sich
nicht:** Sie übernimmt die Stufe der KWRA (TB6 Tabelle 1) und nimmt die Quellenlage nicht auf
([querschnitt_gewissheit.md](querschnitt_gewissheit.md), „Festlegung“). Solange der Code die Stufe noch aus dem
Anteil der belegten Parameter bildet (`gewissheit.py`, `gewissheitsstufe`), verschiebt Regel K auch diese Stufe, und
die Unsicherheits-Zusammenschau führt c_kal, d_saison und c_tag als nicht belegt. Wie der Code das umsetzt, legt
Schritt 2 fest.

### Begründung und Fundstelle

- **P1** (`CLAUDE.md` des Produkts, Abschnitt „Vorgaben des Aufsichtsrats für das Produkt“, Spiegelstrich P1): „Je
  Parameter steht dort entweder die Quelle oder der Vermerk, dass es eine begründete Abschätzung von KAP3 ist, samt
  Herleitung, wie sie zustande kommt.“ P1 kennt zwei Aussagen, Quelle oder Abschätzung, und verlangt die Herleitung.
  Regel K gibt jedem berechneten Parameter eine der beiden Aussagen („aus Quellen“ oder „enthält Abschätzung von
  KAP3“) und behält mit „berechnet“ die Herleitung.
- **Aufgabe §4** (`docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md`, „Felder `kennzeichnung`, `abgeleitet_aus`, `rolle`“):
  „`kennzeichnung` (Pflicht) hat genau drei Werte: `quelle | abschaetzung_kap3 | berechnet`. `quelle`: der Wert steht
  in einer benannten Quelle. `abschaetzung_kap3`: begründete Abschätzung von KAP3 mit Herleitung (P1). `berechnet`:
  der Wert folgt rechnerisch aus anderen Parametern.“ und „`abgeleitet_aus` nennt bei `berechnet` die Parameter-IDs,
  aus denen der Wert entsteht; sonst leer.“ Regel K behält die drei Werte und zieht die Grenze dort, wo §4 sie
  zieht: an den anderen Parametern.

**Was Regel K nicht entscheidet.** Ob im Block selbst eine Setzung steckt (Frage 1), urteilt der Bericht nach §4 und
dem Prüfstein von #95 Log 40; Regel K übernimmt dieses Urteil aus der Kennzeichnung des Berichts. Für uv.lambda
(Perioden-Näherung) und uv.l_rest (Restlebenserwartung am medianen Sterbealter) führt #98 die Näherung als
Modellgrenze (GP-Befund 43), nicht als Setzung; ob das dem Prüfstein standhält, gehört zu den Befunden an Berichte in
Schritt 2.

## Anwendung auf M0: die 11 berechneten Blöcke

Alle 11 Blöcke tragen im Bericht heute `kennzeichnung: berechnet`. Eingänge in der Reihenfolge von `abgeleitet_aus`,
ihre Kennzeichnung nach Regel K in derselben Reihenfolge; „kein Block“ heißt Quellenschlüssel (Festlegung, b).

| Bericht | Block-ID | Eingänge | deren Kennzeichnung | Kennzeichnung nach der Regel | Anzeigetext |
|---|---|---|---|---|---|
| 95 | `heat.c_kal` | `heat.t0_region` · `heat.beta_85plus_region` · `heat.f_alter` · `heat.m_basissterberate` · `heat.q_wochenquantile` | `quelle` · `abschaetzung_kap3` · `abschaetzung_kap3` · `quelle` · `quelle` | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ |
| 95 | `heat.beta_pfl` | `heat.m_basissterberate` · `heat.qbar_pfl` | `quelle` · `quelle` | `berechnet` | „berechnet aus Quellen“ |
| 95 | `heat.h_heim` | `heat.qbar_pfl` · `heat.beta_pfl` | `quelle` · `berechnet` (aus Quellen) | `berechnet` | „berechnet aus Quellen“ |
| 96 | `pollen.d_saison` | `pollen.f_symptomtage` · `pollen.p_sens_gruppen` · `pollen.l_saison` | `abschaetzung_kap3` · `abschaetzung_kap3` · `abschaetzung_kap3` | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ |
| 96 | `pollen.c_tag` | `pollen.c_jahr_direkt` · `pollen.d_saison` | `quelle` · `berechnet` (enthält Abschätzung von KAP3) | `berechnet` | „berechnet, enthält Abschätzung von KAP3“ |
| 98 | `uv.ssd_delta_region` | `dwd_cdc_ssd_raster_x_vg250_x_zensus2022` | `quelle` (kein Block) | `quelle` | „Quelle“ |
| 98 | `uv.k_uv` | `lorenz2024_dwd_ssd_trend` · `dwd_cdc_ssd_raster_x_vg250_x_zensus2022` · `uv.ssd_delta_region` | `quelle` (kein Block) · `quelle` (kein Block) · `quelle` | `berechnet` | „berechnet aus Quellen“ |
| 98 | `uv.baf` | `uv.w_scc` · `slaper1996_rivm2023_madronich2021` | `quelle` · `quelle` (kein Block) | `berechnet` | „berechnet aus Quellen“ |
| 98 | `uv.lambda` | `zfkd_kid2025` | `quelle` (kein Block) | `quelle` | „Quelle“ |
| 98 | `uv.l_rest` | `zfkd_kid2025_sterbetafel2224` | `quelle` (kein Block) | `quelle` | „Quelle“ |
| 98 | `uv.c_kal` | `uv.i_raten_roh` · `zfkd_kid2025` | `quelle` · `quelle` (kein Block) | `berechnet` | „berechnet aus Quellen“ |

Zur Zielreihe von heat.c_kal: `rki_eb19_2025` steht im Feld `quelle:`, nicht in `abgeleitet_aus`. Sie zählt nach
Festlegung (c) als `quelle` und ändert das Ergebnis nicht.

### Beispiel-Block

`regel_k`, aus dem Stamm des Produkt-Repos ausführbar (am 06.10.2026 gelaufen, Ausgabe darunter). Er liest die Blöcke
aus Kapitel 7 der drei Berichte und die Tabellen dieser Datei; abgeschrieben wird nichts.

```python
# regel_k — Regel K an allen Kapitel-7-Blöcken von #95, #96 und #98, gegen die Tabellen dieser Datei
import re

BERICHTE = {"95": "95_hitzebelastung", "96": "96_aeroallergene", "98": "98_uv_schaedigungen"}
ANZEIGE = {"quelle": "Quelle", "abschaetzung_kap3": "Abschätzung von KAP3",
           "aus_quellen": "berechnet aus Quellen", "mit_abschaetzung": "berechnet, enthält Abschätzung von KAP3"}
ZUSATZ = {"aus_quellen": "aus Quellen", "mit_abschaetzung": "enthält Abschätzung von KAP3"}


def feld(block, name):
    """Wert eines Feldes ohne Kommentar, etwa 'kennzeichnung' → 'berechnet'."""
    m = re.search(r"^\s+" + name + r": ([^#\n]*)", block, re.M)
    return m.group(1).strip() if m else ""


def bloecke(datei):
    """Kapitel-7-Blöcke eines Berichts, geschnitten wie im Prüfausdruck: id → Blocktext."""
    text = open(f"docs/methodik/{datei}.md", encoding="utf-8").read()
    teile = [b.split(chr(96) * 3)[0] for b in re.split(r"\nparameter:", text)[1:]]
    return {re.search(r"id: (\S+)", b).group(1): b for b in teile}


B = {nr: bloecke(d) for nr, d in BERICHTE.items()}
KZ = {nr: {i: feld(b, "kennzeichnung") for i, b in B[nr].items()} for nr in B}
AUS = {nr: {i: [e.strip() for e in feld(b, "abgeleitet_aus").strip("[]").split(",") if e.strip()]
            for i, b in B[nr].items()} for nr in B}
QUELLEN = {nr: {feld(b, "quelle").split()[0] for b in B[nr].values() if feld(b, "quelle")} for nr in B}


def regel_k(nr, i):
    """Regel K für Block i in Bericht nr → (Kennzeichnung nach der Regel, Anzeigeklasse)."""
    if KZ[nr][i] == "abschaetzung_kap3":          # Frage 1: Setzung im Block selbst (Urteil des Berichts)
        return "abschaetzung_kap3", "abschaetzung_kap3"
    for e in AUS[nr][i]:                            # (b) Eingang ohne Block: Quellenschlüssel aus einem Feld quelle:
        assert e in B[nr] or ("." not in e and e in QUELLEN[nr]), (i, e)
    ids = [e for e in AUS[nr][i] if e in B[nr]]     # Parameter-IDs
    if not ids:                                     # Frage 2: keine Parameter-ID → quelle
        return "quelle", "quelle"
    schwach = any(regel_k(nr, e)[1] in ("abschaetzung_kap3", "mit_abschaetzung") for e in ids)  # Frage 3
    return "berechnet", "mit_abschaetzung" if schwach else "aus_quellen"


def eingang_text(nr, e):
    """Kennzeichnung eines Eingangs, wie die Spalte „deren Kennzeichnung“ sie schreibt."""
    if e not in B[nr]:
        return "quelle (kein Block)"
    kz, kl = regel_k(nr, e)
    return f"berechnet ({ZUSATZ[kl]})" if kz == "berechnet" else kz


# Die 11 Blöcke, die heute berechnet tragen (dieselbe Auswahl wie der Prüfausdruck)
ELF = [(nr, i) for nr in B for i in B[nr] if re.search(r"^\s+kennzeichnung: berechnet", B[nr][i], re.M)]
assert len(ELF) == 11

# Tabellen dieser Datei lesen: 6 Spalten = Tabelle der 11 Blöcke, 4 Spalten = Zählung belegt
q = open("docs/methodik/querschnitt_kennzeichnung.md", encoding="utf-8").read()
tab, tab_z = {}, {}
for zeile in q.splitlines():
    z = [c.strip().replace(chr(96), "") for c in zeile.strip().strip("|").split("|")]
    if z[0] in BERICHTE and len(z) == 6:
        tab[(z[0], z[1])] = z
    elif z[0] in BERICHTE and len(z) == 4:
        tab_z[z[0]] = tuple(int(x) for x in z[1:])
assert set(tab) == set(ELF), set(tab) ^ set(ELF)

for nr, i in ELF:
    kz, kl = regel_k(nr, i)
    _, _, ein, ein_kz, soll_kz, soll_text = tab[(nr, i)]
    assert ein.split(" · ") == AUS[nr][i], (i, ein)
    assert ein_kz.split(" · ") == [eingang_text(nr, e) for e in AUS[nr][i]], (i, ein_kz)
    assert (soll_kz, soll_text.strip("„“")) == (kz, ANZEIGE[kl]), (i, soll_kz, soll_text)
    print(f"#{nr} {i:<22} {kz:<10} „{ANZEIGE[kl]}“")

# heat.c_kal ausdrücklich: zwei abgeschätzte Eingänge, die Setzung bewegt den Fit (Feld band)
c = B["95"]["heat.c_kal"]
assert regel_k("95", "heat.c_kal") == ("berechnet", "mit_abschaetzung")
assert ANZEIGE[regel_k("95", "heat.c_kal")[1]] == tab[("95", "heat.c_kal")][5].strip("„“")
assert [e for e in AUS["95"]["heat.c_kal"] if KZ["95"][e] == "abschaetzung_kap3"] == \
    ["heat.beta_85plus_region", "heat.f_alter"]
assert feld(c, "wert") == "0.581" and "0,559 (s_Sued=1,85)" in c and "0,661 (ohne Sued)" in c
assert "s_Sued 1,65" in B["95"]["heat.beta_85plus_region"]
assert (feld(c, "rolle"), feld(c, "quelle")) == ("kalibrierung", "rki_eb19_2025")
assert regel_k("98", "uv.c_kal") == ("berechnet", "aus_quellen")      # (c) gleiche Regel, anderes Ergebnis

# (a) Grenze, benannt an uv.ssd_delta_region und uv.lambda; gleiche Lage wie ΔS in #96 (Log 25)
assert regel_k("98", "uv.ssd_delta_region") == regel_k("98", "uv.lambda") == ("quelle", "quelle")
assert KZ["96"]["pollen.delta_s_region"] == "quelle" and not AUS["96"]["pollen.delta_s_region"]

# Wo Regel K von der Kennzeichnung im Bericht abweicht (alle Blöcke, nicht nur die 11)
wechsel = sorted(i for nr in B for i in B[nr] if regel_k(nr, i)[0] != KZ[nr][i])
assert wechsel == ["heat.beta_iso", "uv.l_rest", "uv.lambda", "uv.ssd_delta_region"], wechsel
print("Kennzeichnung weicht vom Bericht ab:", wechsel)

# (d) Zählung belegt: bisher quelle + berechnet, nach Regel K „Quelle“ + „berechnet aus Quellen“
zaehl = {nr: (len(B[nr]), sum(KZ[nr][i] in ("quelle", "berechnet") for i in B[nr]),
              sum(regel_k(nr, i)[1] in ("quelle", "aus_quellen") for i in B[nr])) for nr in B}
assert zaehl == tab_z, (zaehl, tab_z)
print("Blöcke, belegt bisher, belegt nach Regel K:", zaehl)
```

Ausgabe:

```
#95 heat.c_kal             berechnet  „berechnet, enthält Abschätzung von KAP3“
#95 heat.beta_pfl          berechnet  „berechnet aus Quellen“
#95 heat.h_heim            berechnet  „berechnet aus Quellen“
#96 pollen.d_saison        berechnet  „berechnet, enthält Abschätzung von KAP3“
#96 pollen.c_tag           berechnet  „berechnet, enthält Abschätzung von KAP3“
#98 uv.ssd_delta_region    quelle     „Quelle“
#98 uv.k_uv                berechnet  „berechnet aus Quellen“
#98 uv.baf                 berechnet  „berechnet aus Quellen“
#98 uv.lambda              quelle     „Quelle“
#98 uv.l_rest              quelle     „Quelle“
#98 uv.c_kal               berechnet  „berechnet aus Quellen“
Kennzeichnung weicht vom Bericht ab: ['heat.beta_iso', 'uv.l_rest', 'uv.lambda', 'uv.ssd_delta_region']
Blöcke, belegt bisher, belegt nach Regel K: {'95': (30, 13, 12), '96': (14, 5, 3), '98': (22, 11, 11)}
```

## Rechenkette

Format nach Aufgabe §4, hier „Eingänge → Kennzeichnung“ statt „Zahl × Faktor“, weil Regel K einordnet und nicht
rechnet. Am Ende steht kein Euro-Betrag, sondern der Anzeigetext in der Parameterliste. Beispiel: heat.c_kal aus
Bericht 95, der Kalibrierskalar der Sterbefälle durch Hitze.

| Ebene | Block | Eingänge | Kennzeichnung der Eingänge | Kennzeichnung nach der Regel | Anzeigetext |
|---|---|---|---|---|---|
| 1 | heat.t0_region: Temperatur, ab der die Sterblichkeit steigt, je Region | keine; Ablesewerte Winklmayr 2022, Abb. 3 | – | `quelle` (Frage 2) | „Quelle“ |
| 2 | heat.beta_85plus_region: Anstieg der Sterblichkeit je Grad, ab 85 Jahren | keine; Nord und Mitte abgelesen, Süd von KAP3 nachgeschätzt (s_Süd = 1,65) | – | `abschaetzung_kap3` (Frage 1) | „Abschätzung von KAP3“ |
| 3 | heat.f_alter: Faktor je Altersband | keine; aus RKI-Anteilen zurückgerechnet mit linearer Näherung von KAP3 | – | `abschaetzung_kap3` (Frage 1) | „Abschätzung von KAP3“ |
| 4 | heat.m_basissterberate: Sterbefälle 2023 ÷ Bevölkerung, je Altersband | keine; Quotient amtlicher Summen | – | `quelle` (Frage 2) | „Quelle“ |
| 5 | heat.q_wochenquantile: Temperaturquantile je Woche | keine; aus DWD-Tageswerten ausgezählt | – | `quelle` (Frage 2) | „Quelle“ |
| 6 | Zielreihe `rki_eb19_2025`: hitzebedingte Sterbefälle des RKI 2012–2024 | Quellenschlüssel im Feld `quelle:` | – | zählt als `quelle` (Festlegung, c) | – |
| 7 | heat.c_kal = 0,581: Fit des Modells aus Ebene 1–5 an die Reihe aus Ebene 6 | Ebene 1–5 (Parameter-IDs) und Ebene 6 | `quelle` · `abschaetzung_kap3` · `abschaetzung_kap3` · `quelle` · `quelle`; Reihe `quelle` | Frage 1: keine eigene Setzung, Frage 2: fünf Parameter-IDs, also `berechnet` (Frage 3) | schwächster Eingang Ebene 2 und 3: „berechnet, enthält Abschätzung von KAP3“ |
| 8 | Gegenprobe am Band von heat.c_kal | s_Süd aus Ebene 2 geändert | – | Fit 0,559 bei s_Süd = 1,85, 0,661 ohne Region Süd, statt 0,581 | Die Setzung steckt im Wert. |
| 9 | Zählung in der Quellenlage von #95 | 30 Blöcke in Kap. 7 | – | heat.c_kal zählt als abgeschätzt | belegt 12 statt 13 von 30 |

**Nacherzählt.** c_kal ist die Zahl, mit der KAP3 das Hitzemodell so einstellt, dass es die Sterbefälle des RKI der
Jahre 2012–2024 trifft. Das Modell besteht aus fünf Bausteinen. Drei stammen aus Quellen. Zwei hat KAP3 selbst
abgeschätzt: den Anstieg der Sterblichkeit im Süden und den Faktor je Altersband. Weil c_kal genau das ausgleicht, was
diese beiden Bausteine verschieben, steckt ihre Abschätzung in c_kal. Ändert man die Abschätzung im Süden, wird aus
0,581 eine 0,559. Deshalb zeigt die Parameterliste „berechnet, enthält Abschätzung von KAP3“ und zählt c_kal nicht als
belegt. Den Ausschlag geben Ebene 2 und 3; ein einziger abgeschätzter Eingang hätte genügt.

**Über zwei Rechenstufen: pollen.c_tag (Bericht 96).** pollen.d_saison = 0,70 × (0,55 × 30 + 0,75 × 60) = 43,05 Tage
folgt aus drei Abschätzungen von KAP3 und zeigt „berechnet, enthält Abschätzung von KAP3“. pollen.c_tag = 266,90 €
÷ 43,05 Tage = 6,20 € je Tag (Preisstand 2024) folgt aus c_jahr (`quelle`) und d_saison. c_tag selbst hat keinen
abgeschätzten Eingang, erbt die Abschätzung aber über d_saison und zeigt ebenfalls „berechnet, enthält Abschätzung von
KAP3“. So wird eine Setzung auch über eine Rechnung weitergereicht nie als Quelle gezeigt.

**Was die einfachere Regel verfälschen würde (§8 E3).** Liest man `berechnet` wie heute als belegt, zählen heat.c_kal,
pollen.d_saison und pollen.c_tag als belegt: #95 käme auf 13 statt 12 belegte Blöcke von 30, #96 auf 5 statt 3 von
14, und die Liste zeigte drei Setzungen als belegt. Schreibt man stattdessen schlicht „Abschätzung von KAP3“, verliert
die Anzeige, dass c_kal ein Fit an die RKI-Reihe ist und drei seiner fünf Eingänge aus Quellen stammen.

## Entscheidungslog

**Gewählt:** Ansatz B, die Vererbung der schwächsten Kennzeichnung über alle Stufen, angezeigt als Verbindung, mit
der Grenze zwischen `quelle` und `berechnet` aus Aufgabe §4. Verworfen, je in einem Satz:

- **Ansatz A** (`berechnet` als neutrale Klasse wie heute, gelesen wie belegt): Er zeigt heat.c_kal, pollen.d_saison
  und pollen.c_tag als belegt, obwohl in ihnen Setzungen von KAP3 stecken, und verletzt damit den Prüfstein aus P1.
- **Ansatz C** (ein berechneter Wert mit abgeschätztem Eingang heißt schlicht `abschaetzung_kap3`): Er hält den
  Prüfstein ein, verliert in der Anzeige aber, dass der Wert aus anderen Parametern folgt und welche davon belegt
  sind, also die Herleitung, die P1 verlangt.
- **Ansatz D** (Urteil je Block ohne feste Regel): Er ist genau das, was #95 Log 40 und #98 Log 36 auseinanderlaufen
  ließ, und ließe sich weder im Beispiel-Block noch im Code nachrechnen.
- **Grenze nach #98 Log 36** (jede eigene Auswertung amtlicher Daten ist `berechnet`): Sie widerspricht Aufgabe §4,
  wonach `berechnet` aus anderen Parametern folgt, und machte jede Sterberate und jedes ausgezählte Quantil zu
  `berechnet`, ohne dass der Leser etwas über Setzungen erfährt.
- **Ausnahme für umgerechnete Studienzahlen** (heat.beta_iso bleibt `quelle`, obwohl er den Block heat.qbar_1p nutzt,
  #95 Log 40): Sie verlangt ein Urteil je Block, und heat.beta_iso zählt als „berechnet aus Quellen“ ebenso als
  belegt.
- **Kalibrierskalar als `quelle`, weil gegen eine amtliche Reihe gefittet**: Das verwechselt die an die Reihe
  angepasste Summe mit dem Skalar, der die Setzungen des Modells ausgleicht und sich mit ihnen ändert (heat.c_kal
  0,559 statt 0,581 bei s_Süd = 1,85).
- **Quellenschlüssel ohne Block wie eine Abschätzung zählen**: Das stellte Zahlen einer Quelle schlechter als einen
  Block mit denselben Zahlen und überzeichnete die Unsicherheit amtlicher Quotienten.
- **Fünfter Anzeigetext „Quelle, ausgewertet von KAP3“**: Die Auswertung steht schon in der Herleitung, die P1 je
  Parameter verlangt, und der Text zeigte gleich gerechnete Blöcke verschieden, weil etwa heat.m_basissterberate kein
  `abgeleitet_aus` führt.

**Abgrenzung zur Gewissheit.** Regel K sagt, woher der Wert eines Parameters stammt. Die Gewissheit einer
Klimawirkung legt Regel G in [querschnitt_gewissheit.md](querschnitt_gewissheit.md) fest: Sie übernimmt die Gewissheit
der Bewertung aus KWRA TB6 Tabelle 1 und rechnet sie nicht aus Parametern. Die Quellenlage der Parameter erscheint
dort nur als Zählung zum Vergleich und geht in die Gewissheit nicht ein. Regel K ändert diese Zählung (Festlegung, d),
aber keine Stufe nach Regel G. querschnitt_gewissheit.md bleibt unverändert.

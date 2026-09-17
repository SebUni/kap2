#!/usr/bin/env python3
"""
Stichprobe #60, Teil 2: Jahresschadensraten je nachgebildeter ZÜRS-Klasse aus den
acht Anker-Kommunen — Grundlage für Befund 32 (A) an #60.

Befunde des Laufs 17.09.2026 — quantifizierter Restfehler (§3.4/§3.9)
---------------------------------------------------------------------
Das Folgepaket zitiert diesen Block für den Restfehler der Klassenraten. Alle Zahlen
stammen aus dem Lauf dieses Skripts auf den Stichprobendateien; sie stehen zugleich
in m0_klassenraten.csv.

Streuung der Rate über die acht Anker-Kommunen (rate_zellen_1_pro_a, 1/a):

  Klasse    kleinster Wert            größter Wert           gewichtetes Mittel
  gk3_gk4   0,00184563 Reichertshofen 0,00798267 Grimma      0,00419732
  gk2       0,00004514 Grimma         0,00103729 Halle(Saale) 0,00043606
  gesamt    0,00077279 Rosenheim      0,00753784 Grimma      0,00230531

Der größte Kommunenwert liegt in gk3_gk4 um den Faktor 4,3 über dem kleinsten, in gk2
um den Faktor 23. Die Rate ist damit keine bundesweite Konstante, sondern ein
Stichprobenmittel mit kommunaler Streuung dieser Größenordnung — das ist die
Hauptkomponente des Restfehlers unterhalb der Stichprobenauflösung.

Gewichtetes Mittel am zweiten Nenner (rate_exponiert_hqextrem_1_pro_a, 1/a):
gk3_gk4 0,00597960; gk2 0,00067515; gesamt 0,00342169.

Kartenzellen ohne Zensuszeile (W_z = 0, tragen nichts zum Schaden bei, stehen aber in
der Zellzahl): gk3_gk4 10.589 von 13.414 (78,9 %); gk2 2.539 von 4.523 (56,1 %);
gesamt 13.128 von 17.937 (73,2 %). Das sind unbewohnte Zellen oder solche, die im
Zensus-Paket geheim gehalten sind. Folge für die Lesart der Spalten: `zellen` zählt
alle Zellen der Klasse einschließlich dieser; `anteil_fallback_zensus` ist deshalb
hoch (gk3_gk4 79,5 %, gk2 57,0 %, gesamt 73,8 %), weil eine fehlende Zensuszeile keine
Angabe 'zensus' trägt. Nur unter den Zellen MIT Zensuszeile liegt der Ersatzwertanteil
bei gk3_gk4 2,6 % (74 von 2.825), gk2 1,9 % (37 von 1.984), gesamt 2,3 % (111 von
4.809). Das Folgepaket muss angeben, welche der beiden Lesarten es zitiert. Zellen mit
a = 0 in allen drei Szenarien kamen nicht vor (0 Zellen verworfen): die Kartendateien
führen nur überflutete Zellen.

Bekannter Sonderfall Deggendorf HQ100: 88,5 % Ersatztiefen (fallback_kommune) laut
Skriptkopf von stichprobe60_kernformel.py; über alle Szenarien betrachtet tragen
88,5 % der gk3_gk4-Zellen Deggendorfs eine Ersatztiefe. Deggendorfs HQ100-Schaden ist
damit überwiegend Abschätzung, nicht Kartentiefe. Rate ohne Deggendorf:

  Klasse    mit Deggendorf   ohne Deggendorf   Deggendorf allein
  gk3_gk4   0,00419732       0,00436548        0,00254537
  gk2       0,00043606       0,00044404        0,00016142
  gesamt    0,00230531       0,00232598        0,00198213

Deggendorf zieht das gewichtete Mittel in gk3_gk4 um 3,9 % nach unten (0,0041973 statt
0,0043655). Der Ersatztiefen-Sonderfall verschiebt die Klassenrate also um wenige
Prozent, nicht um Größenordnungen; er ist als ausgewiesene Unsicherheit zu führen, nicht
als Ausschlussgrund.

Ersatztiefen insgesamt (Anteil der Zellen mit mindestens einem h_herkunft ≠ 'karte'):
gk3_gk4 17,7 %, gk2 1,6 %, gesamt 13,7 % — überwiegend aus Deggendorf und Passau.

Gegenprobe: Die Summe der zellweisen Jahreswerte trifft für alle acht Kommunen den
Wert aus ergebnis_kernformel.csv (Schranke 1e-7 relativ); das Skript bricht sonst ab.

Abweichung von der Vorabmessung des Planers: Die Raten und Wohnflächensummen stimmen
(gk3_gk4 Σ W 6,198 Mio m², Rate 0,0042/a; gk2 Σ W 6,274 Mio m², Rate 0,00044/a). Die
Zellzahlen der Vorabmessung (2.825 / 1.984) sind die Zellen MIT Zensuszeile; die Spalte
`zellen` führt hier alle Zellen der Klasse (13.414 / 4.523), weil Zellen ohne
Zensuszeile laut Ticket mit W_z = 0 zur Klasse gehören. 13.414 − 10.589 = 2.825 und
4.523 − 2.539 = 1.984 — beide Zählweisen gehen exakt ineinander über.

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2–§3.4)
------------------------------------------------------------------------------
Ticket T-0309 (Ersatz für T-0290, Teil 1 von 2). Dieses Skript schließt keinen Befund:
Bericht, Befund-Ledger, Evidenz-Register und lint_methodik.py werden weder geschrieben
noch gelesen. Es liefert nur die Zahlen, mit denen das Folgepaket Befund 32 schließt.
Die Rechenlogik ist unverändert die von stichprobe60_kernformel.py (§3.3/§3.4); sie wird
hier nicht neu erfunden, sondern nur zellweise statt kommunenweise aufsummiert. Weil
Schritt 2 linear in A ist, ist die Summe der Zell-Erwartungswerte identisch mit dem
Kommunenwert aus ergebnis_kernformel.csv — das ist die Gegenprobe (§3.6).

Ressourcen-Regel §3.4: kein neuer Abruf, kein Vollraster-Lauf. Gerechnet wird
ausschließlich auf den Zellen der bereits vorliegenden Stichprobendateien.

Eingaben (nur gelesen)
----------------------
  docs/evidenz/60_stichprobe/zensus_wohnflaeche.csv   W_z je Zelle (Spalte
      wohnflaeche_m2), Kennzeichen Ersatzwert (Spalte herkunft), Verbindungsschlüssel
      gitter_id, Kommune (Spalte kommune)
  docs/evidenz/60_stichprobe/hq_sachsen.csv           Grimma, Dresden
  docs/evidenz/60_stichprobe/hq_bayern.csv            Deggendorf, Passau, Rosenheim,
                                                      Reichertshofen
  docs/evidenz/60_stichprobe/hq_sachsen_anhalt.csv    Halle (Saale)
  docs/evidenz/60_stichprobe/hq_niedersachsen.csv     Hitzacker
      je Zelle und Szenario: a_anteil (überfluteter Flächenanteil), h_m (Wassertiefe),
      h_herkunft ('karte' oder 'fallback_*')
  docs/evidenz/60_stichprobe/ergebnis_kernformel.csv  nur für die Gegenprobe
      (Spalte jahresschaden_m2a je Kommune)

Ausgabe
-------
  docs/evidenz/60_stichprobe/m0_klassenraten.csv (UTF-8, Trennzeichen ';',
  Dezimalpunkt), 3 Klassen × 9 Kommunenzeilen = 27 Zeilen, auch wo sie null tragen.

Herleitung je Ausgabespalte (Vorgabe P1 — Quelle oder ausgewiesene Abschätzung)
------------------------------------------------------------------------------
klasse      Nachgebildete ZÜRS-Klasse, siehe Abschnitt „Klasseneinteilung“ unten.
            Ausgewiesene Zuordnung von KAP3 aus hq_*.csv (Spalte a_anteil), KEINE
            amtliche Zonierung.
kommune     Spalte kommune aus hq_*.csv; zusätzlich die Sammelzeile 'alle'
            (Summe über die acht Anker-Kommunen).
zellen      Zahl der Gitterzellen der Klasse. Quelle: gitter_id aus hq_*.csv, je Zelle
            einmal gezählt (nicht je Szenariozeile).
wohnflaeche_zellen_m2
            Σ W_z über alle Zellen der Klasse. Quelle: wohnflaeche_m2 aus
            zensus_wohnflaeche.csv, verbunden über gitter_id. Eine Kartenzelle ohne
            Zensuszeile trägt W_z = 0 (unbewohnt oder im Zensus geheim gehalten).
            Dies ist der Nenner des Beispielblocks im Bericht, der 6,311 m²/a auf die
            gesamte Zellwohnfläche 1.200 m² bezieht.
wohnflaeche_exponiert_hq100_m2
            Σ W_z·a_{z,HQ100}. Quellen: wohnflaeche_m2 (Zensus) × a_anteil (hq_*.csv,
            Szenario HQ100).
wohnflaeche_exponiert_hqextrem_m2
            Σ W_z·a_{z,HQextrem}, analog mit Szenario HQextrem. Zweiter, engerer
            Nenner für die Sensitivität; welcher der beiden zu 339.000 Adressen ×
            208 m² passt, begründet das Folgepaket, deshalb werden beide geliefert.
jahresschaden_m2a
            Σ über die Zellen der Klasse von Ā_z = Trapezregel über die drei Szenarien
            plus p3·A3, mit A_{z,s} = W_z·a_{z,s}·d(h_{z,s})·f_S093·f_S094,
            d(h) = 0,035·(0,250/0,035)^((min(max(h;0,10);1,75)−0,10)/1,65),
            f_S093 = f_S094 = 1,00 (geparkt, §3.2) und
            p = 0,1 / 0,01 / sqrt(5e-3·1e-3). Quellen: a_anteil und h_m aus hq_*.csv,
            wohnflaeche_m2 aus zensus_wohnflaeche.csv; Formeln §3.3/§3.4 des Berichts,
            identisch mit stichprobe60_kernformel.py.
rate_zellen_1_pro_a
            jahresschaden_m2a ÷ wohnflaeche_zellen_m2 (0, wenn der Nenner 0 ist).
            Abgeleitete Größe, keine eigene Quelle.
rate_exponiert_hqextrem_1_pro_a
            jahresschaden_m2a ÷ wohnflaeche_exponiert_hqextrem_m2 (0 bei Nenner 0).
            Abgeleitete Größe, keine eigene Quelle.
anteil_fallback_tiefe
            Anteil der Zellen der Klasse (Zellzahl, nicht Fläche), bei denen in
            mindestens einem Szenario h_herkunft nicht 'karte' ist. Quelle:
            h_herkunft aus hq_*.csv. Maß dafür, wie weit die Rate auf Ersatztiefen
            statt auf Kartentiefen ruht.
anteil_fallback_zensus
            Anteil der Zellen der Klasse (Zellzahl), deren Zensuszeile in der Spalte
            herkunft nicht 'zensus' trägt. Quelle: herkunft aus
            zensus_wohnflaeche.csv. Eine Kartenzelle ohne Zensuszeile trägt keine
            Angabe 'zensus' und zählt deshalb hier mit; ihre Zahl steht oben im
            Befundblock gesondert, damit beide Lesarten nachvollziehbar sind.

Klasseneinteilung (ausgewiesene Zuordnung von KAP3, §3.9 „Abgeschätzt")
-----------------------------------------------------------------------
Die ZÜRS-Klassen sind über die Jährlichkeit der Überflutung definiert: GK4 häufiger
als HQ10, GK3 zwischen HQ10 und HQ100, GK2 seltener als HQ100. Hier werden sie über
dasselbe Merkmal aus den amtlichen Gefahrenkarten nachgebildet:

  gk3_gk4   Zelle mit a > 0 bei HQhäufig ODER bei HQ100
  gk2       Zelle mit a = 0 in beiden, aber a > 0 bei HQextrem
  (Zellen mit a = 0 in allen drei Szenarien fallen weg.)
  gesamt    Summe aus gk3_gk4 und gk2 (Zeile je Kommune und für 'alle')

Das ist eine ausgewiesene Zuordnung von KAP3, keine amtliche Zonierung: Die
ZÜRS-Adressdaten sind schlüsselpflichtig und werden nicht verwendet. Die Grenzen der
Nachbildung sind (a) die Kartenauflösung des jeweiligen Landes, (b) das HQhäufig der
Länder ist nicht überall exakt HQ10, (c) GK3 und GK4 werden nicht getrennt, weil das
Merkmal dafür (HQ10 gegen häufiger) in den Stichprobendateien nicht vorliegt.

Modellgrenzen
-------------
* Markierungszeilen ('keine', 'nicht_kartiert', 'nicht_ueberflutet') tragen 0 bei und
  gehen in keine Klasse ein; tritt der Fall ein, ist die 0 eine Modellgrenze der
  Kartenlage (Lackmustest §3.1), kein gemessenes Nullrisiko.
* Die Ersatztiefen (fallback_*) stammen aus den Eingabepaketen und werden hier
  ungeprüft übernommen; ihr Anteil steht in der Ausgabe und im Befundblock.
* Die acht Anker-Kommunen sind eine Stichprobe, kein Bundesdurchschnitt; die Streuung
  der Rate über die Kommunen im Befundblock ist das Maß für den Restfehler unterhalb
  der Stichprobenauflösung (§3.4/§3.9).
"""
import csv
import os
import sys

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ORDNER = os.path.join(WURZEL, 'docs', 'evidenz', '60_stichprobe')
ZENSUS = 'zensus_wohnflaeche.csv'
KARTEN = ('hq_sachsen.csv', 'hq_bayern.csv', 'hq_sachsen_anhalt.csv', 'hq_niedersachsen.csv')
GEGENPROBE = 'ergebnis_kernformel.csv'
AUSGABE = 'm0_klassenraten.csv'

KOMMUNEN = ('Grimma', 'Dresden', 'Deggendorf', 'Passau', 'Halle (Saale)', 'Hitzacker',
            'Rosenheim', 'Reichertshofen')
SZENARIEN = ('HQhäufig', 'HQ100', 'HQextrem')          # absteigend nach p sortiert
P = (1.0e-1, 1.0e-2, (5.0e-3 * 1.0e-3) ** 0.5)
MARKIERUNGEN = ('keine', 'nicht_kartiert', 'nicht_ueberflutet')
KLASSEN = ('gk3_gk4', 'gk2', 'gesamt')

D1, D5, H1, H5 = 0.035, 0.250, 0.10, 1.75
F_S093 = F_S094 = 1.00

SPALTEN = ('klasse', 'kommune', 'zellen', 'wohnflaeche_zellen_m2',
           'wohnflaeche_exponiert_hq100_m2', 'wohnflaeche_exponiert_hqextrem_m2',
           'jahresschaden_m2a', 'rate_zellen_1_pro_a', 'rate_exponiert_hqextrem_1_pro_a',
           'anteil_fallback_tiefe', 'anteil_fallback_zensus')


def d(h):
    """Schadensquote §3.3: log-linear zwischen den belegten Enden, außerhalb gedeckelt."""
    return D1 * (D5 / D1) ** ((min(max(h, H1), H5) - H1) / (H5 - H1))


def jahreswert(a):
    """Schritt 2 §3.4: Trapezregel über die Szenarien plus p3·A3."""
    return sum((P[i] - P[i + 1]) * (a[i] + a[i + 1]) / 2 for i in range(2)) + P[2] * a[2]


def selbstkontrolle():
    assert abs(d(0.405) - 0.0503) < 5e-4 and abs(d(1.75) - 0.250) < 1e-9
    assert d(4.00) == 0.250 and d(0.05) == 0.035
    w = 1200.0
    a = [w * an * ds * F_S093 * F_S094 for an, ds in ((0.25, 0.050), (0.80, 0.081), (1.00, 0.250))]
    a_bar = jahreswert(a)
    if abs(a_bar - 6.311) >= 1e-3:
        sys.exit('Selbstkontrolle fehlgeschlagen: Ā = %.6f statt 6,311 m²/a' % a_bar)
    return a_bar


def lies(name):
    with open(os.path.join(ORDNER, name), encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh, delimiter=';'))


def ist_markierung(z):
    return (z['gitter_id'].strip() in MARKIERUNGEN or z['h_herkunft'].strip() in MARKIERUNGEN
            or z['a_anteil'].strip() in MARKIERUNGEN or not z['gitter_id'].startswith('CRS'))


def zahl(x):
    return float(x.replace(',', '.'))


def leer():
    return {'zellen': 0, 'w': 0.0, 'w_hq100': 0.0, 'w_extrem': 0.0, 'j': 0.0,
            'fb_tiefe': 0, 'fb_zensus': 0, 'ohne_zensus': 0, 'fb_zensus_vorhanden': 0}


def addiere(ziel, quelle):
    for s in ziel:
        ziel[s] += quelle[s]


def main():
    print('Selbstkontrolle Zellblock: Ā = %.4f m²/a' % selbstkontrolle())

    # --- Zensus: W_z und Ersatzwert-Kennzeichen je Zelle ---------------------------
    wz, zensus_fb = {}, {}
    for z in lies(ZENSUS):
        schluessel = (z['kommune'], z['gitter_id'])
        if schluessel in wz:
            sys.exit('Zensus-Datei: doppelte Zelle %r' % (schluessel,))
        wz[schluessel] = zahl(z['wohnflaeche_m2'])
        zensus_fb[schluessel] = z['herkunft'].strip() != 'zensus'

    # --- Karten: a und h je Zelle und Szenario -------------------------------------
    zellen = {}
    for name in KARTEN:
        for z in lies(name):
            k, s = z['kommune'], z['szenario']
            if k not in KOMMUNEN or s not in SZENARIEN:
                sys.exit('%s: unbekannte Kommune/Szenario %r/%r' % (name, k, s))
            if ist_markierung(z):
                continue
            eintrag = zellen.setdefault((k, z['gitter_id']), {})
            if s in eintrag:
                sys.exit('%s: doppelte Zelle/Szenario %r/%r/%r' % (name, k, z['gitter_id'], s))
            eintrag[s] = (zahl(z['a_anteil']), zahl(z['h_m']), z['h_herkunft'].strip())

    # --- Klassenzuordnung und zellweise Rechnung -----------------------------------
    tabelle = {(c, k): leer() for c in KLASSEN for k in KOMMUNEN + ('alle',)}
    verworfen = 0
    for (k, gid), eintrag in zellen.items():
        a = [eintrag.get(s, (0.0, 0.0, 'karte'))[0] for s in SZENARIEN]
        if a[0] > 0 or a[1] > 0:
            klasse = 'gk3_gk4'
        elif a[2] > 0:
            klasse = 'gk2'
        else:
            verworfen += 1
            continue
        w = wz.get((k, gid), 0.0)
        schaden = [w * eintrag[s][0] * d(eintrag[s][1]) * F_S093 * F_S094 if s in eintrag else 0.0
                   for s in SZENARIEN]
        zelle = leer()
        zelle['zellen'] = 1
        zelle['w'] = w
        zelle['w_hq100'] = w * a[1]
        zelle['w_extrem'] = w * a[2]
        zelle['j'] = jahreswert(schaden)
        zelle['fb_tiefe'] = int(any(v[2] != 'karte' for v in eintrag.values()))
        zelle['fb_zensus'] = int(zensus_fb.get((k, gid), True))
        zelle['ohne_zensus'] = int((k, gid) not in wz)
        zelle['fb_zensus_vorhanden'] = int(zensus_fb.get((k, gid), False))
        for ziel in ((klasse, k), (klasse, 'alle'), ('gesamt', k), ('gesamt', 'alle')):
            addiere(tabelle[ziel], zelle)

    # --- Gegenprobe gegen ergebnis_kernformel.csv ----------------------------------
    soll = {z['kommune']: zahl(z['jahresschaden_m2a']) for z in lies(GEGENPROBE)}
    for k in KOMMUNEN:
        if k not in soll:
            sys.exit('Gegenprobe: Kommune %r fehlt in %s' % (k, GEGENPROBE))
        ist = tabelle[('gesamt', k)]['j']
        if abs(ist - soll[k]) > 1e-7 * max(1.0, soll[k]):
            sys.exit('Gegenprobe %s: %.6f statt %.6f m²/a' % (k, ist, soll[k]))
    print('Gegenprobe gegen %s: alle acht Kommunen getroffen.' % GEGENPROBE)

    # --- Ausgabe -------------------------------------------------------------------
    def teile(z, n):
        return z / n if n else 0.0

    zeilen = []
    for c in KLASSEN:
        for k in KOMMUNEN + ('alle',):
            t = tabelle[(c, k)]
            zeilen.append([c, k, '%d' % t['zellen'],
                           '%.6f' % t['w'], '%.6f' % t['w_hq100'], '%.6f' % t['w_extrem'],
                           '%.6f' % t['j'],
                           '%.15f' % teile(t['j'], t['w']),
                           '%.15f' % teile(t['j'], t['w_extrem']),
                           '%.15f' % teile(t['fb_tiefe'], t['zellen']),
                           '%.15f' % teile(t['fb_zensus'], t['zellen'])])
    with open(os.path.join(ORDNER, AUSGABE), 'w', encoding='utf-8', newline='') as fh:
        wr = csv.writer(fh, delimiter=';', lineterminator='\n')
        wr.writerow(list(SPALTEN))
        wr.writerows(zeilen)

    # --- Befundblock für den Skriptkopf (P1) ---------------------------------------
    print('\nZellen ohne Klasse (a = 0 in allen drei Szenarien): %d' % verworfen)
    for c in KLASSEN:
        raten = [(teile(tabelle[(c, k)]['j'], tabelle[(c, k)]['w']), k) for k in KOMMUNEN
                 if tabelle[(c, k)]['w'] > 0]
        alle = tabelle[(c, 'alle')]
        ohne_d_j = alle['j'] - tabelle[(c, 'Deggendorf')]['j']
        ohne_d_w = alle['w'] - tabelle[(c, 'Deggendorf')]['w']
        print('\n[%s] Zellen %d, Σ W = %.0f m², Ā = %.1f m²/a' % (c, alle['zellen'], alle['w'],
                                                                 alle['j']))
        print('  rate_zellen: min %.8f (%s), max %.8f (%s), gewichtetes Mittel %.8f 1/a'
              % (min(raten)[0], min(raten)[1], max(raten)[0], max(raten)[1],
                 teile(alle['j'], alle['w'])))
        print('  rate_exponiert_hqextrem (gewichtetes Mittel): %.8f 1/a'
              % teile(alle['j'], alle['w_extrem']))
        print('  Kartenzellen ohne Zensuszeile: %d von %d (%.1f %%)'
              % (alle['ohne_zensus'], alle['zellen'],
                 100 * teile(alle['ohne_zensus'], alle['zellen'])))
        print('  Ersatztiefen %.1f %% der Zellen, Ersatz-Zensus %.1f %% der Zellen'
              % (100 * teile(alle['fb_tiefe'], alle['zellen']),
                 100 * teile(alle['fb_zensus'], alle['zellen'])))
        print('  davon Ersatz-Zensus nur unter den Zellen MIT Zensuszeile: %.1f %% (%d von %d)'
              % (100 * teile(alle['fb_zensus_vorhanden'], alle['zellen'] - alle['ohne_zensus']),
                 alle['fb_zensus_vorhanden'], alle['zellen'] - alle['ohne_zensus']))
        print('  ohne Deggendorf: rate_zellen %.8f 1/a (Σ W = %.0f m², Ā = %.1f m²/a)'
              % (teile(ohne_d_j, ohne_d_w), ohne_d_w, ohne_d_j))
        print('  Deggendorf allein: rate_zellen %.8f 1/a, Ersatztiefen %.1f %% der Zellen'
              % (teile(tabelle[(c, 'Deggendorf')]['j'], tabelle[(c, 'Deggendorf')]['w']),
                 100 * teile(tabelle[(c, 'Deggendorf')]['fb_tiefe'],
                             tabelle[(c, 'Deggendorf')]['zellen'])))
    print('\ngeschrieben: %s (%d Zeilen)'
          % (os.path.relpath(os.path.join(ORDNER, AUSGABE), WURZEL), len(zeilen)))


if __name__ == '__main__':
    main()

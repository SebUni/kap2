#!/usr/bin/env python3
"""
Stichprobe #60: Kernformel §3.4 auf den acht Anker-Kommunen — exponierte Wohnfläche
und schadensäquivalente Wohnfläche je HQ-Szenario, Jahreserwartungswert je Kommune.

Modellkontext (docs/methodik/60_gebaeudeschaeden_flusshochwasser.md, §3.2–§3.4)
------------------------------------------------------------------------------
Letztes Paket des Vorhabens T-0284 (Ticket T-0305, Ersatz für T-0302) und Grundlage
für T-0290 (Befund 32). Es schließt keinen Befund. Bericht, Ledger und Evidenz-Register
werden nicht geschrieben; die Eingaben werden nur gelesen.

Eingaben (nur gelesen, kein neuer Abruf, kein Vollraster — Ressourcen-Regel §3.4)
--------------------------------------------------------------------------------
  docs/evidenz/60_stichprobe/zensus_wohnflaeche.csv   Ebene GEBAEUDEWERT (W_z, ags, land)
  docs/evidenz/60_stichprobe/hq_sachsen.csv           Ebenen HQ_FLAECHE/HQ_TIEFE (Grimma, Dresden)
  docs/evidenz/60_stichprobe/hq_bayern.csv            (Deggendorf, Passau, Rosenheim, Reichertshofen)
  docs/evidenz/60_stichprobe/hq_sachsen_anhalt.csv    (Halle (Saale))
  docs/evidenz/60_stichprobe/hq_niedersachsen.csv     (Hitzacker)

Ausgabe
-------
  docs/evidenz/60_stichprobe/ergebnis_kernformel.csv  (UTF-8, Trennzeichen ';', Dezimalpunkt)
  kommune;ags;land;szenario;w_exponiert_m2;a_schaden_m2;jahresschaden_m2a;
  quelle_hq_flaeche;quelle_hq_tiefe;quelle_gebaeudewert

Rechnung (Block beispiel_60_kernformel_zelle im Bericht ist die Referenz)
------------------------------------------------------------------------
* Verbindung Karte ↔ Zensus über gitter_id. Eine Karten-Zelle ohne Zensus-Zeile zählt
  mit W_z = 0; eine Markierungszeile ('keine', 'nicht_kartiert', 'nicht_ueberflutet')
  trägt 0 bei, liefert aber ihre URLs.
* Schadensquote d(h) = 0,035·(0,250/0,035)^((min(max(h; 0,10); 1,75) − 0,10)/1,65),
  f_S093 = f_S094 = 1,00 (geparkt, §3.2).
* Schritt 1 je Kommune k und Szenario s:
    w_exponiert_m2 = Σ_z W_z·a_{z,s}                  (exponierte Wohnfläche W)
    a_schaden_m2   = Σ_z W_z·a_{z,s}·d(h_{z,s})·f_S093·f_S094   (A_{k,s})
* Schritt 2: jahresschaden_m2a = Σ_{i=1,2} (p_i − p_{i+1})·(A_i + A_{i+1})/2 + p_3·A_3
  mit p = 0,1 / 0,01 / sqrt(5e-3·1e-3) (HQhäufig / HQ100 / HQextrem); steht auf allen
  drei Zeilen der Kommune gleich. Da Schritt 2 linear in A ist, ist das identisch mit der
  Summe der Zell-Erwartungswerte Ā_z (§3.6).
* Selbstkontrolle: Der Zellblock des Berichts (W = 1200 m², a = 0,25/0,80/1,00,
  d = 0,050/0,081/0,250) wird mit derselben Funktion nachgerechnet; weicht Ā von
  6,311 m²/a um mehr als 1e-3 ab, bricht das Skript ab.
* Kein Euro-Schritt, kein M0, kein λ — das macht T-0290.

Quellen je Ebene (ohne Schlüssel)
---------------------------------
quelle_hq_flaeche / quelle_hq_tiefe = quelle_flaeche_url / quelle_tiefe_url der
Karten-Datei des Landes, mehrere verschiedene URLs je Kommune und Szenario mit ' | '
verbunden (Reihenfolge des ersten Auftretens). quelle_gebaeudewert = quelle_url der
Zensus-Datei der Kommune.

Befunde des Laufs 17.09.2026
----------------------------
Verbundene Zellen = Karten-Zellen des Szenarios mit Zensus-Zeile (von allen
Karten-Zellen). Ersatzwert-Anteil Karte = Anteil der Karten-Zeilen mit
h_herkunft fallback_*; Ersatzwert-Anteil Zensus = Anteil der Zensus-Zeilen der
Kommune mit herkunft fallback_*.

Selbstkontrolle Zellblock: Ā = 6,3115 m²/a (Soll 6,311).

Kommune (AGS)    Szenario  verbunden/Karte  Ersatz Karte  W [m²]      A [m²]     | Ersatz Zensus | Ā [m²/a]
Grimma           HQhäufig     95 / 1 156       0,0 %         42 251      3 423,8 |
  (14729160)     HQ100       139 / 1 356       0,0 %        125 490     21 559,8 | 2,4 % (35/1 430) | 1 386,333
                 HQextrem    155 / 1 465       1,9 %        135 197     29 155,7 |
Dresden          HQhäufig    795 / 3 489       0,0 %        406 897     49 610,8 |
  (14612000)     HQ100     1 836 / 5 271       0,0 %      2 597 695    282 752,9 | 1,5 % (131/8 790) | 19 099,805
                 HQextrem  2 541 / 6 305       2,7 %      4 616 279    497 839,7 |
Deggendorf       HQhäufig     73 /   674       0,0 %         21 695      1 730,9 |
  (09271119)     HQ100       322 / 2 347      88,5 %        368 542     19 225,2 | 3,3 % (38/1 141) | 1 486,300
                 HQextrem    420 / 2 575       0,1 %        510 800     76 601,1 |
Passau           HQhäufig    152 /   805       0,0 %         66 266     15 160,7 |
  (09262000)     HQ100       217 /   964      11,1 %        187 486     34 219,3 | 2,2 % (37/1 687) | 2 772,174
                 HQextrem    289 / 1 154      15,0 %        307 503     68 197,8 |
Halle (Saale)    HQhäufig    140 / 2 175       0,0 %         44 818      8 360,6 |
  (15002000)     HQ100       176 / 2 397       0,0 %        103 625     15 632,8 | 1,6 % (58/3 662) | 2 387,502
                 HQextrem    400 / 2 881       0,0 %      1 098 551    203 842,1 |
Hitzacker        HQhäufig     10 /   488       0,0 %          1 467        356,5 |
  (03354009)     HQ100        10 /   490       0,0 %          1 493        373,2 | 1,5 % (5/324)     | 78,108
                 HQextrem     72 / 1 235       0,0 %         55 409      7 162,6 |
Rosenheim        HQhäufig     53 /   175       0,0 %         13 707      2 801,3 |
  (09163000)     HQ100        82 /   349       0,0 %         21 677      4 469,1 | 2,9 % (36/1 246) | 1 482,289
                 HQextrem    791 / 1 675       0,0 %      1 664 218    185 969,6 |
Reichertshofen   HQhäufig     25 /   177       0,0 %          3 077        450,8 |
  (09186147)     HQ100        33 /   214       0,0 %          5 352        657,1 | 0,6 % (2/358)     | 60,056
                 HQextrem     45 /   248       0,0 %         15 081      1 250,0 |

Auffällig: Deggendorf HQ100 trägt zu 88,5 % Ersatztiefen (fallback_kommune) aus dem
Kartenpaket Bayern; der HQ100-Schaden von Deggendorf ist damit überwiegend eine
Abschätzung, nicht Kartentiefe.

Modellgrenzen
-------------
* Keines der vier Kartenpakete hat für eine der acht Kommunen nur 'nicht_kartiert'
  oder 'nicht_ueberflutet' geliefert; der Markierungsfall ist implementiert (W und
  Schaden 0, URLs aus der Markierungszeile, Meldung im Lauf), trat aber nicht ein.
  Tritt er künftig ein, ist die 0 eine Modellgrenze der Kartenlage (Lackmustest §3.1),
  kein gemessenes Nullrisiko.
* Karten-Zellen ohne Zensus-Zeile tragen W_z = 0 (unbewohnte Zellen oder Zellen, die
  im Zensus-Paket geheim gehalten sind); ihre Zahl steht oben als Differenz.
* Die Ersatzwerte (fallback_kommune) stammen aus den Eingabepaketen und werden hier
  ungeprüft übernommen; ihr Anteil ist oben ausgewiesen.
"""
import csv
import os
import sys
from collections import OrderedDict

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ORDNER = os.path.join(WURZEL, 'docs', 'evidenz', '60_stichprobe')
ZENSUS = 'zensus_wohnflaeche.csv'
KARTEN = ('hq_sachsen.csv', 'hq_bayern.csv', 'hq_sachsen_anhalt.csv', 'hq_niedersachsen.csv')
AUSGABE = 'ergebnis_kernformel.csv'

KOMMUNEN = ('Grimma', 'Dresden', 'Deggendorf', 'Passau', 'Halle (Saale)', 'Hitzacker',
            'Rosenheim', 'Reichertshofen')
SZENARIEN = ('HQhäufig', 'HQ100', 'HQextrem')          # absteigend nach p sortiert
P = (1.0e-1, 1.0e-2, (5.0e-3 * 1.0e-3) ** 0.5)
MARKIERUNGEN = ('keine', 'nicht_kartiert', 'nicht_ueberflutet')

D1, D5, H1, H5 = 0.035, 0.250, 0.10, 1.75
F_S093 = F_S094 = 1.00


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


def main():
    a_bar_beispiel = selbstkontrolle()
    print('Selbstkontrolle Zellblock: Ā = %.4f m²/a' % a_bar_beispiel)

    zensus = lies(ZENSUS)
    wz, meta, zensus_n, zensus_fb = {}, {}, {}, {}
    for z in zensus:
        k = z['kommune']
        wz[(k, z['gitter_id'])] = zahl(z['wohnflaeche_m2'])
        m = (z['ags'], z['land'], z['quelle_url'])
        if meta.setdefault(k, m) != m:
            sys.exit('Zensus-Datei: uneinheitliche ags/land/quelle_url für %s' % k)
        zensus_n[k] = zensus_n.get(k, 0) + 1
        zensus_fb[k] = zensus_fb.get(k, 0) + z['herkunft'].startswith('fallback_')

    felder = {}
    for name in KARTEN:
        for z in lies(name):
            k, s = z['kommune'], z['szenario']
            if k not in KOMMUNEN or s not in SZENARIEN:
                sys.exit('%s: unbekannte Kommune/Szenario %r/%r' % (name, k, s))
            f = felder.setdefault((k, s), {'w': 0.0, 'a': 0.0, 'zellen': 0, 'verbunden': 0,
                                           'fallback': 0, 'markierung': [],
                                           'u_fl': OrderedDict(), 'u_ti': OrderedDict()})
            f['u_fl'][z['quelle_flaeche_url'].strip()] = None
            f['u_ti'][z['quelle_tiefe_url'].strip()] = None
            if ist_markierung(z):
                f['markierung'].append(z['h_herkunft'] or z['gitter_id'])
                continue
            f['zellen'] += 1
            f['fallback'] += z['h_herkunft'].startswith('fallback_')
            w = wz.get((k, z['gitter_id']))
            if w is None:
                continue                                   # Karten-Zelle ohne Zensus: W_z = 0
            f['verbunden'] += 1
            expo = w * zahl(z['a_anteil'])
            f['w'] += expo
            f['a'] += expo * d(zahl(z['h_m'])) * F_S093 * F_S094

    fehlend = [(k, s) for k in KOMMUNEN for s in SZENARIEN if (k, s) not in felder]
    fehlend += [(k, '-') for k in KOMMUNEN if k not in meta]
    if fehlend:
        sys.exit('Eingaben unvollständig, keine Werte erfunden: %r' % fehlend)

    zeilen, befunde = [], []
    for k in KOMMUNEN:
        a = [felder[(k, s)]['a'] for s in SZENARIEN]
        j = jahreswert(a)
        ags, land, q_geb = meta[k]
        teile = []
        for s in SZENARIEN:
            f = felder[(k, s)]
            for u in list(f['u_fl']) + list(f['u_ti']):
                if not u.startswith('http'):
                    sys.exit('%s/%s: Quelle ohne URL: %r' % (k, s, u))
            zeilen.append([k, ags, land, s, '%.6f' % f['w'], '%.6f' % f['a'], '%.6f' % j,
                           ' | '.join(f['u_fl']), ' | '.join(f['u_ti']), q_geb])
            anteil = f['fallback'] / f['zellen'] if f['zellen'] else 0.0
            teile.append('%s %d/%d Zellen, Ersatz Karte %.1f %%%s' % (
                s, f['verbunden'], f['zellen'], 100 * anteil,
                (', MODELLGRENZE nur Markierung ' + '/'.join(sorted(set(f['markierung']))))
                if f['markierung'] and not f['zellen'] else ''))
            if f['markierung']:
                print('Markierung %s/%s: %s' % (k, s, sorted(set(f['markierung']))))
        befunde.append('* %s (AGS %s): %s; Ersatz Zensus %.1f %% (%d von %d Zeilen); '
                       'W = %s m²; A = %s m²; Ā = %.3f m²/a' % (
                           k, ags, '; '.join(teile), 100 * zensus_fb[k] / zensus_n[k],
                           zensus_fb[k], zensus_n[k],
                           ' / '.join('%.0f' % felder[(k, s)]['w'] for s in SZENARIEN),
                           ' / '.join('%.1f' % felder[(k, s)]['a'] for s in SZENARIEN), j))

    with open(os.path.join(ORDNER, AUSGABE), 'w', encoding='utf-8', newline='') as fh:
        wr = csv.writer(fh, delimiter=';', lineterminator='\n')
        wr.writerow(['kommune', 'ags', 'land', 'szenario', 'w_exponiert_m2', 'a_schaden_m2',
                     'jahresschaden_m2a', 'quelle_hq_flaeche', 'quelle_hq_tiefe',
                     'quelle_gebaeudewert'])
        wr.writerows(zeilen)
    print('\n'.join(befunde))
    print('geschrieben: %s (%d Zeilen)' % (os.path.relpath(os.path.join(ORDNER, AUSGABE), WURZEL),
                                          len(zeilen)))


if __name__ == '__main__':
    main()

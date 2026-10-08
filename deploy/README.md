# Deployment (Testumgebung)

- `test-deploy.sh [main|<commit>]` läuft auf dem Server als Benutzer `overlord`, wird vom Watcher des Firmen-Repos
  bei Signal `deploy_anforderung` gestartet. Baut Frontend
  (`npm ci --no-audit --no-fund --loglevel=error && npm run build`) — derselbe Aufruf wie in `test-deploy.sh`;
  seit dem Entfernen der ungenutzten `@nebula.gl`-Pakete läuft `npm ci` ohne `--legacy-peer-deps` durch.
  Installiert das Backend in
  `/opt/overlord/kap2-venv`, migriert die Datenbank, startet `kap2-test.service` neu, prüft `/api/health` und
  schreibt `betrieb/deploy-status.json` ins Firmen-Repo (das ist das Signal für den CEO).
- Vor Abhängigkeiten, Bau, Migration und Neustart läuft der Schritt `deploy-tests`
  (`backend/tests/test_deploy_*.py` gegen den auszuliefernden Stand, T-0530). Ist ein Test rot,
  bricht der Lauf dort ab und meldet `fehler` — gebaut oder ausgeliefert wird nichts. Die Tests
  suchen Textanker in `test-deploy.sh` nur in Befehlszeilen (`backend/tests/_deploy_anker.py`):
  ein fehlender oder nur noch in einem Kommentar stehender Anker macht den Test rot, mit dem
  Namen des Ankers in der Meldung.
- Der Schritt `datenbank` führt genau einen Weg aus: `alembic upgrade head`. Davor gibt er die Zeile
  `Datenbank vorher: <Ausgabe von alembic current, oder leer>` aus, nach dem Erfolg
  `Datenbank nachher: <…>`; beide Werte stehen in den Shell-Variablen `DATENBANK_VORHER` und
  `DATENBANK_NACHHER`. Scheitert das Upgrade — auch mit „already exists“ —, endet der Schritt über die
  ERR-Falle (`Abbruch`, Deploy-Status `fehler`), und die Meldung verweist auf
  `docs/BETRIEB.md`, Abschnitt „Bestandsdatenbank auf die Migrationskette heben“. Der Deploy setzt
  den Alembic-Stand nie von Hand und legt das Schema nie auf anderem Weg an; ein Schema, das nicht aus
  der Migrationskette stammt, hebt ein Mensch nach dem Runbook auf die Kette.
- Der Schritt `beispielkommune` (T-1831, A-0066) steht nach dem Health-Check und vor `status`. Aufruf:
  `KAP2_VENV="$VENV" python3 "$PRODUKT/scripts/sicht_beispielkommune.py" --basis http://127.0.0.1:8010
  --neu-rechnen --anmeldung sitzung --warte-sekunden 900`. Er rechnet die Beispielkommune Warmsen mit dem
  gerade ausgelieferten Stand neu (legt Gemeindetabelle, Kommune und Maßnahme an, falls sie fehlen) und
  meldet sich mit einer technischen Sitzung an; `DATABASE_URL` und der Sitzungsschlüssel werden nie
  ausgegeben. **Wartegrenze:** 900 s für die Bewertung (Frist des Watchers: 30 min = 1800 s; schlechtester
  Fall 480 s + 900 s = 1380 s). Die ganze Ausgabe geht ins Protokoll, die letzte Zeile (JSON) liegt in der
  Datei, auf die die Shell-Variable `BEISPIEL_JSON` zeigt. **Rot** (ERR-Falle, Status `fehler`, nie
  `fertig`) wird der Schritt, wenn (1) das Skript mit Rückgabewert ≠ 0 endet, auch bei der Wartegrenze,
  (2) die letzte Ausgabezeile kein JSON-Objekt ist, (3) in `klimawirkungen` keine Bezeichnung mit `#95`,
  `#96` oder `#98` steht (die Meldung nennt die fehlenden), oder (4) der gemeldete `commit` nicht der
  ausgelieferte ist.
- Die Statusdatei `betrieb/deploy-status.json` trägt seit T-1832 zwei Felder als Nachweis ohne Browser;
  sie stehen in jedem Status, auch bei `fehler`:
  - `datenbank`: `{"vorher": …, "nachher": …}` mit der Ausgabe von `alembic current` vor und nach
    `alembic upgrade head` (Werte der Variablen `DATENBANK_VORHER` und `DATENBANK_NACHHER`). Eine leere
    Ausgabe (keine Tabelle `alembic_version` oder kein Eintrag darin) und ein Wert, der wegen eines
    früheren Abbruchs nie gesetzt wurde, stehen beide als `null`.
  - `beispielkommune`: `kommune`, `gemeindeschluessel`, `commit`, `zeit_rechnung` und `klimawirkungen`
    (Liste mit `bezeichnung` und `betrag_eur_jahr`), gelesen aus der Datei in `BEISPIEL_JSON`. Übernommen
    wird nur diese feste Auswahl, nie die ganze Datei. Ist die Datei nicht vorhanden, leer oder kein
    JSON-Objekt — etwa bei einem Abbruch vor dem Schritt —, steht `beispielkommune: null`; die Statusdatei
    mit `status: fehler` und den Protokollzeilen wird trotzdem geschrieben, auch unter `set -u`.
  Das Passwort steht nie in der Datei, nur `zugang.passwort_quelle` (T-0169). Der Watcher liest daraus nur
  `zeit`, `status` und `fehler`; die zusätzlichen Felder stören ihn nicht.
- **Regel für eine neue Datenbank der Testumgebung:** Sie bekommt ihr Schema nur über den Deploy.
  `kap2-test.service` darf vor dem ersten Deploy nicht starten, weil `app/main.py` beim Start
  `create_all` ausführt: Das Schema entstünde dann ohne Alembic-Stand, und der erste `alembic upgrade
  head` scheiterte an der Doppelanlage.
- `kap2-test.service`: uvicorn auf 127.0.0.1:8010, Konfiguration in `/etc/overlord/kap2-test.env`,
  läuft als `User=overlord`. Installation als **System-Unit**: `cp deploy/kap2-test.service
  /etc/systemd/system/kap2-test.service && systemctl daemon-reload && systemctl enable --now kap2-test`
  (als root).
- Neustart ohne `sudo`: Der Deploy-Lauf trägt die Sperre „no new privileges"; darunter kann `sudo`
  grundsätzlich nicht mehr nach root wechseln. `systemctl restart kap2-test` fragt stattdessen über
  D-Bus PID 1, die polkit befragt — kein setuid-Programm, die Sperre greift nicht. Die Berechtigung
  liegt auf dem Server als `.pkla`-Regel unter
  `/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla` (polkit 0.105 kennt keine
  JavaScript-`.rules`). Fehlt sie, bricht `test-deploy.sh` im Schritt `dienst` mit genau dieser
  Anweisung ab — es wird nichts übersprungen.
- Der Schritt `dienst` prüft nach dem Neustart, dass sich die `MainPID` geändert hat (und ≠ 0 ist)
  und dass `/api/health` auf 127.0.0.1:8010 den **gerade ausgerollten Commit** meldet. So kann kein
  alter, weiterlaufender Prozess ein Deployment fälschlich als `fertig` erscheinen lassen.
  `/api/health` liefert dazu neben `status` die Felder `commit` (überschreibbar über
  `KAP2_DEPLOY_COMMIT`) und `gestartet` (Prozessstart, ISO 8601).
- `apache-kap2-test.conf`: Apache-VHost, statisches `frontend/dist` plus Proxy für `/api`, HTTP-Basic-Auth.
- Nie auf eine Live-Umgebung. Kein FTP.

## Berechtigung für den Dienstneustart

- Welche Datei gilt, hängt von der polkit-Fassung auf dem Server ab: `deploy/polkit-kap2-test.rules`
  gilt für polkit ab 0.106 (JavaScript-Regeln); `deploy/polkit-kap2-test.pkla` gilt für polkit 0.105
  (`localauthority`, keine JavaScript-Regeln) — das ist die heute auf dem Server aktive Fassung.
- Die polkit-Fassung wird mit `dpkg -s policykit-1 | grep Version` festgestellt.
- Ablageort: `deploy/polkit-kap2-test.rules` gehört nach `/etc/polkit-1/rules.d/50-kap2-test.rules`,
  `deploy/polkit-kap2-test.pkla` gehört nach `/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla`.
- Die `.pkla`-Regel öffnet dem Benutzer `overlord` **alle** systemd-Einheiten und ist deshalb beim
  nächsten Betriebssystem-Sprung durch die `.rules`-Datei zu ersetzen.

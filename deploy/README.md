# Deployment (Testumgebung)

- `test-deploy.sh [main|<commit>]` läuft auf dem Server als Benutzer `overlord`, wird vom Watcher des Firmen-Repos
  bei Signal `deploy_anforderung` gestartet. Baut Frontend
  (`npm ci --no-audit --no-fund --loglevel=error && npm run build`) — derselbe Aufruf wie in `test-deploy.sh`;
  seit dem Entfernen der ungenutzten `@nebula.gl`-Pakete läuft `npm ci` ohne `--legacy-peer-deps` durch.
  Installiert das Backend in
  `/opt/overlord/kap2-venv`, migriert die Datenbank, startet `kap2-test.service` neu, prüft `/api/health` und
  schreibt `betrieb/deploy-status.json` ins Firmen-Repo (das ist das Signal für den CEO).
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

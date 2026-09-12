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
  /etc/systemd/system/ && systemctl daemon-reload && systemctl enable --now kap2-test` (als root).
- `polkit-kap2-test.rules`: **einmalig als root** nach `/etc/polkit-1/rules.d/50-kap2-test.rules`
  kopieren, dann `systemctl restart polkit`. Erst damit darf `overlord` im Deploy-Lauf
  `systemctl restart kap2-test` ausführen.
  - Hintergrund (T-0195, 8e34f7b0): Der Deploy-Lauf startete den Dienst früher über `sudo`. Der
    aufrufende Prozess trägt die Sperre „no new privileges"; darunter kann `sudo` grundsätzlich nicht
    mehr nach root wechseln — durch keine `sudoers`-Zeile behebbar.
  - Abwägung der Alternativen: (a) **Polkit-Regel** — gewählt; `systemctl restart` ohne `sudo` fragt
    über D-Bus PID 1, die Sperre greift nicht, weil kein setuid-Programm startet. Die Unit bleibt
    System-Unit (Boot-Start, Ordnung gegen `postgresql.service`, `User=overlord` bleibt erhalten),
    freigegeben wird genau eine Unit für genau einen Benutzer. (b) *systemd-User-Unit* — bräuchte
    zusätzlich `loginctl enable-linger overlord`, verlöre die Ordnung gegen `postgresql.service`
    und barg das Risiko, dass die alte System-Unit weiterläuft und der Health-Check fälschlich
    grün wird. (c) *Deploy als root* — verworfen, größere Rechteausweitung als nötig.
  - Beide Schritte liegen außerhalb des Produkt-Repos und müssen vor dem nächsten Deploy-Versuch
    auf dem Server ausgeführt werden. Fehlen sie, bricht `test-deploy.sh` im Schritt `dienst` mit
    genau diesen Anweisungen ab (es wird nichts übersprungen).
- Der Schritt `dienst` prüft nach dem Neustart, dass sich die `MainPID` geändert hat und dass
  `/api/health` auf 127.0.0.1:8010 den **gerade ausgerollten Commit** meldet. So kann kein alter,
  weiterlaufender Prozess ein Deployment fälschlich als `fertig` erscheinen lassen.
- `apache-kap2-test.conf`: Apache-VHost, statisches `frontend/dist` plus Proxy für `/api`, HTTP-Basic-Auth.
- Nie auf eine Live-Umgebung. Kein FTP.

# Deployment (Testumgebung)

- `test-deploy.sh [main|<commit>]` läuft auf dem Server als Benutzer `overlord`, wird vom Watcher des Firmen-Repos
  bei Signal `deploy_anforderung` gestartet. Baut Frontend
  (`npm ci --no-audit --no-fund --loglevel=error && npm run build`) — derselbe Aufruf wie in `test-deploy.sh`;
  seit dem Entfernen der ungenutzten `@nebula.gl`-Pakete läuft `npm ci` ohne `--legacy-peer-deps` durch.
  Installiert das Backend in
  `/opt/overlord/kap2-venv`, migriert die Datenbank, startet `kap2-test.service` neu, prüft `/api/health` und
  schreibt `betrieb/deploy-status.json` ins Firmen-Repo (das ist das Signal für den CEO).
- `kap2-test.service`: uvicorn auf 127.0.0.1:8010, Konfiguration in `/etc/overlord/kap2-test.env`. Seit T-0195
  eine **systemd-USER-Unit** von `overlord`, keine System-Unit mehr: installieren nach
  `~/overlord/.config/systemd/user/kap2-test.service` (Home des Benutzers `overlord`), aktivieren mit
  `systemctl --user enable kap2-test` als `overlord`. Einmalig als root nötig:
  `loginctl enable-linger overlord`, damit die User-systemd-Instanz von `overlord` auch ohne aktive
  Anmeldesitzung weiterläuft — sonst findet `systemctl --user restart kap2-test` im nicht-interaktiven
  Deploy-Lauf keinen User-Bus. Grund für die Umstellung: Ein Neustart einer System-Unit durch einen
  nicht-root-Benutzer braucht Rechteausweitung (sudo oder eine Polkit-Regel); sudo scheitert im
  Deploy-Lauf zuverlässig an der "no new privileges"-Sperre des aufrufenden Prozesses (T-0195,
  8e34f7b0) — das lässt sich durch keine Sudoers-Konfiguration mehr beheben. Als User-Unit braucht der
  Neustart keinerlei Rechteausweitung.
- `apache-kap2-test.conf`: Apache-VHost, statisches `frontend/dist` plus Proxy für `/api`, HTTP-Basic-Auth.
- Nie auf eine Live-Umgebung. Kein FTP.

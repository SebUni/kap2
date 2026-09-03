# Deployment (Testumgebung)

- `test-deploy.sh [main|<commit>]` läuft auf dem Server als Benutzer `overlord`, wird vom Watcher des Firmen-Repos
  bei Signal `deploy_anforderung` gestartet. Baut Frontend (`npm ci && npm run build`), installiert das Backend in
  `/opt/overlord/kap2-venv`, migriert die Datenbank, startet `kap2-test.service` neu, prüft `/api/health` und
  schreibt `betrieb/deploy-status.json` ins Firmen-Repo (das ist das Signal für den CEO).
- `kap2-test.service`: uvicorn auf 127.0.0.1:8010, Konfiguration in `/etc/overlord/kap2-test.env`.
- `apache-kap2-test.conf`: Apache-VHost, statisches `frontend/dist` plus Proxy für `/api`, HTTP-Basic-Auth.
- Nie auf eine Live-Umgebung. Kein FTP.

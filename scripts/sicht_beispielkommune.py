#!/usr/bin/env python3
"""Beispielkommune Warmsen für den Sichtstart anlegen (T-1775).

    python3 scripts/sicht_beispielkommune.py [--warte-sekunden N] [--basis URL] [--neu-rechnen]
                                             [--anmeldung lokal|sitzung]

Das Skript nutzt nur die Standardbibliothek. Es startet `bash scripts/sichtstart.sh`
als Kindprozess (eigene Postgres-Instanz, Backend auf 127.0.0.1:8000, Frontend auf
127.0.0.1:5173), wartet auf `/api/health` und steuert dann die API des Produkts
direkt, mit denselben Schritten wie die Oberfläche:

  (0) Gemeindetabelle füllen: fehlt die VG250-Gemeinde von Warmsen in `gemeinden`, läuft der
      vorhandene VG250-Import des Produkts (`ingest_gemeinden`, Niedersachsen). Ohne sie findet der
      Worker keinen Gemeindeschlüssel, und Stufe 2 der Ersatzregel 65+ entfällt (T-1814). War Warmsen
      schon berechnet, wird nach dem Füllen einmal neu berechnet.
  (a) vorhanden? Warmsen mit Status `done` und die Maßnahme da: nur lesen und ausgeben,
  (b) Suche und Anlegen der Kommune (Grenze aus OSM),
  (c) Raster erzeugen,
  (d) Bewertung einreihen und den Status abfragen, bis `done`,
  (e) genau eine Maßnahme aus dem Katalog anlegen und ihre Wirkung berechnen,
  (f) den Jahresbetrag #95 aus `risk-summary` lesen (API-Wert ohne Wirkung der Maßnahme; die Karte
      nimmt bei geladenem `cost-summary` den Stand mit Maßnahmen).

Zweites Ziel (T-1830): Mit `--basis URL` startet das Skript keinen Sichtstart, sondern spricht
einen laufenden Dienst unter dieser Adresse an (z. B. kap2-test auf 127.0.0.1:8010). Der Produktcode
(Gemeindetabelle, Gemeindeschlüssel, Sitzung) läuft dann gegen die Datenbank aus `DATABASE_URL`, mit
der Projektumgebung aus `KAP2_VENV`; fehlt `DATABASE_URL`, endet das Skript mit Exit 1.
`--neu-rechnen` reiht die Bewertung auch bei Status `done` neu ein und wartet bis `done`.
`--anmeldung sitzung` legt über Produktcode einen technischen Nutzer ohne verwendbares Passwort an
(falls er fehlt), erzeugt mit `auth_service.create_session` eine Sitzung, sendet sie als Cookie
`kap2_session` und widerruft sie am Ende mit `auth_service.revoke_session`. `/api/auth/me` muss den
technischen Nutzer nennen, sonst bricht das Skript ab. Der Sitzungsschlüssel erscheint in keiner
Ausgabe und reist nie als Argument.

Am Ende beendet es den Sichtstart mit SIGTERM und wartet auf sein Ende, auch bei
Fehlern. Keine Zahl wird von Hand in die Datenbank geschrieben; alle Beträge stammen
aus Antworten der API. Die letzte Zeile der Ausgabe ist JSON; Exit-Code 0 nur, wenn
alles gelungen ist. Die Schlusszeile nennt zusätzlich alle Klimawirkungen aus `risk-summary` mit
Jahresbetrag, den Commit des Dienstes (`/api/health`) und die Zeit der Rechnung (UTC).
"""
import argparse
import getpass
import gzip
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = "http://127.0.0.1:8000"
KOMMUNE = "Warmsen"
LANDKREIS_HINWEIS = "Nienburg"
MASSNAHME_PRAEFIX = "Sichtstart: "
# Risikocodes der Berichte #95 (Hitzebelastung) und #96 (Aeroallergene).
RISIKEN_95_96 = {
    "EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY",
    "EXPECTED_ANNUAL_ALLERGY_DAYS",
}
AGS_WARMSEN = "03256034"
BUNDESLAND_WARMSEN = "Niedersachsen"
VENV = os.environ.get("KAP2_VENV", os.path.join(os.path.expanduser("~"), ".venvs", "kap2"))
PGDATA = os.environ.get("KAP2_SICHT_PGDATA",
                        os.path.join(os.path.expanduser("~"), ".local", "share", "kap2-sicht", "pgdata"))
# Datenbank des Sichtstarts, gleiche Form wie in scripts/sichtstart.sh (Socket, ohne Passwort).
DATENBANK_URL = f"postgresql://{getpass.getuser()}@/kap2_sicht?host={PGDATA}"
# Ziel dieses Aufrufs: Adresse der API und Datenbank für den Produktcode (main setzt sie).
ZIEL = {"basis": BASIS, "datenbank": DATENBANK_URL}
GOLDEN_95_EUR = 175256  # backend/data/kalibrierung/golden95_zellen.md
SESSION_COOKIE = "kap2_session"  # backend/app/api/deps.py
TECHNIK_EMAIL = "sichtstart-technik@kap3.invalid"
SITZUNG_ENV = "KAP2_SICHT_SITZUNG"  # Übergabe an das Kind nur über die Umgebung, nie als Argument
# Die Sitzung des Laufs; der Wert wird in jeder Ausgabe durch *** ersetzt.
SITZUNG = {"wert": None}


class Fehler(RuntimeError):
    pass


def euro(betrag, stellen=2):
    """Betrag in deutscher Schreibweise: 144.392,88 €."""
    text = f"{betrag:,.{stellen}f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return text + " €"


def verdecke(text):
    """Ersetzt den Sitzungsschlüssel in einem Text durch ***."""
    wert = SITZUNG["wert"]
    return str(text).replace(wert, "***") if wert else str(text)


def melde(text):
    print(verdecke(text), flush=True)


# ── HTTP ──────────────────────────────────────────────────────────────────────

def api(methode, pfad, daten=None, timeout=120):
    """Eine Anfrage an die API; gibt das ausgewertete JSON zurück (gzip wird entpackt)."""
    body = None
    kopf = {"Accept": "application/json"}
    if SITZUNG["wert"]:
        kopf["Cookie"] = f"{SESSION_COOKIE}={SITZUNG['wert']}"
    if daten is not None:
        body = json.dumps(daten).encode("utf-8")
        kopf["Content-Type"] = "application/json"
    anfrage = urllib.request.Request(ZIEL["basis"] + pfad, data=body, method=methode, headers=kopf)
    try:
        with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
            roh = antwort.read()
            if antwort.headers.get("Content-Encoding") == "gzip":
                roh = gzip.decompress(roh)
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")[:500]
        raise Fehler(f"{methode} {pfad} -> HTTP {exc.code}: {verdecke(text)}") from exc
    except (urllib.error.URLError, OSError) as exc:
        raise Fehler(f"{methode} {pfad} nicht erreichbar: {verdecke(exc)}") from exc
    return json.loads(roh) if roh else None


# ── Sichtstart als Kindprozess ────────────────────────────────────────────────

def starte_sichtstart(log_pfad):
    log = open(log_pfad, "wb")
    proc = subprocess.Popen(
        ["bash", "scripts/sichtstart.sh"], cwd=ROOT,
        stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
    )
    return proc, log


def warte_auf_health(proc, log_pfad, sekunden):
    ende = time.time() + sekunden
    while time.time() < ende:
        if proc is not None and proc.poll() is not None:
            raise Fehler(f"Sichtstart endete vorzeitig (Exit {proc.returncode}):\n{log_ende(log_pfad)}")
        try:
            with urllib.request.urlopen(ZIEL["basis"] + "/api/health", timeout=5) as r:
                if r.status == 200:
                    return
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(2)
    raise Fehler(f"/api/health antwortet nach {sekunden} s nicht:\n{log_ende(log_pfad) if proc else ''}")


def beende_sichtstart(proc, log):
    if proc.poll() is None:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
    log.close()


def log_ende(log_pfad, zeichen=2000):
    try:
        with open(log_pfad, "rb") as f:
            return f.read()[-zeichen:].decode("utf-8", "replace")
    except OSError:
        return "(kein Protokoll)"


# ── Produktcode in der Projektumgebung (Gemeindetabelle) ──────────────────────

_CODE_FUELLEN = """
import json, sys
from app.db.database import SessionLocal
from app.models.lite_models import Gemeinde
from app.services.lite.vg250_loader import ingest_gemeinden
ags, land = sys.argv[1], sys.argv[2]
db = SessionLocal()
try:
    vorher = db.query(Gemeinde).count()
    da = db.query(Gemeinde.ags).filter(Gemeinde.ags == ags).first() is not None
    geschrieben = 0
    if not da:
        geschrieben = ingest_gemeinden(db, bundesland=land)
    print(json.dumps({"vorher": vorher, "warmsen_vorher": da, "geschrieben": geschrieben,
                      "nachher": db.query(Gemeinde).count(),
                      "warmsen_nachher": db.query(Gemeinde.ags).filter(Gemeinde.ags == ags).first() is not None}))
finally:
    db.close()
"""

_CODE_SCHLUESSEL = """
import sys
from app.db.database import SessionLocal
from app.models.models import Kommune
from app.tasks.assessment_worker import _gemeindeschluessel
db = SessionLocal()
try:
    print(_gemeindeschluessel(db, db.query(Kommune).filter(Kommune.id == int(sys.argv[1])).first()))
finally:
    db.close()
"""


def produktcode(code, *argumente, timeout=1800, umgebung=None):
    """Führt Produktcode mit der Projektumgebung gegen die Datenbank des Ziels aus (Sichtstart-
    Datenbank, mit `--basis` `DATABASE_URL`); gibt die letzte Ausgabezeile zurück.

    `umgebung`: zusätzliche Umgebungsvariablen (so reist die Sitzung zum Kind, nie als Argument).
    """
    python = os.path.join(VENV, "bin", "python")
    if not os.path.exists(python):
        raise Fehler(f"Projektumgebung fehlt: {python} (anlegen mit bash scripts/testlauf.sh)")
    env = dict(os.environ, DATABASE_URL=ZIEL["datenbank"],
               PYTHONPYCACHEPREFIX=os.path.join(VENV, "pycache"), **(umgebung or {}))
    try:
        p = subprocess.run([python, "-c", code, *argumente], cwd=os.path.join(ROOT, "backend"),
                           env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise Fehler(f"Produktcode nach {timeout} s nicht fertig") from exc
    if p.returncode != 0:
        raise Fehler(f"Produktcode endete mit Exit {p.returncode}:\n{verdecke((p.stdout + p.stderr)[-2000:])}")
    zeilen = [z for z in p.stdout.splitlines() if z.strip()]
    return zeilen[-1] if zeilen else ""


# Technischer Nutzer: feste Adresse (.invalid wird nie aufgelöst) und Passwort-Hash "!". Das ist kein
# bcrypt-Hash; `auth_service.verify_password` fängt den ValueError und liefert False, ein Login mit
# Passwort ist damit nie möglich. `Kommune` wird mitimportiert, weil der Mapper von `User` sie kennt.
_CODE_SITZUNG_ANLEGEN = """
import sys
from app.db.database import SessionLocal
from app.models.models import Kommune  # noqa: F401
from app.models.auth_models import User, ROLE_ADMIN
from app.services import auth_service
email = sys.argv[1]
db = SessionLocal()
try:
    nutzer = db.query(User).filter(User.email == email).first()
    if nutzer is None:
        nutzer = User(email=email, password_hash="!", display_name="Sichtstart (technisch)",
                      role=ROLE_ADMIN, is_active=True)
        db.add(nutzer)
        db.commit()
        db.refresh(nutzer)
    elif nutzer.password_hash != "!" or nutzer.role != ROLE_ADMIN or not nutzer.is_active:
        nutzer.password_hash, nutzer.role, nutzer.is_active = "!", ROLE_ADMIN, True
        db.commit()
    print(auth_service.create_session(db, nutzer))
finally:
    db.close()
"""

_CODE_SITZUNG_WIDERRUFEN = """
import os
from app.db.database import SessionLocal
from app.models.models import Kommune  # noqa: F401
from app.models.auth_models import User  # noqa: F401
from app.services import auth_service
db = SessionLocal()
try:
    auth_service.revoke_session(db, os.environ["KAP2_SICHT_SITZUNG"])
    print("widerrufen")
finally:
    db.close()
"""


def melde_sitzung_an():
    """`--anmeldung sitzung`: technischen Nutzer anlegen (falls er fehlt), Sitzung erzeugen und über
    `/api/auth/me` belegen, dass genau sie wirkt (nicht die lokale Anmeldung des Sichtstarts)."""
    SITZUNG["wert"] = produktcode(_CODE_SITZUNG_ANLEGEN, TECHNIK_EMAIL) or None
    if not SITZUNG["wert"]:
        raise Fehler("Die Sitzung wurde nicht erzeugt (keine Ausgabe des Produktcodes).")
    ich = api("GET", "/api/auth/me")
    nutzer = (ich or {}).get("user") or {}
    if not (ich or {}).get("authenticated") or nutzer.get("email") != TECHNIK_EMAIL:
        raise Fehler(f"/api/auth/me nennt nicht den technischen Nutzer {TECHNIK_EMAIL}, sondern "
                     f"{nutzer.get('email')!r} – Abbruch, die Sitzung wirkt nicht.")
    melde(f"Angemeldet als {TECHNIK_EMAIL} (Rolle {nutzer.get('role')}) laut /api/auth/me.")


def widerrufe_sitzung():
    """Sitzung im `finally` widerrufen; gibt False zurück, wenn das scheitert."""
    if not SITZUNG["wert"]:
        return True
    try:
        produktcode(_CODE_SITZUNG_WIDERRUFEN, umgebung={SITZUNG_ENV: SITZUNG["wert"]}, timeout=120)
    except Fehler as exc:
        print(f"FEHLER: Sitzung nicht widerrufen: {verdecke(exc)}", file=sys.stderr, flush=True)
        return False
    melde("Sitzung widerrufen.")
    return True


def fuelle_gemeinden():
    """(0) Gemeindetabelle über den VG250-Import des Produkts füllen, wenn Warmsen fehlt.

    Gibt True zurück, wenn dabei geschrieben wurde (eine frühere Bewertung ist dann veraltet).
    """
    melde("Gemeindetabelle prüfen (VG250, ggf. Download und Import für Niedersachsen) …")
    antwort = json.loads(produktcode(_CODE_FUELLEN, AGS_WARMSEN, BUNDESLAND_WARMSEN))
    if not antwort["warmsen_nachher"]:
        raise Fehler(f"Gemeinde {AGS_WARMSEN} fehlt nach dem VG250-Import in `gemeinden`.")
    if antwort["warmsen_vorher"]:
        melde(f"Gemeindetabelle schon gefüllt: {antwort['nachher']} Zeilen, Warmsen ({AGS_WARMSEN}) dabei.")
        return False
    melde(f"Gemeindetabelle gefüllt: {antwort['vorher']} → {antwort['nachher']} Zeilen "
          f"({antwort['geschrieben']} Gemeinden {BUNDESLAND_WARMSEN} aus VG250), Warmsen ({AGS_WARMSEN}) dabei.")
    return True


# ── Schritte ──────────────────────────────────────────────────────────────────

def finde_kommune():
    treffer = [k for k in api("GET", "/api/kommune") if k["name"] == KOMMUNE]
    return treffer[0] if treffer else None


def lege_kommune_an():
    """(b) Suche und Anlegen mit dem Suchtreffer, wie die Oberfläche es tut."""
    treffer = None
    for versuch in range(4):
        try:
            ergebnisse = api("GET", "/api/kommune/search?q=" + urllib.parse.quote(KOMMUNE))
        except Fehler as exc:
            melde(f"Suche fehlgeschlagen (Versuch {versuch + 1}/4): {exc}")
            time.sleep(10)
            continue
        passend = [
            e for e in ergebnisse
            if e.get("name") == KOMMUNE and e.get("osm_type") == "relation"
            and LANDKREIS_HINWEIS in e.get("display_name", "")
        ]
        if passend:
            treffer = passend[0]
            break
        time.sleep(5)
    if not treffer:
        raise Fehler(f"Kein Suchtreffer „{KOMMUNE}“ im Landkreis {LANDKREIS_HINWEIS} (Nominatim).")
    daten = {k: treffer.get(k) for k in ("osm_id", "name", "osm_type", "geojson", "address")}
    daten["bundesland"] = (treffer.get("address") or {}).get("state")
    kommune = api("POST", "/api/kommune", daten, timeout=300)
    melde(f"Kommune angelegt: {kommune['name']} (id {kommune['id']}, OSM {kommune['osm_id']}, "
          f"{kommune.get('landkreis')}, {kommune.get('area_km2')} km²)")
    return kommune


def bewertung(kommune_id, max_sekunden, neu_rechnen=False, grund_neu=""):
    """(c)+(d) Raster, Bewertung einreihen, abfragen bis `done`. Gibt den Status zurück.

    `neu_rechnen`: eine abgeschlossene Bewertung wird einmal neu eingereitet (Gemeindetabelle eben
    gefüllt oder `--neu-rechnen`) und erst als fertig gewertet, wenn ihr `finished_at` ein neues ist.
    """
    status = api("GET", f"/api/kommune/{kommune_id}/status")
    alt_ende = None
    if status.get("status") == "done" and neu_rechnen:
        melde(f"Bewertung wird neu berechnet{grund_neu}.")
        alt_ende = status.get("finished_at")
        api("POST", f"/api/kommune/{kommune_id}/assess")
        status = {"status": "queued"}
    elif status.get("status") == "done":
        melde("Bewertung schon abgeschlossen (done): kein neuer Bewertungslauf gestartet.")
        return status
    if status.get("status") in (None, "error"):
        if status.get("status") == "error":
            melde(f"Letzter Lauf endete mit error: {status.get('message')} – neuer Versuch.")
        raster = api("POST", f"/api/kommune/{kommune_id}/grid", {"cell_size_m": 100}, timeout=600)
        melde(f"Raster: {raster['cells_created']} Zellen à {raster['cell_size_m']} m")
        api("POST", f"/api/kommune/{kommune_id}/assess")
        melde("Bewertung eingereiht.")
    else:
        melde(f"Bewertung läuft schon ({status.get('status')}): es wird nur gewartet.")
    start = time.time()
    letzte = None
    while time.time() - start < max_sekunden:
        status = api("GET", f"/api/kommune/{kommune_id}/status")
        zeile = (status.get("status"), round(status.get("progress_pct") or 0), status.get("message"))
        if zeile != letzte:
            melde(f"[{int(time.time() - start):>5} s] {zeile[0]} {zeile[1]} % {zeile[2] or ''}")
            letzte = zeile
        if status.get("status") == "done" and (alt_ende is None or status.get("finished_at") != alt_ende):
            return status
        if status.get("status") == "error":
            raise Fehler(f"Bewertung endete mit error: {status.get('message')}")
        time.sleep(15)
    raise Fehler(f"Bewertung nach {max_sekunden} s nicht fertig (letzter Stand: {letzte}).")


def groesste_flaeche(geojson):
    """Größtes Polygon (Außenring) der Gemeindegrenze als GeoJSON-Polygon."""
    if geojson["type"] == "Polygon":
        return geojson
    def flaeche(poly):
        ring = poly[0]
        return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]))) / 2
    return {"type": "Polygon", "coordinates": max(geojson["coordinates"], key=flaeche)}


def katalog_kandidaten():
    """Maßnahmentypen mit Nutzen für #95 oder #96, deren Eingaben der Katalog vorgibt."""
    kandidaten = []
    for m in api("GET", "/api/measure-catalog"):
        if not RISIKEN_95_96.intersection(m.get("linked_risk_codes") or []):
            continue
        eingaben = m.get("config_inputs") or {}
        if m.get("config_input_help") and not eingaben:
            continue  # Eingaben ohne Voreinstellung im Katalog: nichts raten
        config = {k: v.get("voreinstellung") for k, v in eingaben.items()}
        kandidaten.append((m, config))
    return kandidaten


def massnahme(kommune):
    """(e) Genau eine Maßnahme; gibt (Maßnahme, Wirkung, Begründung, neu) zurück."""
    kid = kommune["id"]
    vorhandene = [m for m in api("GET", f"/api/kommune/{kid}/measures")
                  if (m.get("name") or "").startswith(MASSNAHME_PRAEFIX)]
    if vorhandene:
        m = vorhandene[0]
        wirkung = api("POST", f"/api/measures/{m['id']}/calculate-impact", timeout=300)
        return m, wirkung, "schon vorhanden", False
    flaeche = groesste_flaeche(api("GET", f"/api/kommune/{kid}")["boundary_geojson"])
    verworfen = []
    for eintrag, config in katalog_kandidaten():
        m = api("POST", f"/api/kommune/{kid}/measures", {
            "name": MASSNAHME_PRAEFIX + eintrag["name"],
            "measure_type": eintrag["code"],
            "geometry_geojson": flaeche,
            "config": config,
            "description": "Beispielmaßnahme der Sichtprüfung (scripts/sicht_beispielkommune.py)",
        }, timeout=300)
        wirkung = api("POST", f"/api/measures/{m['id']}/calculate-impact", timeout=600)
        if (wirkung.get("annual_benefit_eur") or 0) > 0:
            grund = (f"erster Katalogtyp mit Nutzen für #95/#96 und Jahresnutzen > 0"
                     + (f"; zuvor ohne Nutzen: {', '.join(verworfen)}" if verworfen else ""))
            return m, wirkung, grund, True
        api("DELETE", f"/api/measures/{m['id']}")
        verworfen.append(eintrag["code"])
        melde(f"Maßnahme {eintrag['code']} liefert keinen Nutzen und wurde wieder entfernt.")
    raise Fehler("Kein Maßnahmentyp für #95/#96 liefert einen Nutzen größer 0.")


def betrag_95(kommune_id):
    """(f) Jahresbetrag #95 ohne Wirkung der Maßnahme (API-Wert aus `risk-summary`).

    Die Karte „Erwartete Schäden je Risiko“ zeigt ihn nur, solange `cost-summary` nicht geladen ist.
    """
    cost = api("GET", f"/api/kommune/{kommune_id}/risk-summary")["cost"]
    for k in cost["klimawirkungen"]:
        if "#95" in (k.get("bezeichnung") or ""):
            return float(k["cost_eur"]), k["bezeichnung"]
    raise Fehler("risk-summary enthält keine Klimawirkung #95.")


def baue_klimawirkungen(risk_summary):
    """Alle Einträge aus `risk-summary` → `cost.klimawirkungen` als Liste mit `bezeichnung` und
    `betrag_eur_jahr` (aus `cost_eur`, auf den Cent gerundet; ohne Euro-Ebene `null`)."""
    liste = []
    for k in (risk_summary.get("cost") or {}).get("klimawirkungen") or []:
        betrag = k.get("cost_eur")
        liste.append({"bezeichnung": k.get("bezeichnung"),
                      "betrag_eur_jahr": None if betrag is None else round(float(betrag), 2)})
    return liste


def zeit_utc(zeitpunkt):
    """`finished_at` der API (UTC, meist ohne Zonenangabe) als ISO 8601 mit +00:00; None bleibt None."""
    if not zeitpunkt:
        return None
    zeit = datetime.fromisoformat(zeitpunkt)
    if zeit.tzinfo is None:
        zeit = zeit.replace(tzinfo=timezone.utc)
    return zeit.astimezone(timezone.utc).isoformat()


def arbeite(max_sekunden, neu_rechnen=False):
    start = time.time()
    gemeinden_neu = fuelle_gemeinden()
    kommune = finde_kommune()
    war_vorhanden = kommune is not None
    if not kommune:
        kommune = lege_kommune_an()
    else:
        melde(f"Kommune {kommune['name']} schon vorhanden (id {kommune['id']}).")
    ags = produktcode(_CODE_SCHLUESSEL, str(kommune["id"]))
    melde(f"Gemeindeschlüssel für {kommune['name']} laut Worker-Abfrage: {ags}")
    if ags in ("", "None"):
        raise Fehler("Die Abfrage des Workers liefert für Warmsen keinen Gemeindeschlüssel.")
    status = bewertung(kommune["id"], max_sekunden, neu_rechnen=gemeinden_neu or neu_rechnen,
                       grund_neu=" (--neu-rechnen)" if neu_rechnen else " (Gemeindetabelle eben gefüllt)")
    kommune = api("GET", f"/api/kommune/{kommune['id']}")  # Einwohner stehen erst nach der Bewertung
    m, wirkung, grund, neu = massnahme(kommune)
    betrag, bezeichnung = betrag_95(kommune["id"])
    zellen = len(api("GET", f"/api/measures/{m['id']}/impacts"))
    melde(f"Maßnahme: {m['name']} (Typ {m['measure_type']}, {zellen} Zellen mit Wirkung) – {grund}")
    melde(f"Jahresbetrag {bezeichnung}: {euro(betrag)} (Golden-Test #95 im Bericht: "
          f"{euro(GOLDEN_95_EUR, 0)}; Abweichung {euro(betrag - GOLDEN_95_EUR)}, nicht angeglichen)")
    melde(f"Einwohner laut Kommune: {kommune.get('population')} (Golden-Test: 3087)")
    if war_vorhanden and not neu and not gemeinden_neu and not neu_rechnen:
        melde("Nichts neu angelegt: Kommune und Maßnahme waren da, kein neuer Bewertungslauf.")
    melde(f"Dauer dieses Aufrufs ohne Sichtstart-Start: {int(time.time() - start)} s")
    zusammenfassung = api("GET", f"/api/kommune/{kommune['id']}/risk-summary")
    gesundheit = api("GET", "/api/health")
    return {
        "kommune": kommune["name"],
        "kommune_id": kommune["id"],
        "status": status["status"],
        "gemeindeschluessel": ags,
        "betrag_95_eur_jahr": round(betrag, 2),
        "massnahme": {"name": m["name"], "typ": m["measure_type"]},
        "nutzen_eur_jahr": float(wirkung["annual_benefit_eur"]),
        "massnahmen_mit_praefix": sum(1 for x in api("GET", f"/api/kommune/{kommune['id']}/measures")
                                      if (x.get("name") or "").startswith(MASSNAHME_PRAEFIX)),
        "klimawirkungen": baue_klimawirkungen(zusammenfassung),
        "commit": gesundheit.get("commit"),
        "zeit_rechnung": zeit_utc(status.get("finished_at")),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--warte-sekunden", type=int, default=7200,
                    help="längste Wartezeit auf die Bewertung (Vorgabe 7200)")
    ap.add_argument("--start-sekunden", type=int, default=300,
                    help="längste Wartezeit auf /api/health (Vorgabe 300)")
    ap.add_argument("--basis", metavar="URL",
                    help="laufenden Dienst unter dieser Adresse ansprechen, kein Sichtstart; "
                         "Produktcode läuft gegen DATABASE_URL")
    ap.add_argument("--neu-rechnen", action="store_true",
                    help="Bewertung auch bei Status done neu einreihen und bis done warten")
    ap.add_argument("--anmeldung", choices=("lokal", "sitzung"), default="lokal",
                    help="lokal: Anmeldung des Sichtstarts (Vorgabe); sitzung: technischer Nutzer "
                         "mit Cookie kap2_session")
    args = ap.parse_args(argv)

    if args.basis:
        datenbank = os.environ.get("DATABASE_URL")
        if not datenbank:
            print("FEHLER: Mit --basis muss die Umgebungsvariable DATABASE_URL gesetzt sein "
                  "(Datenbank des Dienstes für den Produktcode).", file=sys.stderr, flush=True)
            return 1
        ZIEL["basis"] = args.basis.rstrip("/")
        ZIEL["datenbank"] = datenbank

    log_pfad = os.path.join(tempfile.gettempdir(), f"sichtstart-beispielkommune-{os.getpid()}.log")
    t0 = time.time()
    proc = log = None
    ergebnis = None
    rc = 0
    try:
        if not args.basis:
            proc, log = starte_sichtstart(log_pfad)
        warte_auf_health(proc, log_pfad, args.start_sekunden)
        melde(f"{'Sichtstart' if proc else 'Dienst unter ' + ZIEL['basis']} bereit nach {int(time.time() - t0)} s.")
        if args.anmeldung == "sitzung":
            melde_sitzung_an()
        ergebnis = arbeite(args.warte_sekunden, neu_rechnen=args.neu_rechnen)
    except Fehler as exc:
        print(f"FEHLER: {verdecke(exc)}", file=sys.stderr, flush=True)
        rc = 1
    finally:
        if not widerrufe_sitzung():
            rc = 1
        if proc is not None:
            beende_sichtstart(proc, log)
            melde("Sichtstart beendet.")
    if rc == 0 and ergebnis is not None:
        print(verdecke(json.dumps(ergebnis, ensure_ascii=False)), flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())

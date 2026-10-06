#!/usr/bin/env python3
"""Beispielkommune Warmsen für den Sichtstart anlegen (T-1775).

    python3 scripts/sicht_beispielkommune.py [--warte-sekunden N]

Das Skript nutzt nur die Standardbibliothek. Es startet `bash scripts/sichtstart.sh`
als Kindprozess (eigene Postgres-Instanz, Backend auf 127.0.0.1:8000, Frontend auf
127.0.0.1:5173), wartet auf `/api/health` und steuert dann die API des Produkts
direkt, mit denselben Schritten wie die Oberfläche:

  (a) vorhanden? Warmsen mit Status `done` und die Maßnahme da: nur lesen und ausgeben,
  (b) Suche und Anlegen der Kommune (Grenze aus OSM),
  (c) Raster erzeugen,
  (d) Bewertung einreihen und den Status abfragen, bis `done`,
  (e) genau eine Maßnahme aus dem Katalog anlegen und ihre Wirkung berechnen,
  (f) den Jahresbetrag #95 aus `risk-summary` lesen (API-Wert ohne Wirkung der Maßnahme; die Karte
      nimmt bei geladenem `cost-summary` den Stand mit Maßnahmen).

Am Ende beendet es den Sichtstart mit SIGTERM und wartet auf sein Ende, auch bei
Fehlern. Keine Zahl wird von Hand in die Datenbank geschrieben; alle Beträge stammen
aus Antworten der API. Die letzte Zeile der Ausgabe ist JSON; Exit-Code 0 nur, wenn
alles gelungen ist.
"""
import argparse
import gzip
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
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
GOLDEN_95_EUR = 175256  # backend/data/kalibrierung/golden95_zellen.md


class Fehler(RuntimeError):
    pass


def euro(betrag, stellen=2):
    """Betrag in deutscher Schreibweise: 144.392,88 €."""
    text = f"{betrag:,.{stellen}f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return text + " €"


def melde(text):
    print(text, flush=True)


# ── HTTP ──────────────────────────────────────────────────────────────────────

def api(methode, pfad, daten=None, timeout=120):
    """Eine Anfrage an die API; gibt das ausgewertete JSON zurück (gzip wird entpackt)."""
    body = None
    kopf = {"Accept": "application/json"}
    if daten is not None:
        body = json.dumps(daten).encode("utf-8")
        kopf["Content-Type"] = "application/json"
    anfrage = urllib.request.Request(BASIS + pfad, data=body, method=methode, headers=kopf)
    try:
        with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
            roh = antwort.read()
            if antwort.headers.get("Content-Encoding") == "gzip":
                roh = gzip.decompress(roh)
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")[:500]
        raise Fehler(f"{methode} {pfad} -> HTTP {exc.code}: {text}") from exc
    except (urllib.error.URLError, OSError) as exc:
        raise Fehler(f"{methode} {pfad} nicht erreichbar: {exc}") from exc
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
        if proc.poll() is not None:
            raise Fehler(f"Sichtstart endete vorzeitig (Exit {proc.returncode}):\n{log_ende(log_pfad)}")
        try:
            with urllib.request.urlopen(BASIS + "/api/health", timeout=5) as r:
                if r.status == 200:
                    return
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(2)
    raise Fehler(f"/api/health antwortet nach {sekunden} s nicht:\n{log_ende(log_pfad)}")


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


def bewertung(kommune_id, max_sekunden):
    """(c)+(d) Raster, Bewertung einreihen, abfragen bis `done`. Gibt den Status zurück."""
    status = api("GET", f"/api/kommune/{kommune_id}/status")
    if status.get("status") == "done":
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
        if status.get("status") == "done":
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


def arbeite(max_sekunden):
    start = time.time()
    kommune = finde_kommune()
    war_vorhanden = kommune is not None
    if not kommune:
        kommune = lege_kommune_an()
    else:
        melde(f"Kommune {kommune['name']} schon vorhanden (id {kommune['id']}).")
    status = bewertung(kommune["id"], max_sekunden)
    kommune = api("GET", f"/api/kommune/{kommune['id']}")  # Einwohner stehen erst nach der Bewertung
    m, wirkung, grund, neu = massnahme(kommune)
    betrag, bezeichnung = betrag_95(kommune["id"])
    zellen = len(api("GET", f"/api/measures/{m['id']}/impacts"))
    melde(f"Maßnahme: {m['name']} (Typ {m['measure_type']}, {zellen} Zellen mit Wirkung) – {grund}")
    melde(f"Jahresbetrag {bezeichnung}: {euro(betrag)} (Golden-Test #95 im Bericht: "
          f"{euro(GOLDEN_95_EUR, 0)}; Abweichung {euro(betrag - GOLDEN_95_EUR)}, nicht angeglichen)")
    melde(f"Einwohner laut Kommune: {kommune.get('population')} (Golden-Test: 3087)")
    if war_vorhanden and not neu:
        melde("Nichts neu angelegt: Kommune und Maßnahme waren da, kein neuer Bewertungslauf.")
    melde(f"Dauer dieses Aufrufs ohne Sichtstart-Start: {int(time.time() - start)} s")
    return {
        "kommune": kommune["name"],
        "kommune_id": kommune["id"],
        "status": status["status"],
        "betrag_95_eur_jahr": round(betrag, 2),
        "massnahme": {"name": m["name"], "typ": m["measure_type"]},
        "nutzen_eur_jahr": float(wirkung["annual_benefit_eur"]),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--warte-sekunden", type=int, default=7200,
                    help="längste Wartezeit auf die Bewertung (Vorgabe 7200)")
    ap.add_argument("--start-sekunden", type=int, default=300,
                    help="längste Wartezeit auf /api/health (Vorgabe 300)")
    args = ap.parse_args()

    log_pfad = os.path.join(tempfile.gettempdir(), f"sichtstart-beispielkommune-{os.getpid()}.log")
    t0 = time.time()
    proc, log = starte_sichtstart(log_pfad)
    try:
        warte_auf_health(proc, log_pfad, args.start_sekunden)
        melde(f"Sichtstart bereit nach {int(time.time() - t0)} s.")
        ergebnis = arbeite(args.warte_sekunden)
    except Fehler as exc:
        print(f"FEHLER: {exc}", file=sys.stderr, flush=True)
        return 1
    finally:
        beende_sichtstart(proc, log)
        melde("Sichtstart beendet.")
    print(json.dumps(ergebnis, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

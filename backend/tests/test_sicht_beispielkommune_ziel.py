"""scripts/sicht_beispielkommune.py, zweites Ziel (T-1830): laufender Dienst, Neurechnung, Sitzung.

Nur Standardbibliothek und pytest, ohne Datenbank und ohne Netz: Alle Aufrufe der API und des
Produktcodes sind durch Attrappen ersetzt. Die Datei heißt bewusst nicht `test_deploy_*`.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

PFAD = Path(__file__).resolve().parents[2] / "scripts" / "sicht_beispielkommune.py"
# Fester Attrappenwert ohne Ziffer; kein echter Sitzungsschlüssel.
ATTRAPPE = "attrappe-sitzungswert-nicht-echt"

RISK_SUMMARY = {
    "cost": {
        "klimawirkungen": [
            {"bezeichnung": "Hitzebelastung (#95)", "cost_eur": 179020.8149},
            {"bezeichnung": "UV-bedingte Gesundheitsschädigungen (#98)", "cost_eur": 13053.026},
            {"bezeichnung": "Allergische Reaktionen (#96)", "cost_eur": 2280.6},
            {"bezeichnung": "Ohne Euro-Ebene", "cost_eur": None},
        ]
    }
}


@pytest.fixture()
def sk(monkeypatch):
    """Frisch geladenes Skript; der Sitzungszustand ist leer."""
    spec = importlib.util.spec_from_file_location("sicht_beispielkommune_unter_test", PFAD)
    modul = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modul
    spec.loader.exec_module(modul)
    monkeypatch.setattr(modul.time, "sleep", lambda _s: None)
    monkeypatch.setattr(modul, "starte_sichtstart", lambda _p: pytest.fail("Sichtstart gestartet"))
    yield modul
    sys.modules.pop(spec.name, None)


class FakeAntwort:
    def __init__(self, inhalt):
        self._roh = json.dumps(inhalt).encode("utf-8")
        self.headers = {}
        self.status = 200

    def read(self):
        return self._roh

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False


def _stubs_fuer_lauf(sk, monkeypatch, aufrufe, *, me=None, widerruf_ok=True):
    """Ersetzt Health-Wartezeit, Produktcode, API und Arbeit durch Attrappen."""
    monkeypatch.setattr(sk, "warte_auf_health", lambda *a, **k: None)

    def produktcode(code, *argumente, timeout=0, umgebung=None):
        if code is sk._CODE_SITZUNG_ANLEGEN:
            aufrufe.append(("anlegen", argumente))
            return ATTRAPPE
        if code is sk._CODE_SITZUNG_WIDERRUFEN:
            aufrufe.append(("widerrufen", argumente, dict(umgebung or {})))
            if not widerruf_ok:
                raise sk.Fehler(f"Produktcode endete mit Exit 1: {ATTRAPPE}")
            return "widerrufen"
        pytest.fail("unerwarteter Produktcode")

    def api(methode, pfad, daten=None, timeout=0):
        aufrufe.append((methode, pfad))
        if pfad == "/api/auth/me":
            return me if me is not None else {
                "authenticated": True,
                "user": {"email": sk.TECHNIK_EMAIL, "role": "admin"}}
        pytest.fail(f"unerwartete Anfrage {pfad}")

    monkeypatch.setattr(sk, "produktcode", produktcode)
    monkeypatch.setattr(sk, "api", api)


def test_basis_startet_keinen_sichtstart(sk, monkeypatch, capsys):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    aufrufe = []
    _stubs_fuer_lauf(sk, monkeypatch, aufrufe)
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: {"kommune": "Oschatz"})
    rc = sk.main(["--basis", "http://127.0.0.1:8010/"])
    assert rc == 0  # starte_sichtstart würde pytest.fail auslösen
    assert sk.ZIEL == {"basis": "http://127.0.0.1:8010", "datenbank": "postgresql://dienst@/ziel"}
    assert capsys.readouterr().out.strip().splitlines()[-1] == '{"kommune": "Oschatz"}'


def test_basis_ohne_database_url_endet_mit_exit_1(sk, monkeypatch, capsys):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: pytest.fail("darf nicht laufen"))
    assert sk.main(["--basis", "http://127.0.0.1:8010"]) == 1
    assert "DATABASE_URL" in capsys.readouterr().err


def test_ohne_basis_bleibt_sichtstart(sk, monkeypatch):
    gestartet = []

    class Prozess:
        returncode = 0

        def poll(self):
            return None

    monkeypatch.setattr(sk, "starte_sichtstart", lambda p: gestartet.append(p) or (Prozess(), object()))
    monkeypatch.setattr(sk, "warte_auf_health", lambda *a, **k: None)
    beendet = []
    monkeypatch.setattr(sk, "beende_sichtstart", lambda p, l: beendet.append(p))
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: {"kommune": "Oschatz"})
    assert sk.main([]) == 0
    assert len(gestartet) == 1 and len(beendet) == 1
    assert sk.ZIEL["basis"] == "http://127.0.0.1:8000"


def test_cookie_wird_gesendet(sk, monkeypatch):
    gesehen = []

    def urlopen(anfrage, timeout=0):
        gesehen.append(anfrage)
        return FakeAntwort({"ok": True})

    monkeypatch.setattr(sk.urllib.request, "urlopen", urlopen)
    sk.SITZUNG["wert"] = ATTRAPPE
    assert sk.api("GET", "/api/auth/me") == {"ok": True}
    assert gesehen[0].get_header("Cookie") == f"kap2_session={ATTRAPPE}"
    sk.SITZUNG["wert"] = None
    sk.api("GET", "/api/auth/me")
    assert gesehen[1].get_header("Cookie") is None


def test_sitzung_ablauf_widerruf_und_kein_schluessel_in_ausgabe(sk, monkeypatch, capsys):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    aufrufe = []
    _stubs_fuer_lauf(sk, monkeypatch, aufrufe)

    def arbeite(*_a, **_k):
        sk.melde(f"Antwort mit {ATTRAPPE} im Text")  # melde() muss verdecken
        raise sk.Fehler(f"HTTP 500: {ATTRAPPE}")  # die Fehlerausgabe auch

    monkeypatch.setattr(sk, "arbeite", arbeite)
    rc = sk.main(["--basis", "http://127.0.0.1:8010", "--anmeldung", "sitzung"])
    aus = capsys.readouterr()
    assert rc == 1
    assert ATTRAPPE not in aus.out + aus.err
    assert "***" in aus.out and "***" in aus.err
    arten = [a[0] for a in aufrufe]
    assert arten.index("anlegen") < arten.index("GET") < arten.index("widerrufen")
    widerruf = [a for a in aufrufe if a[0] == "widerrufen"][0]
    assert widerruf[1] == ()  # nie als Argument
    assert widerruf[2] == {sk.SITZUNG_ENV: ATTRAPPE}  # nur über die Umgebung


def test_erfolg_ausgabe_ohne_schluessel(sk, monkeypatch, capsys):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    _stubs_fuer_lauf(sk, monkeypatch, [])
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: {"hinweis": f"enthält {ATTRAPPE}"})
    assert sk.main(["--basis", "http://127.0.0.1:8010", "--anmeldung", "sitzung"]) == 0
    aus = capsys.readouterr()
    assert ATTRAPPE not in aus.out + aus.err
    assert "Sitzung widerrufen." in aus.out


def test_falscher_nutzer_bei_auth_me_bricht_ab(sk, monkeypatch, capsys):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    aufrufe = []
    me = {"authenticated": True, "user": {"email": "sichtpruefung-lokal@example.invalid", "role": "admin"}}
    _stubs_fuer_lauf(sk, monkeypatch, aufrufe, me=me)
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: pytest.fail("darf nicht laufen"))
    assert sk.main(["--basis", "http://127.0.0.1:8010", "--anmeldung", "sitzung"]) == 1
    err = capsys.readouterr().err
    assert "/api/auth/me" in err and ATTRAPPE not in err
    assert "widerrufen" in [a[0] for a in aufrufe]  # auch dann wird widerrufen


def test_gescheiterter_widerruf_ergibt_exit_1(sk, monkeypatch, capsys):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    _stubs_fuer_lauf(sk, monkeypatch, [], widerruf_ok=False)
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: {"kommune": "Oschatz"})
    rc = sk.main(["--basis", "http://127.0.0.1:8010", "--anmeldung", "sitzung"])
    aus = capsys.readouterr()
    assert rc == 1
    assert ATTRAPPE not in aus.out + aus.err
    assert "nicht widerrufen" in aus.err


def _status_folge(sk, monkeypatch, folge):
    """API-Attrappe für `bewertung`: Statusantworten der Reihe nach; hält die POSTs fest."""
    posts = []
    antworten = iter(folge)

    def api(methode, pfad, daten=None, timeout=0):
        if methode == "POST":
            posts.append(pfad)
            return {"message": "eingereiht"}
        if pfad.endswith("/status"):
            return next(antworten)
        pytest.fail(f"unerwartete Anfrage {methode} {pfad}")

    monkeypatch.setattr(sk, "api", api)
    return posts


def test_neu_rechnen_reiht_bei_done_neu_ein_und_wartet(sk, monkeypatch):
    alt = {"status": "done", "finished_at": "2026-10-08T10:00:00"}
    posts = _status_folge(sk, monkeypatch, [
        alt,  # Ausgangsstand
        alt,  # erste Abfrage nach dem Einreihen: noch der alte Stand, zählt nicht als fertig
        {"status": "running", "progress_pct": 40, "message": "Schritt"},
        {"status": "done", "finished_at": "2026-10-08T10:09:00"},
    ])
    status = sk.bewertung(1, 600, neu_rechnen=True)
    assert posts == ["/api/kommune/1/assess"]  # kein neues Raster
    assert status["finished_at"] == "2026-10-08T10:09:00"


def test_ohne_neu_rechnen_bleibt_done_unberuehrt(sk, monkeypatch):
    posts = _status_folge(sk, monkeypatch, [{"status": "done", "finished_at": "2026-10-08T10:00:00"}])
    assert sk.bewertung(1, 600)["status"] == "done"
    assert posts == []


def test_klimawirkungen_aus_risk_summary(sk):
    assert sk.baue_klimawirkungen(RISK_SUMMARY) == [
        {"bezeichnung": "Hitzebelastung (#95)", "betrag_eur_jahr": 179020.81},
        {"bezeichnung": "UV-bedingte Gesundheitsschädigungen (#98)", "betrag_eur_jahr": 13053.03},
        {"bezeichnung": "Allergische Reaktionen (#96)", "betrag_eur_jahr": 2280.6},
        {"bezeichnung": "Ohne Euro-Ebene", "betrag_eur_jahr": None},
    ]
    assert sk.baue_klimawirkungen({}) == []


def test_zeit_rechnung_utc_iso(sk):
    assert sk.zeit_utc("2026-10-08T10:45:59.866162") == "2026-10-08T10:45:59.866162+00:00"
    assert sk.zeit_utc("2026-10-08T12:45:59+02:00") == "2026-10-08T10:45:59+00:00"
    assert sk.zeit_utc(None) is None


def test_schlusszeile_von_arbeite(sk, monkeypatch):
    monkeypatch.setattr(sk, "fuelle_gemeinden", lambda: False)
    kommune = {"id": 7, "name": "Oschatz", "population": 3150}
    massnahme = {"id": 3, "name": "Sichtstart: Hitzeaktionspläne", "measure_type": "HEAT_ACTION_PLANS"}
    monkeypatch.setattr(sk, "finde_kommune", lambda: kommune)
    monkeypatch.setattr(sk, "produktcode", lambda *a, **k: "14730230")
    monkeypatch.setattr(sk, "bewertung", lambda *a, **k: {"status": "done", "finished_at": "2026-10-08T10:45:59"})
    monkeypatch.setattr(sk, "massnahme", lambda k: (massnahme, {"annual_benefit_eur": 10629.77}, "x", False))
    monkeypatch.setattr(sk, "betrag_95", lambda kid: (179020.8149, "Hitzebelastung (#95)"))

    def api(methode, pfad, daten=None, timeout=0):
        if pfad.endswith("/risk-summary"):
            return RISK_SUMMARY
        if pfad == "/api/health":
            return {"status": "ok", "commit": "abc"}
        if pfad.endswith("/measures"):
            return [massnahme, {"name": "Andere"}]
        if pfad.endswith("/impacts"):
            return [1, 2]
        return kommune

    monkeypatch.setattr(sk, "api", api)
    schluss = sk.arbeite(60, neu_rechnen=True)
    assert schluss["commit"] == "abc"
    assert schluss["zeit_rechnung"] == "2026-10-08T10:45:59+00:00"
    assert schluss["massnahmen_mit_praefix"] == 1
    assert [k["betrag_eur_jahr"] for k in schluss["klimawirkungen"]] == [179020.81, 13053.03, 2280.6, None]
    json.dumps(schluss)


def test_tabelle_und_vorgabe(sk):
    assert sk.KOMMUNEN["Oschatz"]["ags"] == "14730230" and sk.KOMMUNEN["Leipzig"]["ags"] == "14713000"
    assert {k["bundesland"] for k in sk.KOMMUNEN.values()} == {"Sachsen"}
    assert sk.gewaehlt()[0] == "Oschatz"


def test_kommune_waehlbar(sk, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    _stubs_fuer_lauf(sk, monkeypatch, [])
    monkeypatch.setattr(sk, "arbeite", lambda *a, **k: {"kommune": sk.gewaehlt()[0]})
    assert sk.main(["--basis", "http://127.0.0.1:8010", "--kommune", "Leipzig"]) == 0
    assert sk.gewaehlt() == ("Leipzig", sk.KOMMUNEN["Leipzig"])


def test_import_fuer_sachsen_wenn_schluessel_fehlt(sk, monkeypatch):
    aufrufe = []

    def produktcode(code, *argumente, **_k):
        aufrufe.append(argumente)
        return json.dumps({"vorher": 964, "da_vorher": False, "geschrieben": 418,
                           "nachher": 1382, "da_nachher": True})

    monkeypatch.setattr(sk, "produktcode", produktcode)
    assert sk.fuelle_gemeinden() is True
    assert aufrufe == [("14730230", "Sachsen")]


def _stubs_arbeite(sk, monkeypatch, ags_worker):
    kommune = {"id": 7, "name": "Oschatz", "population": 14000}
    monkeypatch.setattr(sk, "fuelle_gemeinden", lambda: False)
    monkeypatch.setattr(sk, "finde_kommune", lambda: kommune)
    monkeypatch.setattr(sk, "produktcode", lambda *a, **k: ags_worker)
    monkeypatch.setattr(sk, "bewertung", lambda *a, **k: pytest.fail("darf nicht laufen"))


def test_falscher_schluessel_bricht_mit_exit_1_ab(sk, monkeypatch, capsys):
    monkeypatch.setenv("DATABASE_URL", "postgresql://dienst@/ziel")
    _stubs_fuer_lauf(sk, monkeypatch, [])
    _stubs_arbeite(sk, monkeypatch, "14713000")  # Leipzig statt Oschatz
    assert sk.main(["--basis", "http://127.0.0.1:8010"]) == 1
    err = capsys.readouterr().err
    assert "14713000" in err and "14730230" in err


def test_herzschlag_bei_unveraenderter_bewertung(sk, monkeypatch, capsys):
    uhr = {"t": 1000.0}
    monkeypatch.setattr(sk.time, "time", lambda: uhr["t"])
    monkeypatch.setattr(sk.time, "sleep", lambda s: uhr.__setitem__("t", uhr["t"] + s))
    laufend = {"status": "running", "progress_pct": 95, "message": "Risikokomposition"}
    fertig = {"status": "done", "finished_at": "2026-10-09T10:00:00"}

    def api(methode, pfad, daten=None, timeout=0):
        if pfad.endswith("/status"):
            return laufend if uhr["t"] - 1000.0 < 200 else fertig
        pytest.fail(f"unerwartete Anfrage {methode} {pfad}")

    monkeypatch.setattr(sk, "api", api)
    status = sk.bewertung(1, 600)
    zeilen = [z for z in capsys.readouterr().out.splitlines() if "Risikokomposition" in z]
    assert len(zeilen) >= 3  # erste Meldung plus mindestens zwei Herzschläge in 200 s
    assert status["dauer_bewertung_s"] >= 200


def test_schlusszeile_traegt_dauer_bewertung(sk, monkeypatch):
    kommune = {"id": 7, "name": "Oschatz", "population": 14000}
    monkeypatch.setattr(sk, "fuelle_gemeinden", lambda: False)
    monkeypatch.setattr(sk, "finde_kommune", lambda: kommune)
    monkeypatch.setattr(sk, "produktcode", lambda *a, **k: "14730230")
    monkeypatch.setattr(sk, "bewertung", lambda *a, **k: {"status": "done", "dauer_bewertung_s": 412})
    massnahme = {"id": 3, "name": "Sichtstart: X", "measure_type": "X"}
    monkeypatch.setattr(sk, "massnahme", lambda k: (massnahme, {"annual_benefit_eur": 1.0}, "x", False))
    monkeypatch.setattr(sk, "betrag_95", lambda kid: (1.0, "Hitzebelastung (#95)"))
    monkeypatch.setattr(sk, "api", lambda m, p, d=None, timeout=0:
                        RISK_SUMMARY if p.endswith("/risk-summary") else
                        {"commit": "abc"} if p == "/api/health" else
                        [] if p.endswith(("/measures", "/impacts")) else kommune)
    assert sk.arbeite(60)["dauer_bewertung_s"] == 412

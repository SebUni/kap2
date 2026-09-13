"""Tests für T-0199: Die enge polkit-Regel liegt bereit, die aktive Abweichung ist dokumentiert.

Anlass: Der Aufsichtsrat hat die Berechtigung am 12.09.2026 selbst am Server gesetzt (T-0165) und
dabei gemeldet, dass der Server polkit 0.105 fährt (keine JavaScript-`.rules`-Dateien). Die dort
aktive `.pkla`-Regel kann nicht auf eine Unit eingeschränkt werden und öffnet dem Benutzer
`overlord` alle systemd-Einheiten — weiter als geplant. Dieser Test prüft, dass die enge
`.rules`-Fassung für eine spätere polkit-Fassung bereitliegt, die heute aktive `.pkla`-Fassung
abgebildet ist und die Abweichung in `deploy/README.md` dokumentiert steht.
"""

from __future__ import annotations

from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
RULES = WURZEL / "deploy" / "polkit-kap2-test.rules"
PKLA = WURZEL / "deploy" / "polkit-kap2-test.pkla"
README = WURZEL / "deploy" / "README.md"


def test_rules_datei_existiert_und_hat_genau_eine_regel():
    text = RULES.read_text(encoding="utf-8")
    assert text.count("polkit.addRule(") == 1


def test_rules_datei_gibt_yes_nur_bei_allen_drei_bedingungen():
    text = RULES.read_text(encoding="utf-8")
    assert 'action.id === "org.freedesktop.systemd1.manage-units"' in text
    assert 'action.lookup("unit") === "kap2-test.service"' in text
    assert 'subject.user === "overlord"' in text
    assert "polkit.Result.YES" in text


def test_pkla_datei_existiert_und_hat_kommentar_ueber_fehlende_einschraenkbarkeit():
    text = PKLA.read_text(encoding="utf-8")
    erste_zeile = text.splitlines()[0]
    assert erste_zeile.startswith("#")
    assert "nicht" in erste_zeile.lower()
    assert "einheit" in erste_zeile.lower() or "unit" in erste_zeile.lower()
    assert "Identity=unix-user:overlord" in text
    assert "Action=org.freedesktop.systemd1.manage-units" in text


def test_readme_enthaelt_abschnitt_berechtigung_fuer_den_dienstneustart():
    text = README.read_text(encoding="utf-8")
    assert "## Berechtigung für den Dienstneustart" in text
    abschnitt = text[text.index("## Berechtigung für den Dienstneustart"):]
    assert "/etc/polkit-1/rules.d/50-kap2-test.rules" in abschnitt
    assert "/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla" in abschnitt
    assert "dpkg -s policykit-1 | grep Version" in abschnitt
    assert "alle" in abschnitt
    assert "systemd-Einheiten" in abschnitt
    assert "nächsten Betriebssystem-Sprung" in abschnitt

"""Gemeinsames Setup für die ganze Test-Suite (T-0590).

Hängt die Ersatzmodule für fehlende Schwergewichte (``_stub_heavy_deps``)
**einmal**, vor dem Einsammeln der Testmodule, ein. Vorher riefen einzelne
Testdateien ``_stub_heavy_deps.install()`` selbst auf; welche Datei zuerst
lief, entschied damit zufällig darüber, ob der ``_FallbackFinder`` schon in
``sys.meta_path`` hing, wenn eine andere, von ``_stub_heavy_deps`` unabhängige
Testdatei (z. B. ``test_mandantentrennung.py``) importierte — Tests liefen
dadurch allein anders als in der vollen Suite. Ein globaler Aufruf hier macht
das Verhalten unabhängig von der Reihenfolge der Testdateien.
"""

from __future__ import annotations

import _stub_heavy_deps

_stub_heavy_deps.install()

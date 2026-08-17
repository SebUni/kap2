"""Auslieferung vorgebauter gzip-JSON-Dateien mit ETag/If-None-Match (304).

Starlette-``FileResponse`` SETZT zwar ETag/Last-Modified (aus stat), wertet
``If-None-Match`` aber nicht aus — der 304-Vergleich passiert deshalb hier.
``Cache-Control: no-cache`` heißt: Der Browser revalidiert bei jedem Zugriff
(Invalidierung ist serverseitig), spart über 304 aber den kompletten
Body-Transfer. ``X-Uncompressed-Length`` erlaubt dem Frontend eine echte
Fortschrittsanzeige beim Dekomprimieren.
"""

from __future__ import annotations

import os
import struct

from fastapi import Request
from fastapi.responses import FileResponse, Response


def gzip_uncompressed_size(path: str) -> int:
    """Liest die unkomprimierte Groesse aus dem gzip-Trailer (ISIZE, mod 2^32)."""
    with open(path, "rb") as fh:
        fh.seek(-4, os.SEEK_END)
        return struct.unpack("<I", fh.read(4))[0]


def file_etag(path: str) -> str:
    """ETag aus mtime+Groesse — für Dateien ohne inhaltlichen Fingerprint."""
    st = os.stat(path)
    return f'"f-{st.st_mtime_ns}-{st.st_size}"'


def _etag_matches(if_none_match: str, etag: str) -> bool:
    candidates = [t.strip() for t in if_none_match.split(",")]
    return "*" in candidates or etag in candidates or f"W/{etag}" in candidates


def gzip_json_file_response(request: Request | None, path: str, *, etag: str,
                            download_name: str) -> Response:
    """Streamt eine gzip-JSON-Datei; 304 bei passendem ``If-None-Match``."""
    inm = request.headers.get("if-none-match") if request is not None else None
    if inm and _etag_matches(inm, etag):
        return Response(status_code=304, headers={"ETag": etag, "Cache-Control": "no-cache"})
    headers = {"Content-Encoding": "gzip", "Cache-Control": "no-cache", "ETag": etag}
    try:
        headers["X-Uncompressed-Length"] = str(gzip_uncompressed_size(path))
    except Exception:
        pass
    return FileResponse(
        path,
        media_type="application/json",
        headers=headers,
        filename=download_name,
    )

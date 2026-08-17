"""Statische SEO-Seiten je Gemeinde + Sitemap (programmatic SEO, Plan §Phase H).

Reines Python-String-Rendering (keine Jinja2-Abhängigkeit). Erzeugt pro
Gemeinde eine eigenständige HTML-Seite mit Titel/Meta/JSON-LD und den 8
Risiken samt Vergleich zu Bundesland/Deutschland, dazu eine ``sitemap.xml``
und ``robots.txt``. Die lokalen Treiberwerte im Fließtext machen jede Seite
faktisch einzigartig (kein Duplicate-Content).
"""
from __future__ import annotations

import html
import logging
import os
from collections import defaultdict

from sqlalchemy.orm import Session

from app.config import settings
from app.data import catalog
from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.services.lite.lite_scoring import LITE_RISK_CODES

log = logging.getLogger(__name__)

PUBLIC_BASE = os.environ.get("KAP2_PUBLIC_BASE", "https://kap2.example.de")


def _slug(s: str) -> str:
    s = (s or "").lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), (" ", "-"),
                 ("/", "-"), (".", ""), (",", "")]:
        s = s.replace(a, b)
    return "".join(c for c in s if c.isalnum() or c == "-")


def _pages_dir() -> str:
    return os.path.join(settings.LITE_DATA_DIR, "pages")


def _level(index: float) -> str:
    return "hoch" if index >= 66 else "mittel" if index >= 33 else "gering"


def _render_page(g: Gemeinde, rows: list[GemeindeLiteResult],
                 bl_means: dict, de_means: dict) -> str:
    name = html.escape(g.name)
    bl = html.escape(g.bundesland or "")
    title = f"Klimarisiken in {name} ({bl}) – KAP2"
    desc = (f"Klimarisiken in {name}: Hitze, Starkregen und Dürre auf einen Blick – "
            f"Index und erwartete Schäden in Euro. Grobschätzung je Gemeinde.")
    risk_rows = []
    for r in rows:
        cat = catalog.RISKS_BY_CODE.get(r.risk_code, {})
        blm = bl_means.get(r.risk_code, {}).get(g.bundesland)
        dem = de_means.get(r.risk_code)
        risk_rows.append(
            f"<tr><td>{html.escape(cat.get('name', r.risk_code))}</td>"
            f"<td><b>{r.index_value:.0f}</b> ({_level(r.index_value)})</td>"
            f"<td>{r.outcome_value:.1f} {html.escape(r.outcome_unit or '')}</td>"
            f"<td>{blm:.0f}</td><td>{dem:.0f}</td></tr>"
            if blm is not None and dem is not None else
            f"<tr><td>{html.escape(cat.get('name', r.risk_code))}</td>"
            f"<td><b>{r.index_value:.0f}</b> ({_level(r.index_value)})</td>"
            f"<td>{r.outcome_value:.1f} {html.escape(r.outcome_unit or '')}</td>"
            f"<td>–</td><td>–</td></tr>")
    ags = g.ags
    jsonld = (
        '{"@context":"https://schema.org","@type":"Place",'
        f'"name":"{name}","address":{{"@type":"PostalAddress",'
        f'"addressRegion":"{bl}","addressCountry":"DE"}}}}')
    return f"""<!doctype html>
<html lang="de"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{PUBLIC_BASE}/klimarisiken/{_slug(g.bundesland or '')}/{_slug(g.name)}-{ags}">
<script type="application/ld+json">{jsonld}</script>
<style>body{{font-family:system-ui,sans-serif;max-width:820px;margin:0 auto;padding:1.5rem;color:#1e293b}}
h1{{font-size:1.6rem}}table{{width:100%;border-collapse:collapse;margin:1rem 0}}
th,td{{text-align:left;padding:.5rem;border-bottom:1px solid #e2e8f0;font-size:.9rem}}
th{{background:#f5f7fa}}.cta{{display:inline-block;background:#2563eb;color:#fff;padding:.6rem 1rem;border-radius:8px;text-decoration:none;margin:.3rem .3rem 0 0}}
.muted{{color:#64748b;font-size:.85rem}}</style>
</head><body>
<h1>Klimarisiken in {name}</h1>
<p class="muted">{bl} · {g.population or '–'} Einwohner · {g.area_km2:.0f} km² · Grobschätzung auf Gemeindeebene</p>
<table><thead><tr><th>Risiko</th><th>Index (0–100)</th><th>Erwartet</th><th>Ø {bl}</th><th>Ø DE</th></tr></thead>
<tbody>{''.join(risk_rows)}</tbody></table>
<p>Diese Werte entstehen aus deutschlandweiten Klimadaten (DWD), der Bevölkerungs-
und Gebäudestruktur (Zensus 2022) und der Sozioökonomie (INKAR) – als bewusst
grobe Schätzung je Gemeinde. Die räumlich genaue Analyse auf dem 100-Meter-Raster
liefert das KAP2-Hauptprodukt.</p>
<a class="cta" href="{PUBLIC_BASE}/deutschland?ags={ags}">Interaktiv erkunden</a>
<a class="cta" href="{PUBLIC_BASE}/demo">Detailanalyse: Demo</a>
<a class="cta" href="{PUBLIC_BASE}/kontakt" style="background:#fff;color:#2563eb;border:1px solid #2563eb">Beratungsgespräch</a>
<p class="muted" style="margin-top:2rem">Alle Gemeinden in {bl}:
<a href="{PUBLIC_BASE}/klimarisiken/{_slug(g.bundesland or '')}">Übersicht</a> ·
Methodik: <a href="{PUBLIC_BASE}/studie">KAP2-Deutschlandstudie</a></p>
</body></html>"""


def generate(db: Session, bl_means: dict | None = None) -> int:
    """Rendert alle Gemeinde-Seiten + Sitemap. Gibt die Seitenzahl zurück."""
    from app.services.lite import study_service
    gem = db.query(Gemeinde).all()
    results = db.query(GemeindeLiteResult).all()
    by_ags: dict[str, list] = defaultdict(list)
    for r in results:
        by_ags[r.ags].append(r)

    # Bundesland-/DE-Mittel je Risiko
    if bl_means is None:
        bl_means = study_service.build_study(db)["bundesland_means"]
    de_means: dict[str, float] = {}
    for code in LITE_RISK_CODES:
        vals = [r.index_value for r in results if r.risk_code == code and r.index_value is not None]
        de_means[code] = round(sum(vals) / len(vals), 1) if vals else 0.0

    pages = 0
    urls = []
    for g in gem:
        rows = sorted(by_ags.get(g.ags, []),
                      key=lambda r: LITE_RISK_CODES.index(r.risk_code)
                      if r.risk_code in LITE_RISK_CODES else 99)
        if not rows:
            continue
        bl_slug = _slug(g.bundesland or "unbekannt")
        d = os.path.join(_pages_dir(), bl_slug)
        os.makedirs(d, exist_ok=True)
        fname = f"{_slug(g.name)}-{g.ags}.html"
        with open(os.path.join(d, fname), "w", encoding="utf-8") as fh:
            fh.write(_render_page(g, rows, bl_means, de_means))
        urls.append(f"{PUBLIC_BASE}/klimarisiken/{bl_slug}/{_slug(g.name)}-{g.ags}")
        pages += 1

    _write_sitemap(urls)
    _write_robots()
    log.info("SEO: %d Gemeinde-Seiten + Sitemap", pages)
    return pages


def _write_sitemap(urls: list[str]) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"<url><loc>{html.escape(u)}</loc></url>")
    lines.append("</urlset>")
    with open(os.path.join(settings.LITE_DATA_DIR, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def _write_robots() -> None:
    content = (f"User-agent: *\nAllow: /klimarisiken/\nAllow: /studie\n"
               f"Disallow: /app\nDisallow: /admin\nDisallow: /demo\n"
               f"Sitemap: {PUBLIC_BASE}/sitemap.xml\n")
    with open(os.path.join(settings.LITE_DATA_DIR, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(content)

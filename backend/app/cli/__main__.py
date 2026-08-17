"""CLI entry point: python -m app.cli zensus-download [--keys ...] | create-admin"""

from __future__ import annotations

import argparse
import getpass
import sys

from app.services.zensus_loader import ZENSUS_DATASETS, ensure_zensus_datasets


def cmd_create_admin(args: argparse.Namespace) -> int:
    """Ersten (oder weiteren) Admin-Account anlegen bzw. Passwort setzen."""
    from app.db.database import Base, SessionLocal, engine
    import app.models.models  # noqa: F401
    import app.models.auth_models  # noqa: F401
    from app.models.auth_models import ROLE_ADMIN, User
    from app.services.auth_service import hash_password

    Base.metadata.create_all(bind=engine)

    email = args.email.strip().lower()
    password = args.password or getpass.getpass("Passwort: ")
    if len(password) < 8:
        print("Passwort muss mindestens 8 Zeichen haben", file=sys.stderr)
        return 1

    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.password_hash = hash_password(password)
            user.role = ROLE_ADMIN
            user.is_active = True
            action = "aktualisiert (Rolle admin, neues Passwort)"
        else:
            user = User(
                email=email,
                password_hash=hash_password(password),
                display_name=args.name or email.split("@")[0],
                role=ROLE_ADMIN,
                is_active=True,
            )
            db.add(user)
            action = "angelegt"
        db.commit()
        print(f"Admin {email} {action}")
    return 0


def cmd_finance_budget_import(args: argparse.Namespace) -> int:
    """Bulk-Import der Gemeindefinanzen (Regionalstatistik 71717 → Chip-Store).

    Selbstheilend: übernimmt neuen Stand nur bei erfolgreicher Validierung, sonst
    bleibt der alte erhalten. Für den Cron-Einsatz s. scripts.import_finance_budget.
    """
    import logging
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    from app.services import finance_bulk
    from app.config import settings
    if not settings.REGIONALSTATISTIK_BUDGET_ENABLED:
        print("REGIONALSTATISTIK_BUDGET_ENABLED=False — nichts zu tun.", file=sys.stderr)
        return 1
    return 0 if finance_bulk.run_import() else 1


def cmd_zensus_download(args: argparse.Namespace) -> int:
    keys = args.keys.split(",") if args.keys else None
    if keys:
        unknown = [k for k in keys if k not in ZENSUS_DATASETS]
        if unknown:
            print(f"Unbekannte Keys: {', '.join(unknown)}", file=sys.stderr)
            print(f"Verfügbar: {', '.join(sorted(ZENSUS_DATASETS))}", file=sys.stderr)
            return 1
    paths = ensure_zensus_datasets(keys)
    for p in paths:
        print(p)
    return 0


def cmd_lod2_prefetch(args: argparse.Namespace) -> int:
    """LoD2-Kacheln für eine bbox oder Kommune vorab laden und cachen.

    bbox-Format wie Overpass: "s,w,n,e" (WGS84). Alternativ --ags: bbox aus
    der Gemeindegeometrie (Tabelle ``gemeinden``).
    """
    import logging
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    from app.config import settings
    from app.services.geodata.lod2.loader import fetch_lod2_buildings
    from app.services.geodata.lod2.sources import LOD2_SOURCES

    src = LOD2_SOURCES.get(args.bundesland)
    if src is None:
        print(f"Unbekanntes Bundesland: {args.bundesland}", file=sys.stderr)
        print(f"Verfügbar: {', '.join(sorted(LOD2_SOURCES))}", file=sys.stderr)
        return 1
    if src.phase != 1:
        print(f"{args.bundesland}: noch kein Direkt-Adapter (Phase 2) — "
              f"Einstieg: {src.note}", file=sys.stderr)
        return 1

    bbox = args.bbox
    if not bbox and args.ags:
        from geoalchemy2.shape import to_shape
        from app.db.database import SessionLocal
        from app.models.lite_models import Gemeinde
        with SessionLocal() as db:
            gem = db.get(Gemeinde, args.ags)
            if gem is None or gem.geometry is None:
                print(f"AGS {args.ags} nicht gefunden", file=sys.stderr)
                return 1
            w, s, e, n = to_shape(gem.geometry).bounds
            bbox = f"{s},{w},{n},{e}"
            print(f"{gem.name} ({args.ags}): bbox {bbox}")
    if not bbox:
        print("--bbox oder --ags erforderlich", file=sys.stderr)
        return 1

    buildings = fetch_lod2_buildings(bbox, args.bundesland,
                                     keep_raw=args.keep_raw)
    if buildings is None:
        print("LoD2-Abruf fehlgeschlagen (siehe Log) — kein Cache geschrieben",
              file=sys.stderr)
        return 1
    heights = [b["height"] for b in buildings]
    print(f"{len(buildings)} Gebäude geladen"
          + (f", Höhe min/median/max = {min(heights):.1f}/"
             f"{sorted(heights)[len(heights) // 2]:.1f}/{max(heights):.1f} m"
             if heights else ""))
    print(f"Cache: {settings.LOD2_CACHE_DIR}/extracted/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="app.cli", description="KAP2 administration CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    dl = sub.add_parser("zensus-download", help="Zensus 2022 CSVs herunterladen/extrahieren")
    dl.add_argument(
        "--keys",
        help="Kommagetrennte Dataset-Keys (Default: alle Pflicht-Themen)",
    )
    dl.set_defaults(func=cmd_zensus_download)

    fb = sub.add_parser("finance-budget-import",
                        help="Gemeindefinanzen (Regionalstatistik 71717) in den Chip-Store importieren")
    fb.set_defaults(func=cmd_finance_budget_import)

    ca = sub.add_parser("create-admin", help="Admin-Account anlegen / Passwort setzen")
    ca.add_argument("email", help="E-Mail-Adresse des Admins")
    ca.add_argument("--password", help="Passwort (sonst interaktive Abfrage)")
    ca.add_argument("--name", help="Anzeigename")
    ca.set_defaults(func=cmd_create_admin)

    lp = sub.add_parser("lod2-prefetch",
                        help="LoD2-Gebäudekacheln (amtliche 3D-Modelle) vorab laden")
    lp.add_argument("--bundesland", required=True,
                    help='z. B. "Nordrhein-Westfalen"')
    lp.add_argument("--bbox", help='WGS84-bbox "s,w,n,e" (Overpass-Format)')
    lp.add_argument("--ags", help="Amtlicher Gemeindeschlüssel (bbox aus DB)")
    lp.add_argument("--keep-raw", action="store_true",
                    help="Roh-GML/-ZIP zusätzlich unter data/lod2/raw/ behalten")
    lp.set_defaults(func=cmd_lod2_prefetch)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

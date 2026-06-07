"""CLI entry point: python -m app.cli zensus-download [--keys ...]"""

from __future__ import annotations

import argparse
import sys

from app.services.zensus_loader import ZENSUS_DATASETS, ensure_zensus_datasets


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


def main() -> int:
    parser = argparse.ArgumentParser(prog="app.cli", description="KAP2 administration CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    dl = sub.add_parser("zensus-download", help="Zensus 2022 CSVs herunterladen/extrahieren")
    dl.add_argument(
        "--keys",
        help="Kommagetrennte Dataset-Keys (Default: alle Pflicht-Themen)",
    )
    dl.set_defaults(func=cmd_zensus_download)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

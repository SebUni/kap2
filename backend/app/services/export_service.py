"""Excel export and import for adaptation measures."""

import io
from typing import BinaryIO

from geoalchemy2.shape import to_shape, from_shape
from openpyxl import Workbook, load_workbook
from shapely import wkt
from sqlalchemy.orm import Session

from app.models.models import AdaptationMeasure, MeasureImpact


def export_measures_xlsx(db: Session, kommune_id: int) -> bytes:
    """Export all measures for a kommune as an Excel file.

    Returns xlsx bytes ready for download.
    """
    measures = (
        db.query(AdaptationMeasure)
        .filter(AdaptationMeasure.kommune_id == kommune_id)
        .all()
    )

    wb = Workbook()

    # ── Sheet 1: Measures ──
    ws = wb.active
    ws.title = "Maßnahmen"
    headers = [
        "ID", "Name", "Typ", "Umsetzungsjahr", "Beschreibung",
        "Konfiguration", "Geometrie (WKT)",
        "Kosten (Invest.)", "Kosten (jährl.)", "Einsparungen (jährl.)",
        "ΔTemperatur (Σ)", "ΔHitzeindex (Σ)",
    ]
    ws.append(headers)

    for m in measures:
        geom_wkt = ""
        if m.geometry is not None:
            shape = to_shape(m.geometry)
            geom_wkt = shape.wkt

        # Aggregate impacts
        impacts = db.query(MeasureImpact).filter(MeasureImpact.measure_id == m.id).all()
        total_invest = sum(imp.costs.get("investment", 0) for imp in impacts)
        total_maint = sum(imp.costs.get("annual_maintenance", 0) for imp in impacts)
        total_savings = sum(
            sum(v for v in imp.savings.values()) for imp in impacts
        )
        total_dt = sum(imp.indicator_deltas.get("temperature_estimate", 0) for imp in impacts)
        total_dhi = sum(imp.indicator_deltas.get("heat_stress_index", 0) for imp in impacts)

        import json
        config_str = json.dumps(m.config or {}, ensure_ascii=False)

        ws.append([
            m.id,
            m.name,
            m.measure_type,
            m.implementation_year,
            m.description or "",
            config_str,
            geom_wkt,
            round(total_invest, 2),
            round(total_maint, 2),
            round(total_savings, 2),
            round(total_dt, 2),
            round(total_dhi, 2),
        ])

    # ── Sheet 2: Summary ──
    ws2 = wb.create_sheet("Zusammenfassung")
    ws2.append(["Kennzahl", "Wert"])
    ws2.append(["Anzahl Maßnahmen", len(measures)])
    ws2.append(["Gesamtinvestition (€)", sum(
        sum(imp.costs.get("investment", 0)
            for imp in db.query(MeasureImpact).filter(MeasureImpact.measure_id == m.id).all())
        for m in measures
    )])

    # Auto-width
    for ws_sheet in [ws, ws2]:
        for col in ws_sheet.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws_sheet.column_dimensions[col[0].column_letter].width = min(max_len + 2, 50)

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def import_measures_xlsx(db: Session, kommune_id: int, file: BinaryIO) -> dict:
    """Import measures from an Excel file.

    Expected format: same as export (Sheet 'Maßnahmen' with columns matching export).
    Returns summary of imported/skipped rows.
    """
    import json

    wb = load_workbook(file, read_only=True)
    ws = wb["Maßnahmen"]

    rows = list(ws.iter_rows(min_row=2, values_only=True))
    imported = 0
    skipped = 0
    errors = []

    for i, row in enumerate(rows, start=2):
        try:
            if len(row) < 7:
                errors.append(f"Zeile {i}: Zu wenige Spalten")
                skipped += 1
                continue

            _id, name, mtype, impl_year, desc, config_str, geom_wkt = row[:7]

            if not name or not mtype:
                errors.append(f"Zeile {i}: Name oder Typ fehlt")
                skipped += 1
                continue

            # Parse geometry
            if geom_wkt:
                shape = wkt.loads(geom_wkt)
                geom = from_shape(shape, srid=4326)
            else:
                errors.append(f"Zeile {i}: Keine Geometrie")
                skipped += 1
                continue

            # Parse config
            try:
                config = json.loads(config_str) if config_str else {}
            except (json.JSONDecodeError, TypeError):
                config = {}

            measure = AdaptationMeasure(
                kommune_id=kommune_id,
                name=str(name),
                measure_type=str(mtype),
                geometry=geom,
                config=config,
                implementation_year=int(impl_year) if impl_year else None,
                description=str(desc) if desc else None,
            )
            db.add(measure)
            imported += 1

        except Exception as e:
            errors.append(f"Zeile {i}: {str(e)[:200]}")
            skipped += 1

    db.commit()
    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors[:20],  # Limit error messages
    }

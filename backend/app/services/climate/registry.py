from app.services.climate.base import ClimateAssessor


_registry: dict[str, ClimateAssessor] = {}


def register(assessor: ClimateAssessor) -> None:
    _registry[assessor.climate_type] = assessor


def get_assessor(climate_type: str) -> ClimateAssessor | None:
    return _registry.get(climate_type)


def list_assessors() -> list[dict]:
    return [
        {
            "climate_type": a.climate_type,
            "label": a.label,
            "max_level": a.max_level,
            "indicators": [
                {"key": i.key, "label": i.label, "unit": i.unit, "description": i.description}
                for i in a.get_indicators()
            ],
        }
        for a in _registry.values()
    ]


def _auto_discover():
    """Import all known assessor modules so they self-register."""
    # Each assessor module calls register() at import time
    from app.services.climate.heat import assessor as _  # noqa: F401
    from app.services.climate.heavy_rain import assessor as _hr  # noqa: F401
    from app.services.climate.river_flood import assessor as _rf  # noqa: F401
    from app.services.climate.drought import assessor as _dr  # noqa: F401
    from app.services.climate.forest_fire import assessor as _ff  # noqa: F401
    from app.services.climate.agriculture import assessor as _ag  # noqa: F401
    from app.services.climate.storms import assessor as _st  # noqa: F401
    from app.services.climate.sea_level import assessor as _sl  # noqa: F401


_auto_discover()

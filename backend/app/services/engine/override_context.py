"""Kommune-spezifische Parameter-Overrides für die Berechnungs-Engine."""

from __future__ import annotations

from typing import Any

from app.data import catalog

_overrides: dict[str, Any] = {}


def set_overrides(overrides: dict[str, Any] | None) -> None:
    global _overrides
    _overrides = dict(overrides or {})


def get_override(parameter_id: str, default: Any = None) -> Any:
    return _overrides.get(parameter_id, default)


def effective_ref_value(risk_code: str, default: float) -> float:
    val = get_override(f"risks.{risk_code}.ref_value")
    return float(val) if val is not None else default


def effective_norm_bounds(code: str) -> tuple[float, float]:
    cat = None
    if code in catalog.HAZARDS_BY_CODE:
        cat = "hazards"
    elif code in catalog.EXPOSURES_BY_CODE:
        cat = "exposures"
    elif code in catalog.VULNERABILITIES_BY_CODE:
        cat = "vulnerabilities"
    meta = catalog.INDICATOR_BY_CODE.get(code, {})
    lo = float(meta.get("norm_min", 0.0))
    hi = float(meta.get("norm_max", 1.0))
    if cat:
        lo_ov = get_override(f"{cat}.{code}.norm_min")
        hi_ov = get_override(f"{cat}.{code}.norm_max")
        if lo_ov is not None:
            lo = float(lo_ov)
        if hi_ov is not None:
            hi = float(hi_ov)
    return lo, hi


def normalize_value(code: str, value: float) -> float:
    lo, hi = effective_norm_bounds(code)
    if hi <= lo:
        return 0.0
    x = (float(value) - lo) / (hi - lo)
    return max(0.0, min(1.0, x))


def uhi_coefficients() -> dict[str, float]:
    return {
        "alpha": float(get_override("uhi.alpha", 6.0)),
        "beta": float(get_override("uhi.beta", 2.0)),
        "gamma": float(get_override("uhi.gamma", 3.5)),
        "delta": float(get_override("uhi.delta", 2.0)),
    }

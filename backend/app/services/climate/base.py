from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class IndicatorDef:
    key: str
    label: str
    unit: str
    description: str
    min_value: float = 0.0
    max_value: float = 100.0


@dataclass
class ConfigParamDef:
    category: str
    key: str
    default_value: Any
    description: str
    value_type: str = "float"  # float, int, str, bool


@dataclass
class CellResult:
    grid_cell_id: int
    indicators: dict[str, float]
    risk_score: float = 0.0  # normalised 0–10


class ClimateAssessor(ABC):
    """Abstract base class for climate impact assessors.

    To add a new climate type, subclass this and register it with the registry.
    """

    climate_type: str = ""
    label: str = ""
    max_level: int = 1

    @abstractmethod
    def assess(
        self,
        kommune_id: int,
        level: int,
        grid_cells: list[dict],
        config_params: dict[str, Any],
        progress_callback: Any = None,
    ) -> list[CellResult]:
        ...

    @abstractmethod
    def get_required_config(self) -> list[ConfigParamDef]:
        ...

    @abstractmethod
    def get_indicators(self) -> list[IndicatorDef]:
        ...

    def get_projection_factors(self, bundesland: str) -> dict:
        """Return per-year scaling factors for risk projection (2025–2065).

        Default implementation returns linear +30 % by 2065 for RCP 4.5
        and +80 % for RCP 8.5.  Subclasses can override with real data.
        """
        factors: dict[str, dict[int, float]] = {"rcp45": {}, "rcp85": {}}
        for y in range(2025, 2066):
            t = (y - 2025) / 40.0
            factors["rcp45"][y] = 1.0 + 0.30 * t  # +30 % by 2065
            factors["rcp85"][y] = 1.0 + 0.80 * t  # +80 % by 2065
        return factors

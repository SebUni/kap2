"""Schlanke Ersatzmodule für die schweren Laufzeit-Abhängigkeiten (T-0481).

Hintergrund: Export und KI-Kontext hängen über ``app.models.models`` an
SQLAlchemy/GeoAlchemy und über den Excel-Export an openpyxl. Diese Pakete sind
in der Prüf-/Entwicklungsumgebung nicht installiert (dort läuft nur die
Standardbibliothek), im Deploy-Venv dagegen schon.

``install()`` legt deshalb **nur dann** Ersatzmodule in ``sys.modules``, wenn das
echte Paket fehlt. Ist es vorhanden, passiert nichts und der Test läuft gegen die
echte Bibliothek. Die Ersatzmodule bilden ausschließlich ab, was zum Importieren
der Modelle und der beiden Service-Module nötig ist — sie ersetzen keine
Datenbank und werden nirgends im Produktivcode verwendet.
"""

from __future__ import annotations

import importlib.util
import sys
import types


def _missing(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is None
    except (ImportError, ValueError):
        return True


def _module(name: str) -> types.ModuleType:
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    parent, _, child = name.rpartition(".")
    if parent:
        setattr(sys.modules[parent], child, mod)
    return mod


class _Anything:
    """Platzhalter, der jeden Aufruf und jeden Attributzugriff verträgt."""

    def __init__(self, *a, **k):
        pass

    def __call__(self, *a, **k):
        return _Anything()

    def __getattr__(self, item):
        return _Anything()


def _install_sqlalchemy() -> None:
    sa = _module("sqlalchemy")
    for name in ("BigInteger", "Boolean", "Column", "Integer", "String", "Float",
                 "DateTime", "Enum", "ForeignKey", "JSON", "Text",
                 "UniqueConstraint", "Index", "case", "literal", "func",
                 "select", "text", "create_engine", "and_", "or_", "desc", "asc"):
        setattr(sa, name, _Anything())

    orm = _module("sqlalchemy.orm")

    class _DeclarativeBase:
        """Modelle werden im Test nur als Datenträger instanziiert."""

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def __getattr__(self, item):  # nicht gesetzte Spalten sind leer
            if item.startswith("_"):
                raise AttributeError(item)
            return None

    orm.DeclarativeBase = _DeclarativeBase
    orm.Session = _Anything
    orm.relationship = _Anything()
    orm.sessionmaker = _Anything()
    orm.declarative_base = lambda *a, **k: _DeclarativeBase
    _module("sqlalchemy.exc").SQLAlchemyError = Exception


def _install_geoalchemy2() -> None:
    ga = _module("geoalchemy2")
    ga.Geometry = _Anything
    shape = _module("geoalchemy2.shape")
    shape.to_shape = _Anything()
    shape.from_shape = _Anything()
    _module("geoalchemy2.functions")


def _install_shapely() -> None:
    sh = _module("shapely")
    wkt = _module("shapely.wkt")
    wkt.loads = _Anything()
    sh.wkt = wkt
    geometry = _module("shapely.geometry")
    geometry.shape = _Anything()
    _module("shapely.ops")


class _Dim:
    """Spaltenmaß; nimmt jede Breite entgegen."""

    width = 0


class _Dims(dict):
    def __missing__(self, key):
        self[key] = _Dim()
        return self[key]


class _Cell:
    def __init__(self, value):
        self.value = value
        self.alignment = None
        self.column_letter = "A"

    @property
    def column(self):
        return self


class _Sheet:
    def __init__(self, title: str):
        self.title = title
        self.rows: list[list] = []
        self.column_dimensions = _Dims()

    def append(self, row):
        self.rows.append(list(row))

    @property
    def max_row(self):
        return len(self.rows)

    def cell(self, row, column):
        return _Cell(self.rows[row - 1][column - 1])

    @property
    def columns(self):
        width = max((len(r) for r in self.rows), default=0)
        return [[_Cell(r[i] if i < len(r) else None) for r in self.rows] or [_Cell(None)]
                for i in range(width)] or [[_Cell(None)]]


class _Workbook:
    """Nimmt Zeilen entgegen und behält sie im Speicher (kein echtes xlsx)."""

    def __init__(self):
        self.active = _Sheet("Sheet")
        self.worksheets = [self.active]
        self.column_dimensions = _Dims()

    def create_sheet(self, title):
        ws = _Sheet(title)
        self.worksheets.append(ws)
        return ws

    def save(self, buf):
        buf.write(b"stub-xlsx")


def _install_openpyxl() -> None:
    xl = _module("openpyxl")
    xl.Workbook = _Workbook
    xl.load_workbook = _Anything()
    styles = _module("openpyxl.styles")
    styles.Alignment = _Anything


def _install_pydantic() -> None:
    class _Base:
        """Klassenattribute sind die Defaults; Keyword-Argumente überschreiben."""

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    if _missing("pydantic"):
        pyd = _module("pydantic")
        pyd.BaseModel = _Base
        pyd.Field = lambda default=None, **k: default
        pyd.field_validator = lambda *a, **k: (lambda f: f)
        pyd.ConfigDict = dict
    if _missing("pydantic_settings"):
        ps = _module("pydantic_settings")
        ps.BaseSettings = _Base
        ps.SettingsConfigDict = dict


class _AnyModule(types.ModuleType):
    """Modul, das jedes Attribut als Platzhalter liefert."""

    def __getattr__(self, item):
        if item.startswith("__"):
            raise AttributeError(item)
        return _Anything()


class _FallbackLoader:
    def create_module(self, spec):
        mod = _AnyModule(spec.name)
        mod.__path__ = []   # als Paket behandeln, damit Untermodule mitgehen
        return mod

    def exec_module(self, module):
        return None


class _FallbackFinder:
    """Letzter Finder in ``sys.meta_path``: deckt sonst fehlende Fremdpakete ab.

    Greift nur, wenn kein echter Finder das Modul liefert, und nie für ``app``
    oder die Tests selbst — ein echter Importfehler im Produktivcode bleibt
    damit sichtbar. numpy, pandas und pyogrio stehen bewusst **nicht** in
    ``ERSETZBAR``: numpy und pyogrio kommen über ``backend/requirements.txt``
    und sind in der Prüfumgebung inzwischen echt installiert; pandas ist eine
    von pyogrio selbst über ``try/except ImportError`` weich geprüfte
    Abhängigkeit — ein pauschales Ersatzmodul würde dort ``pandas is not
    None`` liefern und den anschließenden Zugriff auf ``pandas.__version__``
    mit ``AttributeError`` statt der von pyogrio erwarteten Fallback-Antwort
    scheitern lassen.
    """

    #: Fremdpakete, die die Importkette von Export und KI-Kontext berührt und
    #: die für diesen Test keine echte Funktion beisteuern.
    ERSETZBAR = {
        "httpx", "requests", "rasterio", "pyproj", "fiona",
        "fastapi", "starlette", "jinja2", "anthropic", "psycopg2", "redis",
        "scipy", "netCDF4", "xarray", "dateutil", "affine",
    }

    def find_spec(self, fullname, path=None, target=None):
        wurzel = fullname.split(".")[0]
        if wurzel not in self.ERSETZBAR:
            return None
        if not _missing(wurzel):  # echtes Paket bleibt unangetastet
            return None
        return importlib.util.spec_from_loader(fullname, _FallbackLoader())


def install() -> None:
    """Fehlende Schwergewichte durch Ersatzmodule abdecken (idempotent)."""
    if _missing("sqlalchemy"):
        _install_sqlalchemy()
    if _missing("geoalchemy2"):
        _install_geoalchemy2()
    if _missing("shapely"):
        _install_shapely()
    if _missing("openpyxl"):
        _install_openpyxl()
    _install_pydantic()
    if not any(isinstance(f, _FallbackFinder) for f in sys.meta_path):
        sys.meta_path.append(_FallbackFinder())

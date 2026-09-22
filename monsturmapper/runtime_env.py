"""
Runtime environment helpers for geospatial dependencies.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _has_proj_db(path: Path) -> bool:
    """True when the provided directory contains proj.db."""
    return path.is_dir() and (path / "proj.db").is_file()


def _candidate_prefixes() -> list[Path]:
    """Collect likely environment prefixes that may include PROJ/GDAL data."""
    prefixes: list[Path] = []

    for value in [
        os.environ.get("CONDA_PREFIX"),
        os.environ.get("VIRTUAL_ENV"),
        sys.prefix,
        sys.base_prefix,
    ]:
        if value:
            prefixes.append(Path(value))

    # De-duplicate while preserving order.
    seen: set[str] = set()
    ordered: list[Path] = []
    for prefix in prefixes:
        key = str(prefix.resolve()) if prefix.exists() else str(prefix)
        if key not in seen:
            ordered.append(prefix)
            seen.add(key)

    return ordered


def configure_geo_data_paths() -> None:
    """
    Ensure PROJ/GDAL lookup paths are set when available.

    This prevents runtime failures like:
    "PROJ: proj_create_from_database: Cannot find proj.db".
    """
    proj_candidates: list[Path] = []

    env_proj = os.environ.get("PROJ_DATA") or os.environ.get("PROJ_LIB")
    if env_proj:
        proj_candidates.append(Path(env_proj))

    try:
        from pyproj.datadir import get_data_dir  # type: ignore

        pyproj_data = get_data_dir()
        if pyproj_data:
            proj_candidates.append(Path(pyproj_data))
    except Exception:
        pass

    for prefix in _candidate_prefixes():
        proj_candidates.extend(
            [
                prefix / "share" / "proj",
                prefix / "Library" / "share" / "proj",
            ]
        )

    try:
        import rasterio  # type: ignore

        rasterio_root = Path(rasterio.__file__).resolve().parent
        proj_candidates.extend(
            [
                rasterio_root / "proj_data",
                rasterio_root / "share" / "proj",
            ]
        )
    except Exception:
        pass

    for candidate in proj_candidates:
        if _has_proj_db(candidate):
            resolved = str(candidate.resolve())
            os.environ["PROJ_DATA"] = resolved
            os.environ["PROJ_LIB"] = resolved
            break

    # GDAL data is usually bundled near PROJ data in these locations.
    if "GDAL_DATA" not in os.environ:
        gdal_candidates: list[Path] = []
        for prefix in _candidate_prefixes():
            gdal_candidates.extend(
                [
                    prefix / "share" / "gdal",
                    prefix / "Library" / "share" / "gdal",
                ]
            )

        try:
            import rasterio  # type: ignore

            rasterio_root = Path(rasterio.__file__).resolve().parent
            gdal_candidates.append(rasterio_root / "gdal_data")
        except Exception:
            pass

        for candidate in gdal_candidates:
            if candidate.is_dir():
                os.environ["GDAL_DATA"] = str(candidate.resolve())
                break

"""Minimal DuckDB load of a roster (synthetic or committed). DEV/TEST only."""

from __future__ import annotations

from typing import Any

import duckdb


def load_profiles(profiles: list[dict[str, Any]], conn: duckdb.DuckDBPyConnection | None = None):
    """Load profiles into an in-memory DuckDB table `roster`. Values only; labels stay on the document."""
    con = conn or duckdb.connect(":memory:")
    con.execute(
        """
        CREATE TABLE roster (
            name VARCHAR,
            party VARCHAR,
            seat_type VARCHAR,
            ward_number INTEGER,
            council VARCHAR,
            name_label VARCHAR,
            party_label VARCHAR,
            source_url VARCHAR,
            source_page INTEGER
        )
        """
    )
    rows = []
    for p in profiles:
        rows.append(
            (
                p["name"]["value"],
                p["party"]["value"],
                p["seat_type"]["value"],
                p["ward_number"]["value"],
                p["council"]["value"],
                p["name"]["label"],
                p["party"]["label"],
                p["name"].get("source_url"),
                p["name"].get("source_page"),
            )
        )
    if rows:
        con.executemany("INSERT INTO roster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
    return con

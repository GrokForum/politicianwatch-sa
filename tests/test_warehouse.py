"""DuckDB load on synthetic profiles only."""

from pwatch.warehouse import load_profiles


def test_duckdb_roster_round_trip(synthetic_profiles):
    con = load_profiles(synthetic_profiles)
    n, wards = con.execute(
        "SELECT count(*), count(*) FILTER (WHERE seat_type = 'ward') FROM roster"
    ).fetchone()
    assert n == 3
    assert wards == 2
    name, label, page = con.execute(
        "SELECT name, name_label, source_page FROM roster WHERE name = 'THABO TESTWARD'"
    ).fetchone()
    assert name == "THABO TESTWARD"
    assert label == "Confirmed"
    assert page == 10
    missing = con.execute("SELECT ward_number FROM roster WHERE name = 'NOMVULA FIXTURE'").fetchone()[0]
    assert missing is None

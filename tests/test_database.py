import sqlite3
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "healthcare_data.db"

@pytest.fixture(scope = "module")
def connection():
    if not DB_PATH.is_file():
        pytest.fail(
            "Database is missing. Run scripts/generate_data.py first"
        )
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    
    yield conn
    
    conn.close()
    
def test_expected_record_counts(connection):
    expected = {
        "patients": 1000,
        "encounters": 3000,
        "appointments": 2000
    }
    
    for table, expected_count in expected.items():
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]
        
        assert count == expected_count
        
def test_no_duplicate_patient_ids(connection):
    duplicates = connection.execute(
        """
        SELECT patient_id
        FROM patients
        GROUP BY patient_id
        HAVING COUNT(*) > 1
        """
    ).fetchall()
    
    assert duplicates == []
    
def test_foreign_key_integrity(connection):
    violations = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()
    
    assert violations == []
    
def test_no_negative_encounter_costs(connection):
    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM encounters
        WHERE cost < 0 OR cost IS NULL
        """
    ).fetchone()[0]
    
    assert count == 0
    
def test_valid_appointment_statuses(connection):
    invalid = connection.execute(
        """
        SELECT COUNT(*)
        FROM appointments
        WHERE LOWER(TRIM(status)) NOT IN (
            'completed',
            'cancelled',
            'no show'
        )
        OR status IS NULL
        """
    ).fetchone()[0]
    
    assert invalid == 0
    
def test_encounter_join_preserves_row_count(connection):
    encounter_count = connection.execute(
        "SELECT COUNT (*) FROM encounters"
    ).fetchone()[0]
    
    joined_count = connection.execute(
        """
        SELECT COUNT (*)
        FROM encounters AS e
        JOIN patients AS p
            ON e.patient_id = p.patient_id
        """
    ).fetchone()[0]
    
    assert joined_count == encounter_count
    
def test_inspect_appointment_statuses(connection):
    results = connection.execute("""
        SELECT status, COUNT(*)
        FROM appointments
        GROUP BY status
        ORDER BY status
    """).fetchall()

    print("\nAppointment statuses in database:")

    for status, count in results:
        print(f"{status}: {count}")
from datetime import date

import pandas as pd
import pytest

from src.analytics import (
    filter_encounters,
    filter_appointments,
    calculate_encounter_kpis,
    calculate_appointment_kpis
)

@pytest.fixture
def sample_encounters():
    """Create a small dataset with known results."""
    
    return pd.DataFrame({
        "patient_id": ["P001", "P001", "P002", "P003"],
        "visit_date": pd.to_datetime([
            "2026-01-10",
            "2026-01-15",
            "2026-02-10",
            "2026-03-10"
        ]),
        "department": [
            "Cardiology",
            "Cardiology",
            "Dermatology",
            "Neurology"
        ],
        "insurance_provider": [
            "Aetna",
            "Aetna",
            "Cigna",
            "Aetna"
        ],
        "cost": [
            100.0,
            200.0,
            300.0,
            400.0
        ]
    })
    
@pytest.fixture
def sample_appointments():
    return pd.DataFrame({
        "appointment_date": pd.to_datetime([
            "2026-01-10",
            "2026-01-11",
            "2026-01-12",
            "2026-01-13"
        ]),
        "insurance_provider": [
            "Aetna",
            "Aetna",
            "Cigna",
            "Cigna",
        ],
        "status": [
            "Completed",
            "No-Show",
            "Completed",
            "Cancelled"
        ]
    })
    
def test_total_encounters(sample_encounters):
    result = calculate_encounter_kpis(sample_encounters)
    assert result["total_encounters"] == 4
    
def test_unique_patients(sample_encounters):
    result = calculate_encounter_kpis(sample_encounters)
    assert result["unique_patients"] == 3
    
def test_average_cost(sample_encounters):
    result = calculate_encounter_kpis(sample_encounters)
    assert result["average_cost"] == pytest.approx(250.0)
    
def test_no_show_rate(sample_appointments):
    result = calculate_appointment_kpis(sample_appointments)
    assert result["total_appointments"] == 4
    assert result["no_shows"] == 1
    assert result["no_show_rate"] == pytest.approx(25.0)
    
def test_department_filter(sample_encounters):
    result = filter_encounters(
        sample_encounters,
        date(2026, 1, 1),
        date(2026, 12, 31),
        ["Cardiology"],
        ["Aetna", "Cigna"]
    )
    
    assert len(result) == 2
    assert set(result["department"]) == {"Cardiology"}
    
def test_insurance_filter(sample_appointments):
    result = filter_appointments(
        sample_appointments,
        date(2026, 1 , 1),
        date(2026, 12, 31),
        ["Aetna"]
    )
    
    assert len(result) == 2
    
def test_empty_encounter_metrics(sample_encounters):
    empty = sample_encounters.iloc[0:0]
    result = calculate_encounter_kpis(empty)
    
    assert result["total_encounters"] == 0
    assert result["unique_patients"] == 0
    assert result["average_cost"] == 0
    
def test_empty_appointment_metrics(sample_appointments):
    empty = sample_appointments.iloc[0:0]
    result = calculate_appointment_kpis(empty)
    
    assert result["total_appointments"] == 0
    assert result["no_shows"] == 0
    assert result["no_show_rate"] == 0 
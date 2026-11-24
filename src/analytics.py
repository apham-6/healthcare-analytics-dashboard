import pandas as pd

def filter_encounters(
    encounters,
    start_date,
    end_date,
    departments,
    providers
):
    """Filter encounters by date, department, and insurer."""
    
    return encounters.loc[
        encounters["visit_date"].dt.date.between(
            start_date, end_date
        )
        & encounters["department"].isin(departments)
        & encounters["insurance_provider"].isin(providers)
    ].copy()
    
def filter_appointments(
    appointments,
    start_date,
    end_date,
    providers
):
    """Filter appointments by date and insurer."""
    
    return appointments.loc[
        appointments["appointment_date"].dt.date.between(
            start_date, end_date
        )
        & appointments["insurance_provider"].isin(providers)
    ].copy()
    
def calculate_encounter_kpis(encounters):
    """Calculate operational metrics from encounters."""
    
    total = len(encounters)
    
    return {
        "total_encounters": total,
        "unique_patients": encounters["patient_id"].nunique(),
        "average_cost": (
            float(encounters["cost"].mean())
            if total > 0 else 0.0
        )
    }
    
def calculate_appointment_kpis(appointments):
    """Calculate appointment volume and no-show rate"""
    
    total = len(appointments)
    
    no_shows = int(
        (appointments["status"] == "No-Show").sum()
    )
    
    return {
        "total_appointments": total,
        "no_shows": no_shows,
        "no_show_rate": (
            no_shows/total * 100
            if total > 0 else 0.0
        )
    }

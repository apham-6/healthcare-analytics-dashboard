import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import (
    filter_encounters,
    filter_appointments,
    calculate_encounter_kpis,
    calculate_appointment_kpis
)

# Implement data logger
from src.logger import get_logger

logger=get_logger()

# -----------------------------------
# 1. Page configuration
# -----------------------------------

st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "healthcare_data.db"

# -----------------------------------
# 2. Load data from SQLite
# -----------------------------------

@st.cache_data
def load_data(database_path, modified_time):
    logger.info("Loading healthcare data from SQLite")
    
    with sqlite3.connect(database_path) as connection:
        encounters = pd.read_sql_query("""
            SELECT
                e.encounter_id,
                e.patient_id,
                e.visit_date,
                e.department,
                e.cost,
                p.insurance_provider
            FROM encounters AS e
            JOIN patients AS p
                ON e.patient_id = p.patient_id
        """, connection)
        
        appointments = pd.read_sql_query("""
            SELECT
                a.appointment_id,
                a.patient_id,
                a.appointment_date,
                a.status,
                p.insurance_provider
            FROM appointments AS a
            JOIN patients AS p
                ON a.patient_id = p.patient_id
        """, connection)
        
        encounters["visit_date"] = pd.to_datetime(
            encounters["visit_date"])
        
        appointments["appointment_date"] = pd.to_datetime(
            appointments["appointment_date"])
        
        # Implement data logger
        logger.info(
            "Data loaded successfully: %s encounters, %s appointments",
            len(encounters),
            len(appointments)
        )
        
        return encounters, appointments
    
if not DB_PATH.is_file():
    st.error("Database not found. Run scripts/generate_data.py to create the database.")
    st.stop()

# Initial data loader, replacing with exception handling    
# encounters, appointments = load_data(
#     str(DB_PATH),
#     DB_PATH.stat().st_mtime_ns
# )

# Implement error handling
try:
    encounters,appointments=load_data(
        str(DB_PATH),
        DB_PATH.stat().st_mtime_ns
    )
except (sqlite3.Error,pd.errors.DatabaseError,OSError,ValueError):
    logger.exception("Failed to load healthcare database")
    
    st.error(
        "Unable to load healthcare data. "
        "Please verify the database and try again."
    )
    
    st.info(
        "Run scripts/generate_data.py to regenerate "
        "the synthetic healthcare database."
    )
    
    st.stop()
    
if encounters.empty or appointments.empty:
    st.warning(
        "The healthcare database contains an empty dataset. "
        "Please regenerate the synthetic data."
    )
    
    st.stop()

# -----------------------------------
# 3. Dashboard header
# -----------------------------------

# Improved dashboard header
st.title("🏥 Healthcare Analytics Dashboard")

st.markdown(
    "### Clinical Operations & Performance Analytics"
)

st.caption(
    "Interactive healthcare reporting and operational "
    "performance monitoring using synthetic data."
)

st.divider()

# Initial portfolio dashboard header
# st.write(
#     "Interactive analysis of synthetic healthcare "
#     "encounters and appointment records."
# )

# st.caption(
#     "Portfolio project | Python • SQLite • Pandas • Plotly • Streamlit"
# )

# -----------------------------------
# 4. Sidebar filters
# -----------------------------------

st.sidebar.header("Dashboard Filters")

min_date = min(
    encounters["visit_date"].min(),
    appointments["appointment_date"].min()
).date()

max_date = max(
    encounters["visit_date"].max(),
    appointments["appointment_date"].max()
).date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value = (min_date, max_date),
    min_value = min_date,
    max_value = max_date
)

departments = sorted(
    encounters["department"].unique().tolist()
)

selected_departments = st.sidebar.multiselect(
    "Select Departments",
    options = departments,
    default = departments
)

providers = sorted(
    encounters["insurance_provider"].unique().tolist()
)

selected_providers = st.sidebar.multiselect(
    "Select Insurance Providers",
    options = providers,
    default = providers
)

if len(date_range) != 2:
    st.info("Select both a start date and an end date.")
    st.stop()
    
start_date, end_date = date_range

if start_date > end_date:
    st.error("Start date must be before the end date.")
    st.stop()

# -----------------------------------
# 5. Apply dashboard filters
# -----------------------------------

filtered_encounters = filter_encounters(
    encounters,
    start_date,
    end_date,
    selected_departments,
    selected_providers
)

filtered_appointments = filter_appointments(
    appointments,
    start_date,
    end_date,
    selected_providers
)

# Logger warnings for empty filtered selections
if filtered_encounters.empty:
    logger.warning("No encounters match the selected filters")

if filtered_appointments.empty:
    logger.warning("No appointments match the selected filters")

st.caption(
    "Department filters apply to encounters only. "
    "Appointments are filtered by date and insurance provider"
)

# -----------------------------------
# 6. Calculate KPI metrics
# -----------------------------------

encounter_kpis = calculate_encounter_kpis(filtered_encounters)

appointment_kpis = calculate_appointment_kpis(filtered_appointments)

total_encounters = encounter_kpis["total_encounters"]
unique_patients = encounter_kpis["unique_patients"]
average_cost = encounter_kpis["average_cost"]

total_appointments = appointment_kpis["total_appointments"]
no_shows = appointment_kpis["no_shows"]
no_show_rate = appointment_kpis["no_show_rate"]

# -----------------------------------
# 7. Calculate KPI metrics
# -----------------------------------

total_encounters = len(filtered_encounters)

unique_patients = (
    filtered_encounters["patient_id"].nunique()
)

average_cost = (
    filtered_encounters["cost"].mean()
    if total_encounters > 0 else 0
)

total_appointments = len(filtered_appointments)

no_shows = (
    filtered_appointments["status"] == "No Show"
).sum()

no_show_rate = (
    (no_shows/total_appointments) * 100
    if total_appointments > 0 else 0
)

# -----------------------------------
# 8. Display KPI cards
# -----------------------------------

# Improved KPI cards
st.subheader("Operational Performance")

col1,col2,col3,col4=st.columns(4)

col1.metric(
    label="Total Encounters",
    value=f"{total_encounters:,}",
    help="Total healthcare encounters matching the selected filters",
    border=True
)

col2.metric(
    label="Unique Patients",
    value=f"{unique_patients:,}",
    help="Number of distinct patients with matching encounters.",
    border=True
)

col3.metric(
    label="Average Encounter Cost",
    value=(
        f"${average_cost:,.2f}"
        if total_encounters>0 else "N/A"
    ),
    help="Mean cost per encounter.",
    border=True
)

col4.metric(
    label="Appointment No-Show Rate",
    value=(
        f"{no_show_rate:.1f}%"
        if total_appointments>0 else "N/A"
    ),
    help="No-show appointments divided by all selected appointments.",
    border=True
)

st.divider()

# Initial portfolio KPI cards
# st.subheader("Key Performance Indicators")

# col1, col2, col3, col4 = st.columns(4)

# col1.metric(
#     "Total Encounters",
#     f"{total_encounters:,}"
# )

# col2.metric(
#     "Unique Patients",
#     f"{unique_patients:,}"
# )

# col3.metric(
#    "Average Encounter Cost",
#    f"${average_cost:,.2f}"
# )

# col4.metric(
#     "No-Show Rate",
#     f"{no_show_rate:.1f}%"
# )

# -----------------------------------
# 9. Monthly encounter trends
# -----------------------------------

st.subheader("Monthly Encounter Trends")

if not filtered_encounters.empty:
    monthly_visits = (
        filtered_encounters.assign(
            month = filtered_encounters["visit_date"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby("month", as_index=False)
        .size()
        .rename(columns={"size": "encounters"})
    )
    
    # Improved monthly trend figure
    fig_monthly = px.line(
        monthly_visits,
        x = "month",
        y = "encounters",
        markers = True,
        title = "Healthcare Encounters by Month",
        labels = {
            "month": "Month",
            "encounters": "Number of Encounters"
        }
    )
    
    fig_monthly.update_traces(
        line=dict(color="#147D85",width=3),
        marker=dict(size=7)
    )
    
    fig_monthly.update_layout(
    hovermode="x unified"
    )
    
    st.plotly_chart(
        fig_monthly,
        width="stretch"
    )
else:
    st.info("No encounter data available for the selected filters.")
    
# -----------------------------------
# 10. Encounters by department
# -----------------------------------

st.subheader("Encounters by Department")

if not filtered_encounters.empty:
    department_visits = (
        filtered_encounters
        .groupby("department", as_index=False)
        .size()
        .rename(columns={"size": "encounters"})
        .sort_values("encounters", ascending=False)
    )
    
    fig_departments = px.bar(
        department_visits,
        x = "department",
        y = "encounters",
        title = "Encounter Volume by Department",
        labels = {
            "department": "Department",
            "encounters": "Number of Encounters"
        }
    )
    
    # Improved department figure
    fig_departments.update_traces(
        marker_color="#147D85"
    )
    
    st.plotly_chart(
        fig_departments,
        width="stretch"
    )
else:
    st.info("No department data available.")
    
# -----------------------------------
# 11. Appointment status distribution
# -----------------------------------

st.subheader("Appointment Status Distribution")

if not filtered_appointments.empty:
    appointment_summary = (
        filtered_appointments
        .groupby("status", as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    
    fig_appointments = px.pie(
        appointment_summary,
        names = "status",
        values = "count",
        hole = 0.55,
        title = "Appointment Status Breakdown",
        color="status",
        color_discrete_map={
            "Completed":"#147D85",
            "Cancelled":"#E8AE43",
            "No-Show":"#D65C5C"
        }
    )
    
    # Improved appointment status distribution figure
    fig_appointments.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )
    
    fig_appointments.update_layout(
        legend_title_text="Appointment Status"
    )
    
    st.plotly_chart(
        fig_appointments,
        width="stretch"
    )
else:
    st.info("No appointment data available for the selected filters.")
    
# -----------------------------------
# 12. View and download records
# -----------------------------------

st.subheader("Encounter Records")

st.dataframe(
    filtered_encounters,
    width="stretch",
    hide_index = True
)

csv = filtered_encounters.to_csv(index=False)

st.download_button(
    label = "Download Filtered Encounters",
    data = csv,
    file_name = "healthcare_encounters.csv",
    mime = "text/csv"
)

st.caption(
    "All records are synthetic and do not represent "
    "real patient data. This dashboard is for educational "
    "purposes only."
)
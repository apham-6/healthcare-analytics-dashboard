import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

# Use a fixed seed so the generated data is reproducible
random.seed(42)

# Locate the project directory and db file
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "healthcare_data.db"

NUM_PATIENTS = 1000
NUM_ENCOUNTERS = 3000
NUM_APPOINTMENTS = 2000

insurance_providers = [
    "Aetna",
    "Blue Cross Blue Shield",
    "Cigna",
    "UnitedHealthcare",
    "Medicare",
    "Medicaid",
]

departments = [
    "Primary Care",
    "Cardiology",
    "Dermatology",
    "Orthopedics",
    "Neurology",
    "Emergency",
]

appointment_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "No Show",
]

def random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    days_between = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days_between)
                                  )
    
# Connect to SQLite
connection = sqlite3.connect(DB_PATH)
connection.execute("PRAGMA foreign_keys = ON;")
cursor = connection.cursor()

# Create database tables
cursor.executescript("""
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS encounters;
DROP TABLE IF EXISTS patients;
                
CREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    birth_date TEXT NOT NULL,
    sex TEXT NOT NULL,
    insurance_provider TEXT NOT NULL
);

CREATE TABLE encounters (
    encounter_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    visit_date TEXT NOT NULL,
    department TEXT NOT NULL,
    cost REAL NOT NULL CHECK (cost >= 0),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE appointments (
    appointment_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
""")

# Generate patients
patients = []

for i in range(1, NUM_PATIENTS + 1):
    patient_id = f"P{i:05d}"
    birth_date = random_date(
        date(1940, 1, 1), 
        date(2020, 12, 31))
    sex = random.choice(["Male", "Female"])
    insurance = random.choice(insurance_providers)
    
    patients.append((
        patient_id, 
        birth_date.isoformat(), 
        sex, 
        insurance))
    
cursor.executemany("""
INSERT INTO patients (
    patient_id, 
    birth_date, 
    sex, 
    insurance_provider)
VALUES (?, ?, ?, ?)
""", patients)

# Generate encounters
encounters = []

for i in range(1, NUM_ENCOUNTERS + 1):
    encounter_id = f"E{i:05d}"
    patient_id = random.choice(patients)[0]
    visit_date = random_date(
        date(2025, 1, 1), 
        date(2026, 10, 31))
    department = random.choice(departments)
    cost = round(random.uniform(75, 2500), 2)
    
    encounters.append((
        encounter_id, 
        patient_id, 
        visit_date.isoformat(), 
        department, 
        cost))
    
cursor.executemany("""
INSERT INTO encounters (
    encounter_id,
    patient_id,
    visit_date,
    department,
    cost)
VALUES (?, ?, ?, ?, ?)
""", encounters)

# Generate appointments
appointments = []

for i in range(1, NUM_APPOINTMENTS + 1):
    appointment_id = f"A{i:05d}"
    patient_id = random.choice(patients)[0]
    appointment_date = random_date(
        date(2025, 1, 1), 
        date(2026, 10, 31))
    status = random.choice(appointment_statuses)
    
    appointments.append((
        appointment_id, 
        patient_id, 
        appointment_date.isoformat(), 
        status))
    
cursor.executemany("""
INSERT INTO appointments (
    appointment_id,
    patient_id,
    appointment_date,
    status)
VALUES (?, ?, ?, ?)
""", appointments)

# Save all records
connection.commit()

# Verify record counts
for table in ["patients", "encounters", "appointments"]:
    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    
    print(f"{table}: {count:,} records")
    
print(f"\nENCOUNTERS BY INSURANCE PROVIDER:")

cursor.execute("""
    SELECT
        p.insurance_provider,
        COUNT(e.encounter_id) AS total_encounters
    FROM patients AS p
    JOIN encounters AS e
        ON p.patient_id = e.patient_id
    GROUP BY p.insurance_provider
    ORDER BY total_encounters DESC
""") 

for row in cursor.fetchall():
    print(row)   
    
# Close the database connection
connection.close()

print(f"\nDatabase created successfully: {DB_PATH}")
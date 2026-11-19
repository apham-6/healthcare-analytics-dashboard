import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "healthcare_data.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

print("\nTOTAL PATIENTS")
cursor.execute("SELECT COUNT(*) FROM patients;")
print(cursor.fetchone()[0])

print("\nTOTAL ENCOUNTERS")
cursor.execute("SELECT COUNT(*) FROM encounters;")
print(cursor.fetchone()[0])

print("\nVISITS BY DEPARTMENT")
cursor.execute("""
    SELECT
        department,
        COUNT(*) AS total_visits
    FROM encounters
    GROUP BY department
    ORDER BY total_visits DESC
""")

for row in cursor.fetchall():
    print(row)
    
print("\nAPPOINTMENT STATUS")
cursor.execute("""
    SELECT
        status,
        COUNT(*) AS total
    FROM appointments
    GROUP BY status
    ORDER BY total DESC
""")

for row in cursor.fetchall():
    print(row)
    
print("\nAVERAGE ENCOUNTER COST")
cursor.execute("""
    SELECT ROUND(AVG(cost), 2)
    FROM encounters
""")
print(cursor.fetchone()[0])

print("\nENCOUNTERS BY INSURANCE PROVIDER")

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

connection.close()
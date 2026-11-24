# Healthcare Analytics Dashboard

[![Healthcare Dashboard Tests](https://github.com/apham-6/healthcare-analytics-dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/apham-6/healthcare-analytics-dashboard/actions/workflows/tests.yml)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

# Overview

An interactive healthcare analytics application developed using Python, SQLite, Pandas, Plotly, and Streamlit.

The project demonstrates healthcare data management, SQL integration, operational KPI analysis, interactive visualization, and automated software testing.

All patient, encounter, and appointment records are synthetically generated.

# Features

- Interactive dashboard displaying healthcare operational metrics
- Total encounters and unique patient counts
- Average encounter cost analysis
- Appointment no-show rate calculations
- Department and insurance provider filters
- Monthly encounter trends
- Appointment status visualizations
- Downloadable encounter reports
- Automated data quality and application logic tests

# Technologies

| Technology: Purpose
| Python: Application development
| SQLite: Relational database
| Pandas: Data processing and analysis
| Streamlit: Interactive dashboard
| Plotly: Data visualization
| Pytest: Automated testing
| GitHub Actions: Continuous integration

# Project Architecture

Synthetic Data Generator -> SQLite Database -> Python/Pandas Analytics -> Streamlit Dashboard

Automated testing is performed using Pytest and GitHub Actions.

# Dataset

The application generates 1,000 synthetic patient records, 3,000 encounters, and 2,000 appointments.

The dataset is fictional and does not contain protected health information (PHI).

Appointments and encounters are generated independently, and appointment metrics are not interpreted as encounter conversion rates.

# Installation

Clone the repository and navigate to the project directory.

Create and activate a Python virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

python -m pip install -r requirements.txt

Generate the synthetic database:

python scripts/generate_data.py

Run the dashboard:

python -m streamlit run app.py

# Testing

Run the automated test suite:

python -m pytest tests/ -v

The project includes tests for KPI calculations, filtering, database integrity, and data validation.

# Screenshots

## 1. Dashboard Overview
The main dashboard provides a centralized view of key healthcare performance indicators, patient encounters, and operational metrics.

![Dashboard Overview](screenshots/dashboard-overview.png)

## 2. Monthly Encounter Trends
Visualize healthcare encounter trends over time to identify patterns in patient volume, service utilization, and operational demand.

![Monthly Encounter Trends](screenshots/monthly-trends.png)

## 3. Encounters by Department
Displays the distribution of patient encounters across healthcare departments to support resource allocation, worklad assessment, and departmental performance analysis.

![Encounters by Department](screenshots/encounters-by-department.png)

## 4. Appointment Status Distribution
Appointment performance metrics to help identify scheduling trends, cancellations, and patient no-show rates.

![Appointment Status Distribution](screenshots/appointment-status.png)

## 5. Encounter Records
Table that provides a detailed, filterable view of individual encounter records, enabling granular data exploration and operational reporting.

![Encounter Records](screenshots/encounter-records.png)

## 6. Dashboard Filters
Enables users to dynamically filter healthcare data by department and insurance provider. Key performance indicators, visualizations, and encounter records update based on selected criteria, supporting targeted analysis, healthcare utilization monitoring, and data-driven operational decision-making.

![Dashboard Filters](screenshots/dashboard-filters.png)

# Application Architechture

```mermaid
flowchart TD
    A[Synthetic Data Generator] --> B[(SQLite Database)]
    B --> D[Streamlit Application]
    D --> C[Analytics Layer]
    C --> D
    D --> E[Interactive Dashboard]
    D --> F[CSV Export]
    D --> G[Application Logs]
    H[Pytest] -. Validates .-> C
    H -. Validates .-> B
```

# Continuous Integration Pipeline

```mermaid
flowchart TD
    A[Developer Push or Pull Request] --> B[GitHub Actions]
    B --> C[Ubuntu Runner]
    C --> D[Set Up Python]
    D --> E[Install Dependencies]
    E --> F[Generate Synthetic Database]
    F --> G[Run Pytest]
    G --> H{Tests Passed?}
    H --> |Yes| I[Successful Workflow]
    H --> |No| J[Failed Workflow]
    J --> K[Review Logs and Fix Code]
    K --> A
```

# Project Limitations

- All healthcare records are synthetically generated and do not represent actual patients or clinical outcomes.
- Encounters and appointments are generated independently.
- Department filtering applies only to encounter records.
- Appointment no-show rates are calculated using all selected appointments as the denominator.
- SQLite is used for local database storage rather than enterprise-scale database infrastructure.
- The application is designed for educational and portfolio purposes and is not intended for production clinical use.
- Authentication, role-based access control, and cloud deployment are outside the current project scope.

# Future Improvements

- Integrate HL7 FHIR APIs
- Add PostgreSQL support
- Containerize the application using Docker
- Deploy to AWS
- Expand automated data quality monitoring

# Author

Alexander Pham

M.S. Bioinformatics — Johns Hopkins University

Healthcare professional transitioning into Healthcare IT and cloud engineering.
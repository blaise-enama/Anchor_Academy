# Anchor_Academy_DB
This is a MySQL Database + Python project that is meant to track, store, analyze and predict player progress and development. 
In sum, Anchor Academy is an end-to-end sports analytics system that ingests wearable tracking data (e.g., Playermaker), transforms it into a flexible schema, and generates performance insights and ML-ready features for player evaluation and profiling.

**Overview:**

This project simulates a real-world data platform used by sports teams to:

    Ingest player session data from external sources (API / CSV)
    Store data in a normalized, extensible schema
    Perform automated feature engineering
    Analyze player performance and trends
    Prepare datasets for machine learning applications

This system is designed to support ML workflows such as:

    Player position classification
    Performance trend analysis
    Fatigue / workload prediction
    Player similarity modeling


**Key Features**

*Data Ingestion Pipeline*
    Integrates with external APIs (Playermaker-style)
    Maps raw JSON → domain models
    Handles missing/invalid values safely
    Supports batch ingestion and automation

*Flexible Data Model*
    Player → Session → SessionMetric
    Metrics stored dynamically to avoid rigid schemas
    Easily extendable for new data sources or features


*Service Layer (Business Logic)*

Centralized orchestration of:
    Session creation
    Validation
    Feature engineering
    Ensures consistent logic across ingestion, CLI, and testing

*Feature Engineering*

Derived metrics include:

    Work Rate → combines distance + sprint intensity
    Foot Usage Ratio → left vs. right dominance
    Dominant Foot Classification

Transforms raw data into meaningful performance indicators

*Testable Architecture*
    Uses in-memory repositories for unit testing
    Mirrors production logic via service layer
    Simulates database behavior, thus eliminating dependency on a live database

 

**Getting Started**
*in the command line, run*
git clone https://github.com/your-username/Anchor_Academy.git
cd Anchor_Academy

*install Requirements*
pip install -r requirements.txt

*Run the interface using any of the program's arguments:*
    - add-player
    - delete-player
    - find-player
    - list-players
    - add-session
    - delete-session
    -list-session
    - player-sessions 

python cli.py < arg >


**Example Use case**
python cli.py add-session --player_id 1 --date 2026-02-10 ...
python cli.py list-player-sessions --name "John Doe"


**Output:**

Player: John Doe (ID: 1)
-------------------------------------------
Session ID: 1012 | Duration: 90 min

  total_distance: 9450 m
  sprints: 18
  max_speed: 29.3 km/h
  work_rate: 198.5
  foot_usage_ratio: 0.54
  dominant_foot: right


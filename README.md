The Anchor Academy Player Tracker Project is a Python + MySQL application designed to track, store, and analyze soccer player performance using data from wearable trackers (e.g., Playermaker).

It follows an object-oriented approach and uses the Repository Pattern to separate database access from business logic.

**Features** 
- Add and manage Players with attributes like name, age, position, and team.
- Record Sessions for players with performance metrics (distance, sprints, goals, etc.).
- Calculate derived metrics like work rate (e.g., distance per minute).
- Store data in a MySQL database with a clean schema.
- Repository pattern ensures maintainable, testable code.
- Includes unit tests for database connection and core methods.

**Tech Stack**
- Python 3.10+
- MySQL 8.0+
- PyMySQL for database access
- pytest for unit testing
- VS Code with SQLTools extension

**Setup & Installation**
1) Clone this Repository
2) Create a Virtual Environment:

    python -m venv .venv
    source .venv/bin/activate   # Mac/Linux
    .venv\Scripts\activate      # Windows

3) Install Dependencies:

    pip install -r requirements.txt

4) Configure Database:
Update config.json with your MySQL connection details:

    {
      "host": "localhost",
      "user": "root",
      "password": "yourpassword",
      "database": "Anchor_Academy"
    }

5) Run your SQL schema to Initialize Database Tables:

    CREATE TABLE Players (
        player_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        position VARCHAR(20),
        age INT,
        team VARCHAR(50)
    );
    
    CREATE TABLE Sessions (
        session_id INT AUTO_INCREMENT PRIMARY KEY,
        player_id INT,
        session_date DATE,
        duration_minutes INT,
        distance_km FLOAT,
        goals INT,
        sprints INT,
        FOREIGN KEY (player_id) REFERENCES Players(player_id)
    );
6) Running the Project:
    python main.py


**Essentially, This Player Tracker is a structured performance intelligence system that transforms session-level athlete data into longitudinal insights, enabling clinicians to reduce injury risk, coaches to optimize load, and organizations to standardize reporting.**
Some future enhancements include Integrating real-time data ingestions from trackers via API services; building dashboards with Power BI or Plotly;
adding predictive ML models to assess injury risk, performance forecasting, and player classification; deployment via Docker and connecting to cloud MySQL (AWS RDS, GCP CloudSQL, etc. )

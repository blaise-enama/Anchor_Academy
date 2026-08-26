# Anchor Academy

> A comprehensive sports analytics platform for tracking, analyzing, and predicting player performance using wearable sensor data.

## Overview

Anchor Academy is an end-to-end sports analytics system designed to transform raw player performance data into actionable insights. It ingests wearable tracking data (e.g., from Playermaker devices), normalizes it into a flexible database schema, and generates performance metrics and predictions to support data-driven coaching and player development decisions.

## Project Objectives & Goals

### Core Objectives
- **Centralize Player Data**: Build a single source of truth for player performance across multiple sessions and time periods
- **Automate Insight Generation**: Transform raw sensor data into meaningful performance indicators without manual intervention
- **Enable Evidence-Based Decision Making**: Provide coaches with data-driven insights to optimize training, player positioning, and workload management
- **Support Machine Learning**: Prepare clean, feature-engineered datasets for predictive models

### Key Use Cases
- **Player Position Classification**: Analyze movement patterns to suggest optimal positional fit
- **Performance Trend Analysis**: Track player metrics over time to identify development patterns
- **Fatigue & Workload Prediction**: Monitor and predict player fatigue to optimize training loads
- **Player Similarity Modeling**: Identify comparable players for benchmarking and recruitment

## Impact & Direction

Anchor Academy democratizes access to sophisticated sports analytics, traditionally available only to elite professional teams. By automating the pipeline from raw data to insights, it enables:

- **Coaches** to make faster, data-informed decisions about training and player development
- **Athletes** to receive objective performance feedback for improvement
- **Teams** to optimize resource allocation based on player workload and injury risk
- **Researchers** to build and test predictive models on real player data

## Key Features

### 📊 Data Ingestion Pipeline
- Integrates seamlessly with external APIs (Playermaker-compatible)
- Automatically maps raw JSON data to domain models
- Handles missing/invalid values safely with validation
- Supports both batch ingestion and real-time automation

### 🗄️ Flexible Data Model
- **Hierarchical Structure**: Player → Session → SessionMetric
- **Dynamic Metric Storage**: Avoids rigid schemas; easily add new metrics without schema changes
- **Extensible Design**: Built to accommodate new data sources and performance indicators

### ⚙️ Service Layer Architecture
- **Centralized Business Logic**: Orchestrates session creation, validation, and feature engineering
- **Consistency Guarantees**: Same logic applied across API ingestion, CLI, and automated testing
- **Testable Design**: In-memory repositories enable comprehensive unit testing without external dependencies

### 🔧 Automated Feature Engineering
Transforms raw data into performance indicators:
- **Work Rate**: Combines distance traveled and sprint intensity into a composite performance metric
- **Foot Usage Ratio**: Measures left vs. right foot dominance for tactical insight
- **Dominant Foot Classification**: Automatic positional/style classification based on usage patterns

### ✅ Production-Grade Architecture
- **Dependency Injection**: Clean separation of concerns with pluggable repositories
- **Comprehensive Testing**: Mock repositories mirror production logic; no live database required for testing
- **Error Handling**: Robust validation and graceful error handling throughout the pipeline

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- MySQL database (optional for local development; in-memory mock available for testing)
- API credentials for Playermaker or compatible data source

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/blaise-enama/Anchor_Academy.git
   cd Anchor_Academy
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with your configuration:
   ```env
   # Database credentials
   DB_HOST=localhost
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=anchor_academy

   # API credentials
   PLAYERMAKER_API_KEY=your_api_key
   PLAYERMAKER_API_URL=https://api.playermaker.io
   ```

### Running the CLI

The application provides a command-line interface for managing players and sessions:

```bash
python cli.py <command> [options]
```

#### Available Commands

**Player Management:**
- `add-player` — Register a new player
- `delete-player` — Remove a player from the system
- `find-player` — Search for a player by ID or name
- `list-players` — Display all players

**Session Management:**
- `add-session` — Record a new training/match session for a player
- `delete-session` — Remove a session
- `list-sessions` — Display all sessions
- `player-sessions` — View all sessions for a specific player

#### Example Usage

**Add a new player:**
```bash
python cli.py add-player --name "John Doe" --position "Forward"
```

**Add a session for a player:**
```bash
python cli.py add-session --player_id 1 --date 2026-02-10 --duration 90 --distance 9450 --sprints 18 --max_speed 29.3
```

**List all sessions for a player:**
```bash
python cli.py player-sessions --name "John Doe"
```

### Example Output

```
Player: John Doe (ID: 1)
-------------------------------------------
Session ID: 1012 | Date: 2026-02-10 | Duration: 90 min

  Metrics:
  ├─ total_distance: 9,450 m
  ├─ sprints: 18
  ├─ max_speed: 29.3 km/h
  ├─ work_rate: 198.5
  ├─ foot_usage_ratio: 0.54
  └─ dominant_foot: right
```

---

## Project Structure

```
Anchor_Academy/
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/
│   ├── models/           # Domain models (Player, Session, SessionMetric)
│   ├── repositories/     # Data access layer (abstract + implementations)
│   ├── services/         # Business logic layer
│   └── integrations/     # External API integrations (Playermaker)
└── tests/                # Unit and integration tests
```

---

## Development

### Running Tests

```bash
pytest
```

Tests use in-memory repositories, so no database setup is required.

### Adding a New Metric

1. Define the metric in the `SessionMetric` model
2. Add calculation logic to the feature engineering service
3. Update tests to verify the metric calculation
4. Deploy and it's automatically available in the system

---

## Technology Stack

- **Language**: Python 3.8+
- **Database**: MySQL
- **CLI Framework**: Click
- **Testing**: Pytest
- **API Integration**: Requests
- **Configuration**: python-dotenv

---

## License

This project is open source and available for educational and research purposes.

---

## Questions or Contributions?

For issues, questions, or contributions, please open an issue or submit a pull request on GitHub.

**Project Repository**: https://github.com/blaise-enama/Anchor_Academy

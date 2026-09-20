# Log Triage Tool

[![Run Tests](https://github.com/Mihir16x/Log-Triage-Tool/actions/workflows/tests.yml/badge.svg)](https://github.com/Mihir16x/Log-Triage-Tool/actions/workflows/tests.yml)

A Python-based log analysis tool that parses raw application logs, stores structured events in SQLite, calculates service-level error rates, and detects clustered error spikes for operational triage.

## Features

- Parses raw application logs into structured fields
- Extracts:
  - Timestamp
  - Severity level
  - Service name
  - Message
- Stores parsed events in SQLite
- Calculates INFO, WARN, and ERROR counts
- Computes error rates by service
- Detects bursts of errors within configurable time windows
- Includes automated tests with pytest
- Runs tests automatically with GitHub Actions CI

## Architecture

```text
Raw Log Files
      |
      v
Python Parser
      |
      v
Structured Events
      |
      v
SQLite Database
      |
      v
Analysis Engine
      |
      +----------------------+
      |                      |
      v                      v
Error Rates           Error Spike Detection
      |                      |
      +----------+-----------+
                 |
                 v
          CLI Triage Report
```

## Example Output

```text
=== LOG TRIAGE REPORT ===

Total log entries: 30

Log levels:
  INFO: 13
  WARN: 6
  ERROR: 11

Errors by service:
  payment-service: 4
  api-gateway: 4
  inventory-service: 3

Error rate by service:
  auth-service: 0.0%
  payment-service: 50.0%
  api-gateway: 50.0%
  inventory-service: 33.3%

Detected error spikes:
  payment-service -> 3 errors between 2026-09-20 09:04:25 and 2026-09-20 09:05:07
  api-gateway -> 3 errors between 2026-09-20 09:06:01 and 2026-09-20 09:06:13
  inventory-service -> 3 errors between 2026-09-20 09:09:45 and 2026-09-20 09:10:09
```

## Tech Stack

- Python 3.12
- SQLite
- SQL
- pytest
- GitHub Actions

## Project Structure

```text
Log Triage Tool/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── sample.log
│   └── production_sample.log
├── src/
│   ├── analyzer.py
│   ├── database.py
│   ├── main.py
│   └── parser.py
├── tests/
│   ├── test_analyzer.py
│   └── test_parser.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Log Format

The parser expects logs in this format:

```text
YYYY-MM-DD HH:MM:SS LEVEL service-name message
```

Example:

```text
2026-09-20 09:05:03 ERROR payment-service Payment provider timeout for order 5004
```

Each log entry is converted into:

```text
timestamp
level
service
message
```

## Error Rate Analysis

The analyzer calculates a service's error rate as:

```text
error count / total log count for that service
```

Example:

```text
payment-service:
4 ERROR events / 8 total events = 50.0% error rate
```

## Error Spike Detection

The tool identifies clusters of repeated failures within a short time window.

By default, an error spike is detected when:

```text
3 or more ERROR events
from the same service
occur within 2 minutes
```

For example:

```text
09:06:01 ERROR api-gateway
09:06:09 ERROR api-gateway
09:06:13 ERROR api-gateway
```

is detected as an operational error spike.

## SQLite Storage

Parsed logs are stored in a local SQLite database with the following structure:

```text
id
timestamp
level
service
message
```

The database is generated locally and excluded from Git version control.

## Tests

The project includes automated tests for:

- Valid log parsing
- Log-level counting
- Error counts by service
- Error-rate calculation
- Error-spike detection

Run the test suite with:

```powershell
python -m pytest
```

Current test result:

```text
5 passed
```

## Continuous Integration

GitHub Actions runs the full pytest suite automatically on:

- Every push
- Every pull request

The workflow:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs dependencies
4. Runs the complete pytest suite

Workflow file:

```text
.github/workflows/tests.yml
```

## Running Locally

### 1. Clone the repository

```powershell
git clone <repository-url>
cd "Log Triage Tool"
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Run the application

```powershell
python src\main.py
```

### 6. Run the tests

```powershell
python -m pytest
```

## Data

The repository uses synthetic application logs designed to simulate realistic operational scenarios such as:

- Payment provider timeouts
- API gateway failures
- Database connection failures
- Latency warnings
- Service recovery events

The synthetic datasets make it possible to demonstrate log analysis and anomaly detection without exposing private or proprietary production data.

## Future Improvements

Potential extensions include:

- Configurable anomaly thresholds
- Larger log datasets
- Time-series visualizations
- SQL-based diagnostic reports
- JSON and structured log support
- Exportable incident summaries

## Author

Mihir Karnani

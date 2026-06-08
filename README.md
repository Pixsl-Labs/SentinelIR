![Python](https://img.shields.io/badge/Python-3-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

# SentinelIR

SentinelIR is a Python-based incident response and SOC investigation toolkit for analysing authentication logs, monitoring security activity in real time, generating attack scenarios, and supporting defensive investigation workflows.

The project started as a Linux authentication log analyser and is evolving into a lightweight live incident response tool. It is designed around clean software architecture, modular detection logic, configurable thresholds, live monitoring, and test-driven development.

---

# Overview

SentinelIR focuses on helping a security analyst investigate authentication-based activity such as:

- Brute-force login attempts
- Suspicious IP activity
- Successful logins after failed attempts
- Distributed user-targeting attacks
- Password spraying-style behaviour
- Live log changes during monitoring
- Generated attack scenarios for testing detections

The long-term direction is to expand SentinelIR into a broader investigation platform that can support log analysis, file triage, hash/signature scanning, IOC enrichment, and a future GUI.

---

# Current Features

## Static Log Analysis

- Parses Linux-style authentication logs
- Extracts failed login events
- Extracts successful login events
- Groups failed login attempts by IP address
- Builds activity timelines
- Supports filtering by:
  - IP address
  - Username
  - Severity
  - Status
  - Time range

## Detection

- Detects brute-force login attacks
- Detects suspicious IP addresses
- Detects successful logins following failed attempts
- Detects distributed user-targeting attacks
- Calculates severity levels
- Tracks alert state during live monitoring
- Suppresses duplicate live alerts

## Live Monitoring

- Watches a log file for new events
- Processes new log lines as they arrive
- Runs detections immediately against live state
- Prints live alerts when suspicious behaviour is detected
- Displays periodic live monitoring status
- Prints a live session summary when monitoring ends

# Scenario Generator

- Generates realistic SSH authentication log scenarios
- Supports:
  - Brute-force scenario
  - Suspicious-success scenario
  - User-targeting scenario
  - Normal activity scenario
  - Mixed attack scenario
- Can write generated logs instantly
- Can stream generated logs slowly into a file
- Supports append or overwrite mode
- Supports custom stream delay
- Includes scenario preview and confirmation

## Reporting

- Interactive CLI reports
- Attack summaries
- Attack statistics
- TXT report export
- JSON report export

## Testing

- Unit tests for detection logic
- Unit tests for filtering
- Unit tests for report exports
- Unit tests for live event processing
- Unit tests for scenario generation
- Unit tests for file writing and streaming

---

# Project Structure

```text
log-analyser/
├── app/
│   ├── config/
│   ├── detection/
│   ├── generator/
│   ├── interaction/
│   ├── log_analyser/
│   ├── models/
│   ├── monitoring/
│   ├── reporting/
│   ├── runtime/
│   ├── utils/
│   └── main.py
│
├── log_files/
├── logs/
├── reports/
├── tests/
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Architecture

SentinelIR uses a modular architecture to separate core responsibilities.

## Runtime Layer

Responsible for selecting how the application runs.

Current runtime modes:

```text
1. Static Analysis
2. Live Monitoring
3. Generate Scenario
4. Exit
```

Key files:

```text
app/runtime/runtime_controller.py
app/runtime/static_runtime.py
app/runtime/live_runtime.py
app/runtime/generator_runtime.py
```

---

## Log Analysis Layer

Responsible for parsing log files and storing structured authentication events.

Key files:

```text
app/log_analyser/log_analyser.py
app/log_analyser/log_entry.py
app/log_analyser/filtering.py
```

The analyser extracts:

- IP address
- Username
- Timestamp
- Authentication status
- Severity

---

## Detection Layer

Responsible for identifying suspicious behaviour.

Key files:

```text
app/detection/detection_engine.py
app/detection/alert_types.py
```

Current detections include:

- Brute-force detection
- Suspicious success detection
- User-targeting detection
- Live alert suppression
- Alert state tracking

---

## Monitoring Layer

Responsible for real time file monitoring and event processing.

Key files:

```text
app/monitoring/file_monitor.py
app/monitoring/live_event_processor.py
```

The monitoring layer watches a target log file, processes new lines as they arrive, and passes live events into the detection engine.

---

## Generator Layer 

Responsible for creating controlled log scenarios for testing and demonstrations.

Key files:

```text
app/generator/scenarios.py
app/generator/log_generator.py
```

This allows SentinelIR to simulate realistic attack activity and stream it into a monitored log file.

---

## Reporting Layer

Responsible for presenting investigation findings and exporting results.

Key files:

```text
app/reporting/statistics.py
app/reporting/detection.py
app/reporting/investigation.py
app/reporting/exports.py
app/reporting/summary.py
```

---

# Detection Logic

## Brute-Force Detection

Brute-force detection identifies repeated failed login attempts from the same IP address.

Example:

```text
192.168.1.10 -> 5 attempts within 10 seconds
```

In live monitoring mode, the alert fires once for the attacking IP and is then suppressed to prevent duplicate alert spam.

---

## Suspicious Success Detection

Suspicious-success detection identifies successful logins from IP addresses that previously failed authentication.

This may include:

- Credential guessing
- Password compromise
- Successful brute-force attempts
- Suspicious authentication behaviour

---

## User-Targeting Detection

User-targeting detection identifies one username being attacked by multiple IP addresses.

This models:

- Password spraying
- Distributed account targeting
- Coordinated authentication attacks

Example:

```text
admin targeted by 5 unique IP addresses
```

---

# Live Monitoring Workflow

Terminal 1:

```bash
python3 -m app.main generated.log
```

Select:

```text
2. Live Monitoring
```

Terminal 2:

```bash
python3 -m app.main generated.log
```

Select:

```text
3. Generate Scenario
5. Mixed attack
```

Then choose:

```text
Overwrite existing file
Stream slowly
Delay: 0.5 seconds
```

Expected live alerts:

```text
[HIGH] Brute Force Detected
[MEDIUM] Suspicious Success Detected
[HIGH] User Targeting Detected
```

When live monitoring stops, SentinelIR prints a live summary showing processed events, failed logins, successful logins, unique IPs, and alert counts.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Pixsl-Labs/SentinelIR.git
cd SentinelIR
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Usage

Run SentinelIR with a target log file:

```bash
python3 -m app.main <log_file>
```

Example:

```bash
python3 -m app.main brute_force.log
```

You will then be asked to choose a runtime mode:

```text
1. Static Analysis
2. Live Monitoring
3. Generate Scenario
4. Config Monitoring
5. Exit
```

---

## Static Analysis Mode

Static analysis reads an existing log file and opens the investigation menu.

Example:

```bash
python3 -m app.main brute_force.log
```

Select:

```text
1. Static Analysis
```

This allows you to view:

- Full report
- Attack summary
- Attack statistics
- Activity timeline
- Failed login details
- Suspicious IPs
- Brute-force detections
- User-targeting detections
- Successful logins
- Export options

---

## Live Monitoring Mode

Live monitoring watches a log file for new lines.

Example:

```bash
python3 -m app.main generated.log
```

Select:

```text
2. Live Monitoring
```

SentinelIR will monitor the file and process new authentication events in real time.

---

## Scenario Generator Mode

Scenario generator mode creates test authentication logs.

Example:

```bash
python3 -m app.main generated.log
```

Select:

```text
3. Generate Scenario
```

Available scenarios:

```text
1. Brute force
2. Suspicious success
3. User targeting
4. Normal activity
5. Mixed attack
```

Output options:

```text
1. Write instantly
2. Stream slowly
```

File modes:

```text
1. Append to existing file
2. Overwrite existing file
```

---

## Report Exporting

SentinelIR can export investigation data to TXT or JSON.

TXT reports are human-readable.

JSON reports are structured for further processing.

Example report paths:

```text
reports/report.txt
reports/generated.json
```

---

# Testing

Run all tests:

```bash
pytest
```

Run specific test groups:

```bash
pytest tests/test_live_event_processor.py
pytest tests/test_scenarios.py
pytest tests/test_log_generator.py
```

Current tested areas include:

- Brute-force detection
- User-targeting detection
- Suspicious-success detection
- Severity classification
- Filtering
- Exporting reports
- Malformed log handling
- Live event processing
- Live alert state tracking
- Scenario generation
- Log writing and streaming

--- 

# Design Goals

SentinelIR is designed to demonstrate:

- Practical cyber security tooling
- Incident response investigation workflows
- Detection engineering principles
- Clean Python architecture
- Modular software design
- Test-driven development
- Live event processing
- Extensible investigation features

The goal is not to build a full enterprise SIEM. The goal is to build a focused, lightweight investigation tool that demonstrates how suspicious authentication activity can be parsed, monitored, detected, and reported.

---

# Dissertation Direction

SentinelIR is being developed as a potential final-year cyber security dissertation project.

Possible research direction:

```text
Design and Evaluation of SentinelIR: A Lightweight Live Incident Response and SOC Investigation Toolkit
```

The project can support investigation into:

- Rule-based detection
- Behaviour-based anomaly detection
- Authentication attack detection
- Live incident response workflows
- Usability of security investigation tools
- Evaluation of lightweight SOC tooling

---

# Future Improvements

Planned or possible future work includes:

- GUI interface
- Cross-platform log support
- Windows Event Log support
- macOS log support
- Multi-file investigation
- Case management
- File hash generation
- Signature scanning
- VirusTotal-style enrichment
- IOC extraction
- Dashboard-style investigation view
- Advanced anomaly detection
- Baseline profiling
- Alert cooldown windows
- Persistent storage
- Docker support
- Standalone packaged application

---

# Limitations

Current limitations:

- Primarily supports Linux-style SSH authentication logs
- Detection rules are heuristic-based
- No database or persistent case storage yet
- No GUI yet
- No cross-platform event parsing yet
- No external threat intelligence enrichment yet
- No file scanning yet

---

# Technologies Used

- Python 3
- argparse
- logging
- dataclasses
- pytest
- JSON
- colorama

---

# Author

Samuel Stacey

Cyber Security student focused on detection engineering, incident response tooling, Linux, secure software development, and practical cyber security investigation workflows.
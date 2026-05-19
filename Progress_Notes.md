# Dissertation Meeting Prep

## One-Line Project Summary

Python-based authentication log analysis and threat investigation tool focused on detection engineering, investigation workflows, and suspicious authentication behaviour.

---

# Current Features

## Detection

* Brute-force detection
* Suspicious IP detection
* User-targeting detection
* Suspicious success detection
* Severity classification

## Investigation Features

* IP filtering
* Username filtering
* Severity filtering
* Status filtering
* Time-range filtering

## Reporting

* Full reports
* Attack summaries
* Attack statistics
* TXT export
* JSON export

## Engineering Improvements

* Modular architecture
* Shared filtering utilities
* Shared colour utilities
* Dataclasses
* Automated tests
* Configurable thresholds
* CLI UX improvements

---

# Current Architecture

## LogAnalyser

* Parses authentication logs
* Extracts structured events
* Stores failed/successful logins

## LogReporter

* Detection logic
* Investigation workflows
* Reporting/export logic

## Interaction Layer

* CLI menus
* Validation
* User workflows

---

# What I Want To Explore Next

## Short-Term

* Table-style CLI formatting
* Better reporting UX
* Improved threat scoring
* More testing

## Medium-Term

* Live log monitoring
* Real-time detection
* Event correlation
* Multi-file analysis
* Improved anomaly detection

## Long-Term / Dissertation Direction

* Realistic SOC-style investigation workflows
* Behaviour-based detection
* Detection engineering concepts
* Potential lightweight SIEM-style features

---

# Technologies Used

* Python
* argparse
* dataclasses
* pytest
* colorama
* JSON

---

# Why This Project

* Interested in detection engineering
* Enjoy backend/system-level security
* Wanted practical cyber tooling experience
* Strong overlap with security operations and defence work

---

# Good Talking Points

* Started as a small CLI parser and evolved into a modular investigation tool
* Focused heavily on clean architecture and maintainability
* Wanted to emulate realistic investigation workflows rather than just detection scripts
* Tried to keep the project extensible for future features
* Interested in evolving toward real-time monitoring and correlation

---

# Questions To Ask

* Recommended academic direction?
* Recommended research areas/papers?
* Whether live monitoring/correlation is realistic for dissertation scope?
* Suggested evaluation methodology?
* Suggestions for balancing engineering vs research depth?


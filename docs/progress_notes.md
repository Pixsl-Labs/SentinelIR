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





# Notes from meeting with Kabiru

Event files -> different onces across OS -> explore different based on the system

GUI + website -> future -> GUI first! -> makes it easier than CLI -> (advantages of transforming into a website!)

Existing literature -> gaps in current tools / solutions (incident repsonse) -> compare! + new ideas for mine -> output not as good -> hightlight those gaps! MAKE HEAD WAY WITH THE REPORT

Start methodology of the report -> discussing tools / flow / data produced + input

Expand: not just log files but signature scanning (VirusTotal) -> produce an output (Focus on investigation not just log files) -> assess different files / ways / SOC environment -> attack vectors (one home for the SOC worker)

Pentesting IOE -> report provided!

Next steps: GUI + start the report! -> analyse similar tools + objectives -> areas to expand + additionally functionality

Add my own terminal -> shortcuts + CLI used already!

Make into a real-software (downloaded) all in one stand alone software -> Pushing the edge -> extreme marks -> distribute throughout to different students -> feedback (effectiveness / security needs!) -> unit test

SDLC -> software development life cycle -> suitable project management development -> solo! -> Project management section! -> GUI (Usability testing!) -> Cyber security focused project:


Methodology adopted
Evaluation of the sofware itself
Tutorials


Agile (maybe) -> not really suitable
Waterfall


Name: Final Year Dissertation


Tips / Ticks:

Right track -> ahead -> carry on!
Don't discuss how far I've gone with the module!
Focus purely on investigation area!



Third Yr Timeline:

2 Project modules (40 Credits Total):

Sept -> December:

Prep -> project ideas proposal literature review reserach -> 1.5/2k words
Security Audit + Monitoring:
Optional Module: Reverse Engineering!


Jan -> March: Project Delivery: 8k words -> flexible (as much as they can!)
Advanced Pen Testing
Applied Cryptography


Merit: 60-69%



Live Incident Response -> make a real name ...


Research: Undergraduate Cyber Security Dissertation (Coding focused if I can find it!)


Versital cross platform (OS)!


# Docstring Cheat Sheet

analyser: Log analyser instance containing failed login entries.

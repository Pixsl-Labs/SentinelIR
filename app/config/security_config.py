"""
Stores default security detection configuration values.

This module defines threshold values used across SentinelIR detection logic,
including brute-force attempts limits, time window, user-targeting thresholds,
severity boundaries, and suspicious login hours.
"""

BRUTE_FORCE_THRESHOLD = 5

BRUTE_FORCE_TIME_WINDOW = 10

USER_TARGETING_THRESHOLD = 5

SEVERITY_LEVELS = {
    "LOW": 5,
    "MEDIUM": 10,
    "HIGH": 20
}

SUSPICIOUS_HOURS = [
    0,
    1,
    2,
    3,
    4
]
"""
Defines alert type constants used by the live detection engine.

These constants identify each live alert category so alert state can be tracked
and duplicate alerts can be suppressed consistently.
"""

BRUTE_FORCE_ALERT = "BRUTE_FORCE"
SUSPICIOUS_SUCCESS_ALERT = "SUSPICIOUS_SUCCESS"
USER_TARGETING_ALERT = "USER_TARGETING"

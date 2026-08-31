from dataclasses import dataclass


@dataclass
class DetectionResult:
    """
    Base result model for detection outputs.

    Stores shared detection fields used by more specific detection result types,
    including the number of attempts linked to the findings and its calculated
    severity level.
    """
    attempts: int
    severity: str


@dataclass
class SuspiciousIPResult(DetectionResult):
    """
    Represents a suspicious IP detection result.

    Stores the source service, IP address, failed attempt count, severity level,
    and risk status for an IP address that appears suspicious during authentication analysis.
    """
    service: str
    ip: str
    risk_status: str


@dataclass
class BruteForceResult(DetectionResult):
    """
    Represents a brute-force detection result.

    Stores the source service attacking IP address, failed attempt count,
    detection time window, and severity level for repeated login failures
    within a configured period.
    """
    ip: str
    time_window: float
    service: str = "UNKNOWN"


@dataclass
class UserTargetingResult(DetectionResult):
    """
    Represents a distributed user-targeting detection result.

    Stores the source service, targeted username, total failed attempts,
    number of unique attacking IP addresses, and severity level for
    password spraying or coordinated account targeting behaviour.
    """
    username: str
    unique_ips: int
    service: str = "UNKNOWN"


@dataclass
class SuspiciousSuccessResult(DetectionResult):
    """
    Represents a suspicious-success detection result.

    Stores the source service, IP address, attempt count, and severity level for
    a successful login that occurred after previous failed authentication activity from the same IP.
    """
    ip: str
    service: str = "UNKNOWN"


@dataclass
class AnonymousFTPResult(DetectionResult):
    """
    Represents an anonymous FTP login detection result.

    Stores the IP address and username linked to a successful anonymous FTP login.
    """
    ip: str
    username: str

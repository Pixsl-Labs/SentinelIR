from dataclasses import dataclass


@dataclass
class DetectionResult:
    attempts: int
    severity: str


@dataclass
class SuspiciousIPResult(DetectionResult):
    ip: str
    risk_status: str


@dataclass
class BruteForceResult(DetectionResult):
    ip: str
    time_window: float


@dataclass
class UserTargetingResult(DetectionResult):
    username: str
    unique_ips: int


@dataclass
class SuspiciousSuccessResult(DetectionResult):
    ip: str
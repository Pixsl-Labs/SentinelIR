from dataclasses import dataclass


@dataclass
class TargetedUserResult:
    username: str
    attempts: int
    severity: str


@dataclass
class FailedLoginSummaryResult:
    username: str
    ip: str
    attempts: int
    severity: str
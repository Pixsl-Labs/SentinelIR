from dataclasses import dataclass


@dataclass
class TargetedUserResult:
    username: str
    attempts: int
    severity: str
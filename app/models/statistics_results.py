from dataclasses import dataclass


@dataclass
class TargetedUserResult:
    """
    Represents a targeted user statistics result.

    Stores a username, the number of failed attempts linked to that user,
    the calculated severity level, and source service.
    """
    username: str
    attempts: int
    severity: str
    service: str = "UNKNOWN"


@dataclass
class FailedLoginSummaryResult:
    """
    Represents a grouped failed login summary result.

    Stores a username and IP address pair, the number of failed attempts for that
    pair, the calculated severity level, and source service.
    """
    username: str
    ip: str
    attempts: int
    severity: str
    service: str = "UNKNOWN"
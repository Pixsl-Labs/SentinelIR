from dataclasses import dataclass


@dataclass
class TargetedUserResult:
    """
    Represents a targeted user statistics result.

    Stores a username, the number of failed attempts linked to that user,
    and the calculated severity level.
    """
    username: str
    attempts: int
    severity: str


@dataclass
class FailedLoginSummaryResult:
    """
    Represents a grouped failed login summary result.

    Stores a username and IP address pair, the number of failed attempts for that
    pair, and the calculated severity level.
    """
    username: str
    ip: str
    attempts: int
    severity: str
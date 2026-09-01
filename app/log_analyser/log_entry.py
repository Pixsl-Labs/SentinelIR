from datetime import datetime
from dataclasses import dataclass

from app.models.enums import (
    Service,
    AuthenticationStatus
)


@dataclass
class LogEntry:
    """
    Represents a parsed authentication log event.

    Stores the key fields extracted from a log line, including source IP address,
    username, timestamp, login status, severity level, source service, method,
    path, and status code.
    """

    ip: str
    user: str
    timestamp: datetime
    status: AuthenticationStatus
    severity: str = "LOW"
    service: Service = Service.SSH
    method: str | None = None
    path: str | None = None
    status_code: int | None = None

from enum import StrEnum


class Service(StrEnum):
    SSH = "SSH"
    FTP = "FTP"
    HTTP = "HTTP"


class AuthenticationStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class AlertType(StrEnum):
    BRUTE_FORCE = "BRUTE_FORCE"
    SUSPICIOUS_SUCCESS = "SUSPICIOUS_SUCCESS"
    USER_TARGETING = "USER_TARGETING"
    ANONYMOUS_FTP = "ANONYMOUS_FTP"


class OperationResult(StrEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    NOT_FOUND = "NOT_FOUND"
    INVALID = "INVALID"


class Severity(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

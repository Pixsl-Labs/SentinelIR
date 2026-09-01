from enum import Enum

class Service(str, Enum):
    SSH = "SSH"
    FTP = "FTP"
    HTTP = "HTTP"

class AuthenticationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class AlertType(str, Enum):
    BRUTE_FORCE = "BRUTE_FORCE"
    SUSPICIOUS_SUCCESS = "SUSPICIOUS_SUCCESS"
    USER_TARGETING = "USER_TARGETING"
    ANONYMOUS_FTP = "ANONYMOUS_FTP"

class OperationResult(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    NOT_FOUND = "NOT_FOUND"
    INVALID = "INVALID"

from app.config.security_config import SEVERITY_LEVELS


def get_severity_level(count: int) -> str:
    """
    Returns severity level based on attempt count.
    """

    if count >= SEVERITY_LEVELS["HIGH"]:
        return "HIGH"

    elif count >= SEVERITY_LEVELS["MEDIUM"]:
        return "MEDIUM"

    return "LOW"
from app.config import SEVERITY_LEVEL


def get_severity_level(count: int) -> str:
    """
    Returns severity level based on attempt count.
    """

    if count >= SEVERITY_LEVEL["HIGH"]:
        return "HIGH"

    elif count >= SEVERITY_LEVEL["MEDIUM"]:
        return "MEDIUM"

    return "LOW"
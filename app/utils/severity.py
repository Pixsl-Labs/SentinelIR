from app.config.security_config import SEVERITY_LEVELS


def get_severity_level(count: int) -> str:
    """
    Returns a severity level based on an attempt count.

    Compares the supplied count against the configured severity thresholds and
    returns the matching severity label.

    Args:
        count (int): Number of attempts to assess.

    Returns:
        str: Severity level, such as LOW, MEDIUM, or HIGH.
    """

    if count >= SEVERITY_LEVELS["HIGH"]:
        return "HIGH"

    elif count >= SEVERITY_LEVELS["MEDIUM"]:
        return "MEDIUM"

    return "LOW"

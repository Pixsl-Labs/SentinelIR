from app.config.security_config import BRUTE_FORCE_THRESHOLD


def get_risk_level(count: int) -> str:
    """
    Returns a risk label based on the number of failed attempts.

    Compares the supplied attempt count against the configured brute-force
    threshold. Counts meeting or exceeding the threshold are marked for
    investigation, while lower counts are treated as low risk.

    Args:
        count (int): Number of failed attempts to assess.

    Returns:
        str: Risk label for the attempt count.
    """
    return "Investigate" if count >= BRUTE_FORCE_THRESHOLD else "Low risk"

from app.config.security_config import BRUTE_FORCE_THRESHOLD


def get_risk_level(count: int) -> str:
    """
    Returns the risk level based on the number of attempts

    Returns:
        str: Risk level
    """
    return "Investigate" if count >= BRUTE_FORCE_THRESHOLD else "Low risk"
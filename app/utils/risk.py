from app.config import MAX_ATTEMPTS


def get_risk_level(count: int) -> str:
    """
    Returns the risk level based on the number of attempts

    Returns:
        str: Risk level
    """
    return "Investigate" if count >= MAX_ATTEMPTS else "Low risk"
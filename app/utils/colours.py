from colorama import Fore


def get_severity_colour(
    severity: str
) -> str:
    """
    Returns a display colour for a severity level.

    Args:
        severity (str): Severity value, such as LOW, MEDIUM, or HIGH.

    Returns:
        str: Colorama colour matching the severity level.
    """

    if severity == "HIGH":
        return Fore.LIGHTRED_EX

    elif severity == "MEDIUM":
        return Fore.YELLOW

    elif severity == "LOW":
        return Fore.GREEN

    return Fore.WHITE


def get_status_colour(
    status: str
) -> str:
    """
    Returns a display colour for a login status.

    Args:
        status (str): Login status, such as FAILED or SUCCESS.

    Returns:
        str: Colorama colour matching the login status.
    """

    if status.upper() == "FAILED":
        return Fore.LIGHTRED_EX

    elif status.upper() == "SUCCESS":
        return Fore.GREEN

    return Fore.WHITE

def get_attempt_colour(
    count: int
) -> str:
    """
    Returns a display colour based on an attempt count.

    Higher attempt counts return stronger warning colours so suspicious activity
    stands out in reports.

    Args:
        count (int): Number of attempts to evaluate.

    Returns:
        str: Colorama colour matching the attempt count.
    """

    if count >= 15:
        return Fore.LIGHTRED_EX

    elif count >= 10:
        return Fore.RED

    elif count >= 5:
        return Fore.LIGHTYELLOW_EX

    return Fore.LIGHTGREEN_EX

def get_count_colour(
    count: int
) -> str:
    """
    Returns a display colour based on a general count value.

    This is used for totals such as detected alerts, suspicious IPs, or grouped
    result counts.

    Args:
        count (int): Count value to evaluate.

    Returns:
        str: Colorama colour matching the count level.
    """

    if count >= 20:
        return Fore.LIGHTRED_EX

    elif count >= 10:
        return Fore.YELLOW

    elif count >= 1:
        return Fore.CYAN

    return Fore.LIGHTBLACK_EX

def get_live_status_colour(
        label: str,
        value: int
) -> str:
    """
    Returns a display colour for live monitoring status values.

    The colour is selected using the status label and its numeric value so live
    monitoring summaries can highlight events, failures, successes, unique IPs,
    and alerts clearly.

    Args:
        label (str): Live status label being displayed.
        value (int): Numeric value linked to the label.

    Returns:
        str: Colorama colour matching the live status type and value.
    """

    label = label.lower()

    if label == "events_processed":
        return Fore.CYAN

    if label == "failed_logins":
        return get_attempt_colour(value)

    if label == "successful_logins":
        return Fore.GREEN if value > 0 else Fore.LIGHTRED_EX

    if label == "unique_ips":
        return get_count_colour(value)

    if label == "alerts_raised":
        if value >= 3:
            return Fore.LIGHTRED_EX

        if value >= 1:
            return Fore.YELLOW
        return Fore.LIGHTBLACK_EX

    if label == "brute_force_alert":
        return get_count_colour(value)

    if label == "suspicious_success":
        return get_count_colour(value)

    if label == "user_targeting":
        return get_count_colour(value)

    return Fore.WHITE

def get_service_colour(service: str | None) -> str:
    """
    Returns a colour for a log service.

    Args:
        service (str | None): Service name such as SSH, FTP, or HTTP.

    Returns:
        str: Colorama foreground colour.
    """

    service = (
        service or "UNKNOWN"
    ).upper()

    if service == "SSH":

        return Fore.LIGHTCYAN_EX

    if service == "FTP":

        return Fore.LIGHTMAGENTA_EX

    if service == "HTTP":

        return Fore.LIGHTBLUE_EX

    return Fore.WHITE

def get_user_colour(user: str | None) -> str:
    """
    Returns a colour for a user.

    Args:
        user (str | None): Username such as root, admin, and others.

    Returns:
        str: Colorama foreground colour.
    """

    user = (
        user or "unknown"
    ).lower()

    if user == "root":

        return Fore.RED

    if user == "admin":

        return Fore.LIGHTRED_EX

    if user == "deploy":

        return Fore.LIGHTYELLOW_EX

    if user == "anonymous":

        return Fore.LIGHTMAGENTA_EX

    if user == "guest":

        return Fore.LIGHTGREEN_EX

    if user == "unknown":

        return Fore.LIGHTBLACK_EX

    return Fore.WHITE

def get_status_code_colour(status_code: str | None) -> str:
    """
    Returns a colour for a status code based on standard conventions.

    Args:
        status_code (str | None): Status code such as '200', '401', '500'.

    Returns:
        str: Colorama foreground colour.
    """

    if status_code is None:

        return Fore.WHITE

    try:

        code = int(status_code)

    except ValueError:

        return Fore.WHITE

    if 200 <= code <= 300:

        return Fore.LIGHTGREEN_EX

    elif 300 <= code <= 400:

        return Fore.LIGHTCYAN_EX

    elif 400 <= code <= 500:

        return Fore.LIGHTYELLOW_EX

    elif 500 <= code <= 600:

        return Fore.LIGHTRED_EX

    return Fore.WHITE

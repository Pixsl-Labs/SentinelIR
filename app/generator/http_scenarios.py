from datetime import datetime, timedelta


def format_http_timestamp(timestamp: datetime) -> str:
    """
    Formats a datetime object using HTTP access-log timestamp format.

    Example:
        16/Apr/2026:12:01:00

    Args:
        timestamp (datetime): Timestamp to format.

    Returns:
        str: Formatted HTTP access-log timestamp.
    """

    return timestamp.strftime("%d/%b/%Y:%H:%M:%S")

def generate_http_failed_scenario(
        ip: str = "192.168.1.45",
        user: str = "root",
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a single failed HTTP login scenario.

    Creates one failed HTTP authentication event for the selected username and
    source IP address. This can be used to test basic HTTP failed-login parsing,
    failed login storage, suspicious IP tracking, and severity assignment.

    Args:
        ip (str): Source IP address used in the failed HTTP login event.
            Defaults to "192.168.1.45".
        user (str): Username used in the failed HTTP login event.
            Defaults to "root".
        start_time (datetime | None): Timestamp for the generated log line.
            Defaults to None.

    Returns:
        list[str]: Generated HTTP access log line.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 13, 22, 5, 0)

    formatted_time = format_http_timestamp(start_time)

    line = (
            f'{ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'401 532'
    )

    return [line]

def generate_http_success_scenario(
        ip: str = "192.168.1.34",
        user: str = "guest",
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a single successful HTTP login scenario.

    Creates one successful HTTP authentication event for the selected username and
    source IP address. This can be used to test HTTP success parsing, successful
    login storage, and normal HTTP authentication activity.

    Args:
        ip (str): Source IP address used in the successful HTTP login event.
            Defaults to "192.168.1.34".
        user (str): Username used in the successful HTTP login event.
            Defaults to "guest".
        start_time (datetime | None): Timestamp for the generated log line.
            Defaults to None.

    Returns:
        list[str]: Generated HTTP access log line.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 13, 19, 5, 0)

    formatted_time = format_http_timestamp(start_time)

    line = (
            f'{ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'200 532'
    )

    return [line]

def generate_http_brute_force_scenario(
        ip: str = "203.0.113.11",
        user: str = "admin",
        attempts: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a brute-force HTTP login scenario.

    Creates multiple failed login attempts from the same IP address against the
    same username. This can be used to test brute-force detection rules and
    alerting behaviour.

    Args:
        ip (str): Source IP address used in the generated attack.
            Defaults to "203.0.113.11".
        user (str): Username targeted by the failed login attempts.
            Defaults to "admin".
        attempts (int): Number of failed login attempts to generate.
            Defaults to 5.
        start_time (datetime | None): Timestamp for the first generated
            log lines. Defaults to None.

    Returns:
        list[str]: Generated HTTP access log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 12, 12, 0, 0)

    lines = []

    for event_number in range(attempts):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%d/%b/%Y:%H:%M:%S")

        line = (
            f'{ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'401 532'
        )

        lines.append(line)

    return lines

def generate_http_suspicious_success_scenario(
        ip: str = "203.0.113.20",
        user: str = "guest",
        failed_attempts: int = 3,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a suspicious-success HTTP login scenario.

    Creates several failed login attempts from one IP address followed by a
    successful login from the same IP address. This simulates possible credential
    compromise after repeated authentication failures.

    Args:
        ip (str): Source IP address used for the failed and successful
            login events. Defaults to "203.0.113.20".
        user (str): Username used in the generated authentication events.
            Defaults to "guest".
        failed_attempts (int): Number of failed login attempts to generate
            before the successful login. Defaults to 3.
        start_time (datetime | None): Timestamp for the first generated
            log line. Defaults to None.

    Returns:
        list[str]: Generated HTTP access log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 13, 12, 0, 0)

    lines = []

    for event_number in range(failed_attempts):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = format_http_timestamp(timestamp)

        failed_line = (
            f'{ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'401 532'
        )

        lines.append(failed_line)

    success_time = start_time + timedelta(seconds=failed_attempts)
    formatted_time = format_http_timestamp(success_time)

    successful_line = (
        f'{ip} - - '
        f'[{formatted_time} +0000] '
        f'"POST /login?user={user} HTTP/1.1" '
        f'200 532'
    )

    lines.append(successful_line)

    return lines

def generate_http_user_targeting_scenario(
        user: str = "admin",
        base_ip: str = "203.0.113.",
        unique_ips: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a distributed user-targeting HTTP login scenario.

    Creates failed login attempts against the same username from multiple unique
    IP addresses. This simulates password spraying or coordinated account
    targeting behaviour.

    Args:
        user (str): Username targeted by the generated failed logins.
            Defaults to "admin".
        base_ip (str): Base IP prefix used to generate unique source IPs.
            Defaults to "203.0.113.".
        unique_ips (int): Number of unique source IP addresses to generate.
            Defaults to 5.
        start_time (datetime | None): Timestamp for the first generated
            log line. Defaults to None.

    Returns:
        list[str]: Generated HTTP access log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 14, 12, 0, 0)

    lines = []

    initial_ip = 1

    for event_number in range(unique_ips):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = format_http_timestamp(timestamp)

        line = (
            f'{base_ip}{initial_ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'401 532'
        )

        lines.append(line)

        initial_ip += 1

    return lines

def generate_http_normal_activity(
        users: list[str] | None = None,
        ips: list[str] | None = None,
        events: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates normal HTTP authentication activity.

    Creates successful login events from expected users and IP addresses.
    This can be used to test that detection logic does not raise alerts for normal
    authentication behaviour.

    Args:
        users (list[str] | None): Usernames to rotate through when
            generating successful login events. Defaults to None.
        ips (list[str] | None): IP addresses to rotate through when
            generating successful login events. Defaults to None.
        events (int): Number of normal login events to generate.
            Defaults to 5.
        start_time (datetime | None): Timestamp for the first generated
            log line. Defaults to None.

    Returns:
        list[str]: Generated HTTP access log lines.
    """

    if users is None:
        users = ["guest", "admin", "deploy"]

    if ips is None:
        ips = ["192.168.2.4", "192.168.2.6", "192.168.5.7"]

    if start_time is None:
        start_time = datetime(2026, 4, 15, 12, 0, 0)

    lines = []

    for event_number in range(events):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = format_http_timestamp(timestamp)

        user = users[event_number % len(users)]

        ip = ips[event_number % len(ips)]

        line = (
            f'{ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'200 532'
        )

        lines.append(line)

    return lines

def generate_http_mixed_attack_scenario(
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a mixed HTTP authentication scenario.

    Combines normal login activity, brute-force behaviour, suspicious-success
    behaviour, and distributed user-targeting activity into one realistic test
    sequence.

    Args:
        start_time (datetime | None): Timestamp used as the base time for
            the generated scenario. Defaults to None.

    Returns:
        list[str]: Generated HTTP access log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 16, 12, 0, 0)

    lines = []

    # Normal activity

    lines.extend(
        generate_http_normal_activity(
            events=3,
            start_time=start_time
        )
    )

    # Failed login

    lines.extend(
        generate_http_failed_scenario(
            ip="192.168.1.45",
            user="root"
        )
    )

    # Successful login

    lines.extend(
        generate_http_success_scenario(
            ip="192.168.1.34",
            user="guest"
        )
    )

    # Brute-force

    lines.extend(
        generate_http_brute_force_scenario(
            ip="203.0.113.11",
            user="admin",
            attempts=5,
            start_time=start_time + timedelta(minutes=1)
        )
    )

    # Suspicious-success

    lines.extend(
        generate_http_suspicious_success_scenario(
            ip="203.0.113.20",
            user="guest",
            failed_attempts=3,
            start_time=start_time + timedelta(minutes=2)
        )
    )

    # User-targeting

    lines.extend(
        generate_http_user_targeting_scenario(
            user="admin",
            base_ip="203.0.113.",
            unique_ips=5,
            start_time=start_time + timedelta(minutes=3)
        )
    )

    # Normal activity

    lines.extend(
        generate_http_normal_activity(
            events=3,
            start_time=start_time + timedelta(minutes=4)
        )
    )

    return lines
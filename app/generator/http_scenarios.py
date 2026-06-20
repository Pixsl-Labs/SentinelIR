from datetime import datetime, timedelta


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
        list[str]: Generated HTTP authentication log lines.
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
        list[str]: Generated HTTP authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 13, 12, 0, 0)

    lines = []

    for event_number in range(failed_attempts):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

        failed_line = (
            f'{ip} - - '
            f'[{formatted_time} +0000] '
            f'"POST /login?user={user} HTTP/1.1" '
            f'401 532'
        )

        lines.append(failed_line)

    success_time = start_time + timedelta(seconds=failed_attempts)
    formatted_time = success_time.strftime("%b %d %Y %H:%M:%S")

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
        list[str]: Generated HTTP authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 14, 12, 0, 0)

    lines = []

    initial_ip = 1

    for event_number in range(unique_ips):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

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
        list[str]: Generated HTTP authentication log lines.
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

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

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
        list[str]: Generated HTTP authentication log lines.
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
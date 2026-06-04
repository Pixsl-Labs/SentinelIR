from datetime import datetime, timedelta


def generate_brute_force_scenario(
        ip: str = "192.168.1.10",
        user: str = "root",
        attempts: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a brute-force SSH login scenario.

    Creates multiple failed login attempts from the same IP address against the
    same username. This can be used to test brute-force detection rules and
    alerting behaviour.

    Args:
        ip (str): Source IP address used in the generated attack.
            Defaults to "192.168.1.10".
        user (str): Username targeted by the failed login attempts.
            Defaults to "root".
        attempts (int): Number of failed login attempts to generate.
            Defaults to 5.
        start_time (datetime | None): Timestamp for the first generated
            log lines. Defaults to None.

    Returns:
        list[str]: Generated SSH authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 12, 12, 0, 0)

    lines = []

    for event_number in range(attempts):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

        line = (
            f"{formatted_time} server sshd[123]: "
            f"Failed password for {user} "
            f"from {ip} port 22 ssh2"
        )

        lines.append(line)

    return lines

def generate_suspicious_success_scenario(
        ip: str = "192.168.1.20",
        user: str = "deploy",
        failed_attempts: int = 3,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a suspicious-success SSH login scenario.

    Creates several failed login attempts from one IP address followed by a
    successful login from the same IP address. This simulates possible credential
    compromise after repeated authentication failures.

    Args:
        ip (str): Source IP address used for the failed and successful
            login events. Defaults to "192.168.1.20".
        user (str): Username used in the generated authentication events.
            Defaults to "deploy".
        failed_attempts (int): Number of failed login attemtps to generate
            before the successful login. Defaults to 3.
        start_time (datetime | None): Timestamp for the first generated
            log line. Defaults to None.

    Returns:
        list[str]: Generated SSH authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 13, 12, 0, 0)

    lines = []

    for event_number in range(failed_attempts):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

        failed_line = (
            f"{formatted_time} server sshd[124]: "
            f"Failed password for {user} "
            f"from {ip} port 22 ssh2"
        )

        lines.append(failed_line)

    success_time = start_time + timedelta(seconds=failed_attempts)
    formatted_time = success_time.strftime("%b %d %Y %H:%M:%S")

    successful_line = (
        f"{formatted_time} server sshd[124]: "
        f"Accepted password for {user} "
        f"from {ip} port 22 ssh2"
    )

    lines.append(successful_line)

    return lines

def generate_user_targeting_scenario(
        user: str = "admin",
        base_ip: str = "10.20.0.",
        unique_ips: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a distributed user-targeting SSH login scenario.

    Creates failed login attempts against the same username from multiple unqiue
    IP addressses. This simulates password spraying or coordinated account
    targeting behaviour.

    Args:
        user (str): Username targeted by the generated failed logins.
            Defaults to "admin".
        base_ip (str): Base IP prefix used to generate unique source IPs.
            Defaults to "10.20.0.".
        unique_ips (int): Number of unqiue source IP addresses to generate.
            Defaults to 5.
        start_time (datetime | None): Timestamp for the first generated
            log line. Defaults to None.

    Returns:
        list[str]: Generated SSH authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 14, 12, 0, 0)

    lines = []

    initial_ip = 1

    for event_number in range(unique_ips):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

        line = (
            f"{formatted_time} server sshd[123]: "
            f"Failed password for {user} "
            f"from {base_ip}{initial_ip} port 22 ssh2"
        )

        lines.append(line)

        initial_ip += 1

    return lines

def generate_normal_activity(
        users: list[str] | None = None,
        ips: list[str] | None = None,
        events: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates normal SSH authentication activity.

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
        list[str]: Generated SSH authentication log lines.
    """

    if users is None:
        users = ["guest", "admin", "deploy"]

    if ips is None:
        ips = ["192.168.1.5", "192.168.1.6", "192.168.1.7"]

    if start_time is None:
        start_time = datetime(2026, 4, 15, 12, 0, 0)

    lines = []

    for event_number in range(events):

        timestamp = start_time + timedelta(seconds=event_number)

        formatted_time = timestamp.strftime("%b %d %Y %H:%M:%S")

        user = users[event_number % len(users)]

        ip = ips[event_number % len(ips)]

        line = (
            f"{formatted_time} server sshd[123]: "
            f"Accepted password for {user} "
            f"from {ip} port 22 ssh2"
        )

        lines.append(line)

    return lines

def generate_mixed_attack_scenario(
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a mixed SSH authentication scenario.

    Combines normal login activity, brute-force behaviour, suspicious-success
    behaviour, and distributed user-targeting activity into one realistic test
    sequence.

    Args:
        start_time (datetime | None): Timestamp used as the base time for
            the generated scenario. Defaults to None.

    Returns:
        list[str]: Generated SSH authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 16, 12, 0, 0)

    lines = []

    # Normal activity

    lines.extend(
        generate_normal_activity(
            events=3,
            start_time=start_time
        )
    )

    # Brute-force

    lines.extend(
        generate_brute_force_scenario(
            ip="192.168.1.50",
            user="root",
            attempts=5,
            start_time=start_time + timedelta(minutes=1)
        )
    )

    # Suspicious-success

    lines.extend(
        generate_suspicious_success_scenario(
            ip="192.168.1.60",
            user="deploy",
            failed_attempts=3,
            start_time=start_time + timedelta(minutes=2)
        )
    )

    # User-targeting

    lines.extend(
        generate_user_targeting_scenario(
            user="admin",
            base_ip="10.20.0.",
            unique_ips=5,
            start_time=start_time + timedelta(minutes=3)
        )
    )

    # Normal activity

    lines.extend(
        generate_normal_activity(
            events=3,
            start_time=start_time + timedelta(minutes=4)
        )
    )

    return lines
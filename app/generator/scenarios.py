from datetime import datetime, timedelta


def generate_brute_force_scenario(
        ip: str = "192.168.1.10",
        user: str = "root",
        attempts: int = 5,
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a brute-force SSH login scenario.
    
    This creates multiple failed login attempts from the same IP
    against the same username.
    
    Returns:
        list[str]: Fake SSH authentication log lines.
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
    Generates a suspicious successful SSH login scenario.
    
    This creates several failed login attempts from one IP address,
    followed by a successful login from the same IP address. This
    simulates a possible credential compromise after repeated failures.
    
    Returns:
        list[str]: Fake SSH authentication log lines.
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
    Generates a user-targeting SSH login scenario.

    This creates failed login attempts against the same username from
    multiple different IP addresses. This simulates distributed user
    targeting or password-spraying behaviour.

    Returns:
        list[str]: Fake SSH authentication log lines.
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

    This creates benign authentication events such as successful logins
    from expected users and IP addresses. It can be used to test that
    the live detection engine does not alert on normal behaviour.

    Returns:
        list[str]: Fake SSH authentication log lines.
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
    Generates a mixed SSH attack scenario.

    This combines normal activity, brute-force behaviour, suspicious
    success behaviour, and distributed user-targeting activity into one
    realistic sequence of authentication events.

    Returns:
        list[str]: Fake SSH authentication log lines.
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
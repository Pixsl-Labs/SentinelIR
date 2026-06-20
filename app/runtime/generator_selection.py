from colorama import Fore
from datetime import datetime, timedelta

from app.generator.ssh_scenarios import (
    generate_ssh_brute_force_scenario,
    generate_ssh_mixed_attack_scenario,
    generate_ssh_normal_activity,
    generate_ssh_suspicious_success_scenario,
    generate_ssh_user_targeting_scenario,
    generate_ssh_failed_scenario,
    generate_ssh_success_scenario
)
from app.generator.ftp_scenarios import (
    generate_ftp_failed_scenario,
    generate_ftp_success_scenario,
    generate_anonymous_ftp_scenario,
    generate_ftp_brute_force_scenario,
    generate_ftp_mixed_attack_scenario,
    generate_ftp_normal_activity,
    generate_ftp_suspicious_success_scenario,
    generate_ftp_user_targeting_scenario,
)
from app.generator.http_scenarios import (
    generate_http_brute_force_scenario,
    generate_http_mixed_attack_scenario,
    generate_http_normal_activity,
    generate_http_suspicious_success_scenario,
    generate_http_user_targeting_scenario,
    generate_http_failed_scenario,
    generate_http_success_scenario
)

from app.utils.display import (
    print_section_header,
    print_empty_message
)


def select_scenario_type() -> str | None:
    """
    Prompts the user to select a scenario category.

    Displays the available scenario groups, such as SSH, FTP, HTTP, and mixed
    multi-service scenarios. The selected category is used to decide which
    scenario menu should be shown next. The user can also exit without selecting
    a scenario type.

    Returns:
        str | None: Selected scenario type, such as "SSH", "FTP", "HTTP", or
            "MIXED", otherwise None if the user exits.
    """

    scenario_types = {
        "1": "SSH",
        "2": "FTP",
        "3": "HTTP",
        "4": "MIXED"
    }

    while True:

        print_section_header(
            "Select Scenario Type:",
            Fore.GREEN
        )

        print("1. SSH scenarios")
        print("2. FTP scenarios")
        print("3. HTTP scenarios")
        print("4. Mixed service scenarios")
        print("5. Exit")

        choice = input(
            "\nSelect scenario type: (1-5) "
        ).strip()

        if choice == "5":

            return None

        scenario_type = scenario_types.get(
            choice
        )

        if scenario_type is not None:

            return scenario_type

        print_empty_message(
            "Invalid scenario type."
        )

def select_ssh_scenario() -> tuple[str, list[str]] | None:
    """
    Prompts the user to select an SSH log generation scenario.

    Displays available SSH scenario options and returns the selected scenario name
    with its generated SSH authentication log lines. The user can also exit
    without selecting an SSH scenario.

    Returns:
        tuple[str, list[str]] | None: Selected SSH scenario name and generated
            log lines, or None if the user exits.
    """

    while True:

        print_section_header(
            "Select Scenario:",
            Fore.GREEN
        )

        print("1. Failed login")
        print("2. Successful login")
        print("3. Brute force")
        print("4. Suspicious success")
        print("5. User targeting")
        print("6. Normal activity")
        print("7. Mixed attack")
        print("8. Exit")

        choice = input("\nSelect scenario: (1-8) ").strip()

        if choice == "1":

            return "Failed login", generate_ssh_failed_scenario()
        
        elif choice == "2":

            return "Successful login", generate_ssh_success_scenario()

        elif choice == "3":

            return "Brute force", generate_ssh_brute_force_scenario()
        
        elif choice == "4":

            return "Suspicious success", generate_ssh_suspicious_success_scenario()
        
        elif choice == "5":

            return "User targeting", generate_ssh_user_targeting_scenario()
        
        elif choice == "6":

            return "Normal activity", generate_ssh_normal_activity()
        
        elif choice == "7":

            return "Mixed attack", generate_ssh_mixed_attack_scenario()
        
        elif choice == "8":

            return None
        
        else:

            print_empty_message(
                "Invalid scenario choice."
            )

def select_ftp_scenario() -> tuple[str, list[str]] | None:
    """
    Prompts the user to select an FTP log generation scenario.

    Displays available FTP scenario options and returns the selected scenario name
    with its generated FTP authentication log lines. The user can also exit
    without selecting an FTP scenario.

    Returns:
        tuple[str, list[str]] | None: Selected FTP scenario name and generated
            log lines, or None if the user exits.
    """

    while True:

        print_section_header(
            "Select Scenario:",
            Fore.GREEN
        )

        print("1. Failed login")
        print("2. Successful login")
        print("3. Sucessful anonymous login")
        print("4. Brute force")
        print("5. Suspicious success")
        print("6. User targeting")
        print("7. Normal activity")
        print("8. Mixed attack")
        print("9. Exit")

        choice = input("\nSelect scenario: (1-9) ").strip()

        if choice == "1":

            return "Failed login", generate_ftp_failed_scenario()
        
        elif choice == "2":

            return "Successful login", generate_ftp_success_scenario()
        
        elif choice == "3":

            return "Successful anonymous login", generate_anonymous_ftp_scenario()

        elif choice == "4":

            return "Brute force", generate_ftp_brute_force_scenario()
        
        elif choice == "5":

            return "Suspicious success", generate_ftp_suspicious_success_scenario()
        
        elif choice == "6":

            return "User targeting", generate_ftp_user_targeting_scenario()
        
        elif choice == "7":

            return "Normal activity", generate_ftp_normal_activity()
        
        elif choice == "8":

            return "Mixed attack", generate_ftp_mixed_attack_scenario()
        
        elif choice == "9":

            return None
        
        else:

            print_empty_message(
                "Invalid scenario choice."
            )

def select_http_scenario() -> tuple[str, list[str]] | None:
    """
    Prompts the user to select an HTTP access log scenario.

    Displays available HTTP scenario options and returns the selected scenario name
    with its generated HTTP authentication log lines. The user can also exit
    without selecting an HTTP scenario.

    Returns:
        tuple[str, list[str]] | None: Selected HTTP scenario name and generated
            log lines, or None if the user exits.
    """

    while True:

        print_section_header(
            "Select Scenario:",
            Fore.GREEN
        )

        print("1. Failed login")
        print("2. Sucessful login")
        print("3. Brute force")
        print("4. Suspicious success")
        print("5. User targeting")
        print("6. Normal activity")
        print("7. Mixed attack")
        print("8. Exit")

        choice = input("\nSelect scenario: (1-8) ").strip()

        if choice == "1":

            return "Failed login", generate_http_failed_scenario()
        
        elif choice == "2":

            return "Successful login", generate_http_success_scenario()

        elif choice == "3":

            return "Brute force", generate_http_brute_force_scenario()
        
        elif choice == "4":

            return "Suspicious success", generate_http_suspicious_success_scenario()
        
        elif choice == "5":

            return "User targeting", generate_http_user_targeting_scenario()
        
        elif choice == "6":

            return "Normal activity", generate_http_normal_activity()
        
        elif choice == "7":

            return "Mixed attack", generate_http_mixed_attack_scenario()
        
        elif choice == "8":

            return None
        
        else:

            print_empty_message(
                "Invalid scenario choice."
            )

def select_mixed_services() -> tuple[str, list[str]] | None:
    """
    Prompts the user to select a mixed service attack scenario.

    Mixed service scenarios combine generated authentication activity from
    multiple supported services, such as SSH, FTP, and HTTP. This allows
    SentinelIR to test multi-service parsing, static analysis, live monitoring,
    and detection behaviour using one generated log file.

    Returns:
        tuple[str, list[str]] | None: Selected mixed scenario name and generated
            log lines, or None if the user exits the mixed service menu.
    """

    while True:

        print_section_header(
            "Select Mixed Service Scenario:",
            Fore.GREEN
        )

        print("1. SSH + FTP + HTTP")
        print("2. SSH + FTP")
        print("3. SSH + HTTP")
        print("4. FTP + HTTP")
        print("5. Exit")

        choice = input("\nSelect mixed service scenario: (1-5) ").strip()

        if choice == "1":

            return "Mixed service attack", generate_mixed_service_attack_scenario()

        if choice == "2":

            return "Mixed SSH + FTP attack", generate_ssh_ftp_mixed_attack_scenario()

        if choice == "3":

            return "Mixed SSH + HTTP attack", generate_ssh_http_mixed_attack_scenario()

        if choice == "4":

            return "Mixed FTP + HTTP attack", generate_ftp_http_mixed_attack_scenario()

        if choice == "5":

            return None

        print_empty_message(
            "Invalid mixed service scenario choice."
        )

def generate_mixed_service_attack_scenario(
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a mixed multi-service attack scenario.

    Combines SSH, FTP, and HTTP authentication activity into one generated
    scenario. This can be used to test whether SentinelIR can parse, analyse,
    live-monitor, and detect suspicious behaviour across multiple log formats
    within the same file.

    Args:
        start_time (datetime | None): Timestamp used as the base time for
            the generated scenario. Defaults to None.

    Returns:
        list[str]: Generated SSH, FTP, and HTTP authentication-related log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 17, 12, 0, 0)

    lines = []

    lines.extend(
        generate_ssh_mixed_attack_scenario(
            start_time=start_time
        )
    )

    lines.extend(
        generate_ftp_mixed_attack_scenario(
            start_time=start_time + timedelta(minutes=10)
        )
    )

    lines.extend(
        generate_http_mixed_attack_scenario(
            start_time=start_time + timedelta(minutes=20)
        )
    )

    return lines

def generate_ssh_ftp_mixed_attack_scenario(
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a mixed SSH and FTP attack scenario.

    Combines SSH and FTP authentication activity into one generated scenario.
    This can be used to test multi-parser routing, shared detection logic, and
    service-aware analysis across SSH and FTP log formats.

    Args:
        start_time (datetime | None): Timestamp used as the base time for
            the generated scenario. Defaults to None.

    Returns:
        list[str]: Generated SSH and FTP authentication log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 17, 12, 0, 0)

    lines = []

    lines.extend(
        generate_ssh_mixed_attack_scenario(
            start_time=start_time
        )
    )

    lines.extend(
        generate_ftp_mixed_attack_scenario(
            start_time=start_time + timedelta(minutes=10)
        )
    )

    return lines

def generate_ssh_http_mixed_attack_scenario(
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a mixed SSH and HTTP attack scenario.

    Combines SSH authentication logs and HTTP authentication-related access logs
    into one generated scenario. This can be used to test cross-service brute-force,
    suspicious-success, and user-targeting behaviour.

    Args:
        start_time (datetime | None): Timestamp used as the base time for
            the generated scenario. Defaults to None.

    Returns:
        list[str]: Generated SSH and HTTP authentication-related log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 17, 12, 0, 0)

    lines = []

    lines.extend(
        generate_ssh_mixed_attack_scenario(
            start_time=start_time
        )
    )

    lines.extend(
        generate_http_mixed_attack_scenario(
            start_time=start_time + timedelta(minutes=20)
        )
    )

    return lines

def generate_ftp_http_mixed_attack_scenario(
        start_time: datetime | None = None
    ) -> list[str]:
    """
    Generates a mixed FTP and HTTP attack scenario.

    Combines FTP authentication logs and HTTP authentication-related access logs
    into one generated scenario. This can be used to test whether SentinelIR can
    process different service formats through the same detection pipeline.

    Args:
        start_time (datetime | None): Timestamp used as the base time for
            the generated scenario. Defaults to None.

    Returns:
        list[str]: Generated FTP and HTTP authentication-related log lines.
    """

    if start_time is None:
        start_time = datetime(2026, 4, 17, 12, 0, 0)

    lines = []

    lines.extend(
        generate_ftp_mixed_attack_scenario(
            start_time=start_time + timedelta(minutes=10)
        )
    )

    lines.extend(
        generate_http_mixed_attack_scenario(
            start_time=start_time + timedelta(minutes=20)
        )
    )

    return lines
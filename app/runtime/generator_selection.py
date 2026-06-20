from colorama import Fore

from app.generator.ssh_scenarios import (
    generate_ssh_brute_force_scenario,
    generate_ssh_mixed_attack_scenario,
    generate_ssh_normal_activity,
    generate_ssh_suspicious_success_scenario,
    generate_ssh_user_targeting_scenario
)
from app.generator.ftp_scenarios import (
    generate_ftp_failed_scenario,
    generate_ftp_success_scenario,
    generate_anonymous_ftp_scenario,
    generate_ftp_brute_force_scenario,
    generate_ftp_mixed_attack_scenario,
    generate_ftp_normal_activity,
    generate_ftp_suspicious_success_scenario,
    generate_ftp_user_targeting_scenario
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

        print("1. Brute force")
        print("2. Suspicious success")
        print("3. User targeting")
        print("4. Normal activity")
        print("5. Mixed attack")
        print("6. Exit")

        choice = input("\nSelect scenario: (1-6) ").strip()

        if choice == "1":

            return "Brute force", generate_ssh_brute_force_scenario()
        
        elif choice == "2":

            return "Suspicious success", generate_ssh_suspicious_success_scenario()
        
        elif choice == "3":

            return "User targeting", generate_ssh_user_targeting_scenario()
        
        elif choice == "4":

            return "Normal activity", generate_ssh_normal_activity()
        
        elif choice == "5":

            return "Mixed attack", generate_ssh_mixed_attack_scenario()
        
        elif choice == "6":

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

            return "Mixed attack", generate_ftp_normal_activity()
        
        elif choice == "9":

            return None
        
        else:

            print_empty_message(
                "Invalid scenario choice."
            )
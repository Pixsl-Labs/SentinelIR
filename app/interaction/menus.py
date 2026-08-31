from colorama import Fore


from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count,
    print_separator
)


def display_log_analysis_menu() -> None:
    """
    Prints the main log analysis menu.

    Displays available static analysis actions grouped by report type,
    investigation features, detection features, general information, and
    configuration options.

    Returns:
        None
    """

    print_section_header(
        "Log Analysis Menu",
        Fore.GREEN
    )

    print("1. Show full report")
    print("2. Show attack summary")
    print("3. Show attack statistics")

    print_section_header(
        "Investigation"
    )

    print("4. Show activity timeline")
    print("5. Show suspicious activity")
    print("6. Show failed login details")
    print("7. Show failed login summary")

    print_section_header(
        "Detection"
    )

    print("8. Show suspicious IPs")
    print("9. Show brute force detection")
    print("10. Show most targeted users")
    print("11. Show suspicious success")
    print("12. Show user-targeted attacks")
    print("13. Show anonymous FTP logins")

    print_section_header(
        "General Information"
    )

    print("14. Show successful logins")
    print("15. Show total failed logins")
    print("16. Show unique IP count")

    print_section_header(
        "Configuration"
    )

    print("17. Export report to file")
    print("18. Analyse new file")
    print("19. Configure settings")
    print("20. Show current configuration")
    print("21. Exit")

    print_section_header(
        "End of Menu",
        Fore.MAGENTA
    )

def display_configuration_menu(
        threshold: int,
        window_seconds: int
    ) -> None:
    """
    Prints the configuration menu.

    Shows the current brute-force threshold and time window values, and displays
    options for changing settings, restoring defaults, or exiting the menu.

    Args:
        threshold (int): Current brute-force attempt threshold.
        window_seconds (int): Current brute-force time window in seconds.

    Returns:
        None
    """

    print_section_header(
        "Configuration Menu",
        Fore.GREEN
    )

    print(f"1. Maximum number of attempts (current = {threshold})")
    print(f"2. Maximum time window (current = {window_seconds})")
    print("3. Convert back to original")
    print("4. Exit")

    print_section_header(
        "End of Menu",
        Fore.MAGENTA
    )

def current_config(
        threshold: int,
        window_seconds: int
    ) -> None:
    """
    Prints the current detection configuration.

    Displays the active brute-force threshold and time window values so the user
    can confirm which settings are currently being used.

    Args:
        threshold (int): Current brute-force attempt threshold.
        window_seconds (int): Current brute-force time window in seconds.

    Returns:
        None
    """

    print_separator(
        37
    )

    print_section_header(
        "Current Configuration",
        Fore.GREEN
    )

    print(
        Fore.LIGHTYELLOW_EX
        + f"- Threshold: {threshold}")
    print(
        Fore.LIGHTYELLOW_EX
        + f"- Time window: {window_seconds}")

    print_section_header(
        "End of Configuration Settings",
        Fore.MAGENTA
    )

    print_separator(
        37
    )

import logging


from app.utils.display import (
    print_default_message,
    print_empty_message
)


from datetime import datetime, time
from colorama import Fore


def integer_validation(
        prompt, 
        default, 
        label="value"
    ) -> int:
    """
    Prompts the user for an integer input.

    If the user enters a valid integer, that value is returned. If the input is
    empty or invalid, the provided default value is used instead.

    Args:
        prompt (str): Input prompt to display to the user.
        default (int): Default value to use when input is empty or invalid.
        label (str, optional): Name of the value being requested, used in
            user-facing messages. Defaults to "value".

    Returns:
        int: Valid integer entered by the user, or the default value.
    """

    value = input(prompt).strip()

    if value == "":
        print_default_message(
            label,
            default
        )

        return default
    
    try:

        return int(value)
    
    except ValueError:

        logging.error(f"Error: Invalid input, using default.")

        print_default_message(
            label,
            default
        )

        return default
    
def get_time_range() -> tuple[time | None, time | None]:
    """
    Prompts the user for an optional time range filter.

    If the user chooses to apply a time filter, start and end times are collected
    in HH:MM:SS format and converted into time objects. Invalid or skipped input
    returns no time range.

    Returns:
        tuple[time | None, time | None]: Start and end time values, or None values
        when no valid time range is supplied.
    """

    use_time_filter = input(
        "\nApply time range? (y/n): "
    ).strip().lower()

    if use_time_filter != "y":
        return None, None
    
    start = input(
        "Start time (HH:MM:SS) "
    ).strip()

    end = input(
        "End time (HH:MM:SS) "
    ).strip()

    try:

        start_time = (
            datetime.strptime(start, "%H:%M:%S").time()
            if start else None
        )

        end_time = (
            datetime.strptime(end, "%H:%M:%S").time()
            if end else None
        )

        return start_time, end_time
    
    except ValueError:

        logging.error(f"Error: Invalid time format, using default.")

        return None, None
    
def handle_filter_menu(
        reporter,
        title,
        show_function,
        filters
    ) -> None:
    """
    Handles a reusable filtering menu for report and investigation views.

    Builds a dynamic filter menu from the supplied filter names, collects the
    required filter value from the user, optionally applies a time range, and then
    calls the selected display function with the matching keyword arguments.

    Args:
        reporter: Log reporter instance used to display available IP addresses
            and usernames.
        title: Title of the filter menu being displayed.
        show_function: Function called after a filter option is selected.
        filters: List of available filter names, such as ip, username, severity,
            or status.

    Returns:
        None
    """
    while True:

        print(f"\nFilter {title} by:\n")

        options = {}

        option_number = 1

        # Show all
        print(f"{option_number}. None")

        options[str(option_number)] = "none"
        
        option_number += 1

        # Dynamic filters
        for filter_name in filters:
            display_name = filter_name.upper() if filter_name == "ip" else filter_name.title()

            print(f"{option_number}. {display_name}")

            options[str(option_number)] = filter_name

            option_number += 1

        # Back
        print(f"{option_number}. Back")

        options[str(option_number)] = "back"

        choice = input("\nSelect option: ").strip()

        selected_filter = options.get(choice)

        if selected_filter == "none":
            start_time, end_time = get_time_range()

            show_function(
                start_time=start_time,
                end_time=end_time
            )

            break

        elif selected_filter == "ip":

            reporter.print_all_ips()

            ip = input("\nEnter IP address: ").strip()

            if not ip:
                print_empty_message(
                    "No IP entered."
                )

                continue

            start_time, end_time = get_time_range()

            show_function(
                ip=ip,
                start_time=start_time,
                end_time=end_time
            )

            break

        elif selected_filter == "username":

            reporter.print_all_usernames()

            username = input("\nEnter username: ").strip()

            if not username:
                print_empty_message(
                    "No username entered."
                )

                continue

            start_time, end_time = get_time_range()

            show_function(
                username=username,
                start_time=start_time,
                end_time=end_time
            )

            break

        elif selected_filter == "severity":

            severity = input(
                f"\nEnter severity "
                f"({Fore.GREEN}LOW/"
                f"{Fore.YELLOW}MEDIUM/"
                f"{Fore.LIGHTRED_EX}HIGH"
                f"{Fore.RESET}): "
            ).strip().upper()

            if not severity:
                print_empty_message(
                    "No severity entered."
                )

                continue

            start_time, end_time = get_time_range()

            show_function(
                severity=severity,
                start_time=start_time,
                end_time=end_time
            )

            break

        elif selected_filter == "status":

            status = input(
                f"\nEnter status "
                f"({Fore.GREEN}SUCCESS/"
                f"{Fore.LIGHTRED_EX}FAILED"
                f"{Fore.RESET}): "
            ).strip().upper()

            if not status:
                print_empty_message(
                    "No status entered."
                )

                continue

            start_time, end_time = get_time_range()

            show_function(
                status=status,
                start_time=start_time,
                end_time=end_time
            )

            break

        elif selected_filter == "back":

            break

        else:

            print_empty_message(
                f"'{choice}' is an invalid choice."
            )
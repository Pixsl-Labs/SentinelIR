import logging
from datetime import datetime, time
from colorama import Fore


from app.utils.display import (
    print_default_message,
    print_empty_message
)

from app.models.enums import (
    Service,
    Severity,
    AuthenticationStatus
)


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

        logging.error("Error: Invalid input, using default.")

        print_default_message(
            label,
            default
        )

        return default


def prompt_time_value(
        label: str
        ) -> tuple[time | None, bool]:
    """
    Prompts for a single time value until valid, skipped or cancelled.

    Returns:
        tuple[time | None, bool]: Parsed time value and cancel flag.
    """

    while True:

        value = input(
            Fore.LIGHTGREEN_EX
            + f"{label} time "
            + Fore.CYAN
            + "(HH:MM:SS, Enter = skip, back = cancel): "
            + Fore.RESET
        ).strip()

        if value == "":

            return None, False

        if value.lower() in ["back", "cancel", "q", "quit"]:

            return None, True

        try:

            parsed_time = datetime.strptime(
                value,
                "%H:%M:%S"
            ).time()

            return parsed_time, False

        except ValueError:

            print_empty_message(
                "Invalid time format. Use HH:MM:SS, e.g. 13:45:00."
            )


def get_time_range() -> tuple[time | None, time | None]:
    """
    Prompts the user for an optional time range filter.

    Users can retry invalid formats, skip individual time values with Enter,
    or cancel the time range using back/cancel.

    Returns:
        tuple[time | None, time | None]: Start and end time values.
    """

    use_time_filter = input(
        Fore.CYAN
        + "\nApply time range? (y/n): "
        + Fore.RESET
    ).strip().lower()

    if use_time_filter != "y":

        return None, None

    while True:

        start_time, cancelled = prompt_time_value(
            "\nStart"
        )

        if cancelled:

            print_empty_message(
                "Time range cancelled."
            )

            return None, None

        end_time, cancelled = prompt_time_value(
            "\nEnd"
        )

        if cancelled:

            print_empty_message(
                "Time range cancelled."
            )

            return None, None

        if (
            start_time is None
            and end_time is None
        ):

            print_empty_message(
                "No time range applied."
            )

            return None, None

        if (
            start_time is not None
            and end_time is not None
            and end_time < start_time
        ):

            print_empty_message(
                "End time cannot be earlier than start time. Please try again."
            )

            continue

        return start_time, end_time


def format_filter_display_name(
        filter_name: str
        ) -> str:
    """
    Converts an internal filter key into a readable menu label.

    This keeps filter display text consistent across the CLI filter menu. Internal
    keys such as status_code and ip are converted into user-friendly labels such as
    Status Code and IP.

    Args:
        filter_name (str): Internal filter key, such as ip, username, service,
            method, path, or status_code.

    Returns:
        str: Human-readable filter label for display in the terminal menu.
    """

    display_names = {
        "ip": "IP",
        "username": "Username",
        "service": "Service",
        "severity": "Severity",
        "status": "Status",
        "method": "Method",
        "path": "Path",
        "status_code": "Status Code"
    }

    return display_names.get(
        filter_name,
        filter_name.title()
    )


def format_filter_value(
        value
) -> str:
    """
    Converts a filter value into readable display text.
    """

    if value is None:

        return "None applied."

    if hasattr(value, "strftime"):

        return value.strftime(
            "%H:%M:%S"
        )

    if isinstance(
        value,
        (Service, AuthenticationStatus)
    ):
        return value.value

    return str(
        value
    )


def confirm_filter_value(
        title: str,
        filter_values: dict
        ) -> str:
    """
    Shows selected filter values and asks the user how to continue.

    Returns:
        str: apply, restart, or cancel.
    """

    print(
        Fore.GREEN
        + f"\n=== {title} Filter Summary ===\n"
    )

    if not filter_values:

        print("No filters applied.")

    else:

        for filter_name, value in filter_values.items():

            display_name = format_filter_display_name(
                filter_name
            )

            print(
                Fore.CYAN
                + f"{display_name}: "
                + Fore.LIGHTMAGENTA_EX
                + f"{format_filter_value(value)}"
                + Fore.RESET
            )

    print(
        Fore.LIGHTGREEN_EX
        + "\n1. Apply filters"
        + Fore.RESET
    )

    print(
        Fore.LIGHTYELLOW_EX
        + "2. Start again"
        + Fore.RESET
    )

    print(
        Fore.LIGHTRED_EX
        + "3. Cancel"
        + Fore.RESET
    )

    choice = input(
        "\nSelect option: "
    ).strip()

    if choice == "1":

        return "apply"

    if choice == "2":

        return "restart"

    if choice == "3":

        return "cancel"

    print_empty_message(
        "Invalid option. Starting again."
    )

    return "restart"


def parse_filter_selection(
        choice: str,
        options: dict[str, str]
        ) -> list[str]:
    """
    Parses one or more selected filter options from user input.

    Supports numeric menu choices and written filter names. Multiple filters can be
    selected using + or commas, allowing inputs such as "2 + 4", "service + username",
    or "service, ip". Duplicate filters are removed while preserving the order chosen
    by the user.

    Args:
        choice (str): Raw user input containing one or more selected filters.
        options (dict[str, str]): Mapping of menu option numbers to internal filter
            keys.

    Returns:
        list[str]: Selected internal filter keys. Returns ["none"] or ["back"] for
        those menu actions, an empty list if the selection is invalid, or multiple
        filter keys for combined filtering.
    """

    selected_filters = []

    parts = [
        part.strip()
        for part in choice.replace(",", "+").split("+")
        if part.strip()
    ]

    for part in parts:

        if part in options:

            selected_filter = options[part]

        else:

            selected_filter = part.lower().replace(" ", "_")

        if selected_filter in ["none", "back"]:

            return [selected_filter]

        if selected_filter not in options.values():

            print_empty_message(
                f"'{part}' is not a valid filter."
            )

            return []

        if selected_filter not in selected_filters:

            selected_filters.append(
                selected_filter
            )

    return selected_filters


def handle_filter_menu(
        reporter,
        title,
        show_function,
        filters
        ) -> None:
    """
    Handles a reusable multi-filter menu for report and investigation views.

    Collects filter values using the shared filter collection helper, then calls
    the selected display function with those filters.

    Args:
        reporter: Log reporter instance used to display available filter values.
        title (str): Name of the report being filtered.
        show_function: Report printing function called after filters are collected.
        filters (list[str]): Available filter keys for this report.

    Returns:
        None
    """

    filter_values = collect_filter_values(
        reporter=reporter,
        title=title,
        filters=filters
    )

    if filter_values is None:

        return

    show_function(
        **filter_values
    )


def get_available_filter_values(
        reporter,
        filter_name: str
        ) -> list:
    """
    Returns available values for a selected filter.

    This is used before asking the user for a value so filters with no
    available data can be skipped cleanly.
    """

    filter_extractors = {
        "ip": lambda entry: entry.ip,
        "username": lambda entry: entry.user,
        "service": lambda entry: entry.service,
        "severity": lambda entry: entry.severity,
        "status": lambda entry: entry.status,
        "method": lambda entry: entry.method,
        "path": lambda entry: entry.path,
        "status_code": lambda entry: entry.status_code
    }

    extractor = filter_extractors.get(
        filter_name
    )

    if extractor is None:

        return []

    values = set()

    for entry in reporter.get_filter_entries():

        value = extractor(
            entry
        )

        if value is None or value == "":

            continue

        values.add(
            value
        )

    return sorted(
        values
    )


def filter_has_available_values(
        reporter,
        filter_name: str
        ) -> bool:
    """
    Checks whether a selected filter has any values available.
    """

    return bool(
        get_available_filter_values(
            reporter,
            filter_name
        )
    )


def print_unavailable_filter_message(
        filter_name: str
        ) -> None:
    """
    Prints a readable message when a selected filter has no available values.
    """

    unavailable_messages = {
        "ip": "No IP addresses found. Skipping IP filter.",
        "username": "No usernames found. Skipping username filter.",
        "service": "No services found. Skipping service filter.",
        "severity": "No severities found. Skipping severity filter.",
        "status": "No statuses found. Skipping status filter.",
        "method": "No HTTP methods found. Skipping method filter.",
        "path": "No HTTP paths found. Skipping path filter.",
        "status_code": "No HTTP status codes found. Skipping status code filter."
    }

    print_empty_message(
        unavailable_messages.get(
            filter_name,
            f"No available values for {filter_name}. Skipping filter."
        )
    )


def collect_filter_values(
        reporter,
        title: str,
        filters: list[str]
        ) -> dict | None:
    """
    Collects selected filter values from the reusable CLI filter menu.

    Builds a dynamic filter menu, allows the user to select one or more filters,
    collects values for each selected filter, optionally applies a time range, and
    returns the selected filters as keyword arguments.

    Args:
        reporter: Log reporter instance used to display available filter values.
        title (str): Name of the report being filtered.
        filters (list[str]): Available filter keys for this report.

    Returns:
        dict | None: Dictionary of selected filter values, or None if the user
        chooses Back.
    """

    while True:

        print(f"\nFilter {title} by: \n")

        options = {}

        option_number = 1

        print(f"{option_number}. None")

        options[str(option_number)] = "none"

        option_number += 1

        for filter_name in filters:

            display_name = format_filter_display_name(
                filter_name
            )

            print(f"{option_number}. {display_name}")

            options[str(option_number)] = filter_name

            option_number += 1

        print(f"{option_number}. Back")

        options[str(option_number)] = "back"

        choice = input(
            "\nSelect option(s), e.g. service + username or 2 + 4: "
        ).strip()

        selected_filters = parse_filter_selection(
            choice,
            options
        )

        if not selected_filters:

            continue

        if selected_filters == ["back"]:

            return None

        if selected_filters == ["none"]:

            start_time, end_time = get_time_range()

            return {
                "start_time": start_time,
                "end_time": end_time
            }

        filter_values = {}

        invalid_filter = False

        for selected_filter in selected_filters:

            if not filter_has_available_values(
                reporter,
                selected_filter
            ):

                print_unavailable_filter_message(
                    selected_filter
                )

                continue

            if selected_filter == "ip":

                reporter.print_all_ips()

                value = input(
                    "\nEnter IP address: "
                ).strip()

                if not value:
                    print_empty_message(
                        "No IP entered."
                    )

                    invalid_filter = True
                    break

                filter_values["ip"] = value

            elif selected_filter == "username":

                reporter.print_all_usernames()

                value = input(
                    "\nEnter username: "
                ).strip()

                if not value:
                    print_empty_message(
                        "No username entered."
                    )

                    invalid_filter = True
                    break

                filter_values["username"] = value

            elif selected_filter == "service":

                reporter.print_all_services()

                value = input(
                    "\nEnter service: "
                ).strip().upper()

                try:

                    service = Service(
                        value
                    )

                except ValueError:

                    print_empty_message(
                        "Invalid service. Use SSH, FTP, or HTTP."
                    )

                    invalid_filter = True
                    break

                filter_values["service"] = service

            elif selected_filter == "severity":

                reporter.print_all_severities()

                value = input(
                    "\nEnter severity: "
                ).strip().upper()

                try:

                    severity = Severity(
                        value
                    )

                except ValueError:

                    print_empty_message(
                        "Invalid severity. Use LOW, MEDIUM, or HIGH."
                    )

                    invalid_filter = True
                    break

                filter_values["severity"] = severity

            elif selected_filter == "status":

                reporter.print_all_statuses()

                value = input(
                    "\nEnter status: "
                ).strip().upper()

                try:

                    status = AuthenticationStatus(
                        value
                    )

                except ValueError:

                    print_empty_message(
                        "Invalid status. Use SUCCESS or FAILED."
                    )

                    invalid_filter = True
                    break

                filter_values["status"] = status

            elif selected_filter == "method":

                reporter.print_all_methods()

                value = input(
                    "\nEnter method: "
                ).strip().upper()

                if not value:
                    print_empty_message(
                        "No method entered."
                    )

                    invalid_filter = True
                    break

                if value not in [
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE",
                    "PATCH",
                    "HEAD",
                    "OPTIONS"
                ]:

                    print_empty_message(
                        "Invalid method. Use GET, POST, PUT, DELETE, PATCH, HEAD, or OPTIONS."
                    )

                    invalid_filter = True
                    break

                filter_values["method"] = value

            elif selected_filter == "path":

                reporter.print_all_paths()

                value = input(
                    "\nEnter path: "
                ).strip()

                if not value:
                    print_empty_message(
                        "No path entered."
                    )

                    invalid_filter = True
                    break

                filter_values["path"] = value

            elif selected_filter == "status_code":

                reporter.print_all_status_codes()

                value = input(
                    "\nEnter HTTP status code: "
                ).strip()

                if not value.isdigit():

                    print_empty_message(
                        "Invalid status code."
                    )

                    invalid_filter = True
                    break

                filter_values["status_code"] = int(value)

        if invalid_filter:

            continue

        if not filter_values:

            print_empty_message(
                "No usable filters were selected. Please choose again."
            )

            continue

        start_time, end_time = get_time_range()

        filter_values["start_time"] = start_time
        filter_values["end_time"] = end_time

        decision = confirm_filter_value(
            title,
            filter_values
        )

        if decision == "apply":

            return filter_values

        if decision == "cancel":

            return None

        if decision == "restart":

            continue

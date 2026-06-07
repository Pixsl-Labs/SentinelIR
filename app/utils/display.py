from colorama import Fore
import logging


def print_section_header(
    title: str,
    colour: str=Fore.CYAN
) -> None:
    """
    Prints a formatted section header.

    Args:
        title (str): Header title to display.
        colour (str, optional): Colorama colour used for the header text. 
            Defaults to Fore.CYAN.

    Returns:
        None
    """
    
    print(
        colour
        + f"\n=== {title} ===\n"
    )

def print_empty_message(
    message: str
) -> None:
    """
    Prints a formatted empty-result or error-style message.

    Args:
        message (str): Message to display to the user.

    Returns:
        None
    """

    print(
        Fore.LIGHTRED_EX
        + f"\n{message}"
    )

def print_default_message(
    label: str,
    default
) -> None:
    """
    Prints a formatted message when a default value is used.

    Args:
        label (str): Name of the value using the default.
        default: Default value being used.

    Returns:
        None
    """

    print(
        Fore.YELLOW
        + "\nUsing default "
        + Fore.CYAN
        + f"{label}"
        + Fore.YELLOW
        + " value "
        + Fore.LIGHTGREEN_EX
        + f"({default})\n"
    )

def print_info(
    message: str,
    colour: str = Fore.CYAN
) -> None:
    """
    Prints a formatted informational message.

    Args:
        message (str): Message to display to the user.
        colour (str, optional): Colorama colour used for the message.
            Defaults to Fore.CYAN.

    Returns:
        None
    """

    print(
        colour
        + message
    )

def print_total_count(
    label: str,
    count: int,
    colour: str
) -> None:
    """
    Prints a labelled total count with colour formatting.

    Args:
        label (str): Name of the value being counted.
        count (int): Numeric total to display.
        colour (str): Colorama colour used for the ouput text.

    Returns:
        None
    """

    print(
        colour
        + f"   {label}: {count}\n"
    )

def print_separator(
    count: int,
    colour: str=Fore.CYAN
) -> None:
    """
    Prints a coloured separator line.

    Args:
        count (int): Number of separator characters to print.
        colour (str, optional): Colorama colour used for the separator.
            Defaults to Fore.CYAN.

    Returns:
        None
    """
    
    print(
    colour
    + "-" * count
    )

def logging_info(
    message: str,
    colour: str=Fore.YELLOW
) -> None:
    """
    Writes a formatted informational message to the application log.

    Args:
        message (str): Message to write to the log.
        colour (str, optional): Colorama colour prefix applied to the logged message. 
            Defaults to Fore.YELLOW.

    Returns:
        None
    """

    logging.info(
        colour
        + f"{message}"
    )

def logging_error(
    message: str,
    colour: str=Fore.LIGHTRED_EX
) -> None:
    """
    Writes a formatted error message to the application log.

    Args:
        message (str): Message to write to the log.
        colour (str, optional): Colorama colour prefix applied to the logged message. 
            Defaults to Fore.LIGHTRED_EX.

    Returns:
        None
    """

    logging.error(
        colour
        + f"{message}"
    )

def print_alert(
        severity: str,
        title: str,
        message: str
    ) -> None:
    """
    Prints a formatted securityy alert.

    The alert colour is selected from severity level before printing the
    alert title and message.

    Args:
        severity (str): Alert severity, such as LOW, MEDIUM, HIGH, or CRITICAL.
        title (str): Alert title to display.
        message (str): Alert message containing supporting details.

    Returns:
        None
    """

    severity = severity.upper()

    colour = Fore.WHITE

    if severity == "LOW":
        colour = Fore.LIGHTYELLOW_EX

    elif severity == "MEDIUM":
        colour = Fore.LIGHTMAGENTA_EX

    elif severity == "HIGH":
        colour = Fore.LIGHTRED_EX

    elif severity == "CRITICAL":
        colour = Fore.RED

    print()

    print(
        colour
        + f"[{severity}] {title}"
    )

    print(
        colour
        + message
    )

def print_status_line(
    label: str,
    value,
    colour: str,
    width: int = 25
) -> None:
    """
    Prints a formatted labelled status line.

    Args:
        label (str): Label displayed on the left.
        value: Value displayed on the right.
        colour (str): Colorama colour used for the value.
        width (int, optional): Width used to align the label.
            Defaults to 25.

    Returns:
        None
    """

    print(
        f"{label + ':':<{width}} "
        f"{colour}{value}"
    )
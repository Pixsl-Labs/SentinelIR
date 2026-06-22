from colorama import Fore

from app.utils.colours import (
    get_service_colour,
    get_user_colour,
    get_severity_colour
)


TABLE_INDENT = "    "

def format_service_column(
            service: str | None,
            width: int | str,
            align: str = "<"
    ) -> str:
    """
    Formats a service column with service-specific colour.

    Args:
        service (str | None): Service name such as SSH, FTP, or HTTP.
        width (int | str): Column width, or END for the final column.
        align (str): Alignment direction.
            Defaults to "<".

    Returns:
        str: Colour-formatted service column.
    """

    service_text = (
        service or "UNKNOWN"
    ).upper()

    return (
        get_service_colour(service_text)
        + format_column(service_text, width, align)
        + Fore.RESET
    )

def format_user_column(
            user: str | None,
            width: int | str,
            align: str = "<"
    ) -> str:
    """
    Formats the username column with user-specific colour.

    Args:
        user (str | None): Username name such as root, admin, or guest.
        width (int | str): Column width
        align (str): Alignment direction.
            Defaults to "<".

    Returns:
        str: Colour-formatted user column.
    """

    user_text = (
        user or "unknown"
    ).lower()

    return (
        get_user_colour(user_text)
        + format_column(user_text, width, align)
        + Fore.RESET
    )

def format_servity_column(
            servity: str | None,
            width: int | str,
            align: str = "<"
    ) -> str:
    """
    Formats the servity column with user-specific colour.

    Args:
        servity (str | None): Servity name such as "HIGH", "MEDIUM", "LOW"
            or "NONE".
        width (int | str): Column width
        align (str): Alignment direction.
            Defaults to "<".

    Returns:
        str: Colour-formatted servity column.
    """

    severity_text = (
        servity or "UNKNOWN"
    ).upper()

    return (
        get_severity_colour(severity_text)
        + format_column(severity_text, width, align)
        + Fore.RESET
    )

def format_column(
    value,
    width: int | str,
    align="<"
) -> str:
    """
    Formats a value into a table column.

    If width is "END", the value is returned without fixed-width padding. This is
    useful for the final column in a table where no extra spacing is needed.

    Args:
        value: Value to display inside the column.
        width (int | str): Width of the formatted column, or "END" for the final
            unpadded column.
        align (str): Alignment character used by Python string formatting.
            Defaults to "<".

    Returns:
        str: Formatted column string.
    """

    value = str(value)

    if isinstance(width, str) and width.upper() == "END":

        return value

    return f"{value:{align}{width}}"


def print_table_header(
    columns: list[tuple]
) -> None:
    """
    Prints a formatted table header for CLI output.

    Builds a header row from column definitions and prints a separator line
    underneath. Each column can include a title, width, and optional alignment.
    Use "END" as the width for the final column to avoid unnecessary padding.

    Args:
        columns (list[tuple]): Table column definitions. Each tuple should contain
            a column title and width, with an optional alignment value.

    Returns:
        None
    """

    header_row = TABLE_INDENT

    separator_length = 0

    for column in columns:

        if len(column) == 3:
            header, width, align = column

        else:
            header, width = column
            align = "<"

        header_row += format_column(
            header,
            width,
            align
        )

        if isinstance(width, str) and width.upper() == "END":

            separator_length += len(str(header))

        else:

            separator_length += width

    print(
        Fore.CYAN
        + header_row
    )

    print(
        TABLE_INDENT
        + Fore.LIGHTBLACK_EX
        + "-" * separator_length
    )
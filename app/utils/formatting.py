from colorama import Fore


def format_column(
    value,
    width: int,
    align="<"
) -> str:
    """
    Formats a value into a fixed-width table column.

    Converts the supplied value to a string and applies the requested width and
    alignment. This helps keep CLI table output neat and readable.

    Args:
        value: Value to display inside the column.
        width (int): Width of the formatted column.
        align (str): Alignment character used by Python string formatting.
            Defaults to "<".

    Returns:
        str: Formatted column string.
    """

    return f"{str(value):{align}{width}}"


def print_table_header(
    columns: list[tuple]
) -> None:
    """
    Prints a formatted table header for CLI output.

    Builds a header row from column definitions and prints a separator line
    underneath. Each column can include a title, width, and optional alignment.

    Args:
        columns (list[tuple]): Table column definitions. Each tuple should contain
        a column title and width, with an optional alignment value.

    Returns:
        None
    """

    header_row = "   "

    separator_length = 3

    for column in columns:

        if len(column) == 3:
            header, width, align = column

        else:
            header, width = column
            align = "<"

        header_row += (
            format_column(
                header,
                width,
                align
            )
        )

        separator_length += width

    print(
        Fore.CYAN
        + header_row
    )

    print(
        "   "
        + Fore.LIGHTBLACK_EX
        + "-" * separator_length
    )
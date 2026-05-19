from colorama import Fore


def format_column(
    value,
    width,
    align="<"
) -> str:

    return f"{str(value):{align}{width}}"


def print_table_header(
    columns: list[tuple]
) -> None:

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
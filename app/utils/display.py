from colorama import Fore
import logging


def print_section_header(
    title: str,
    colour: str=Fore.CYAN
) -> None:
    
    print(
        colour
        + f"\n=== {title} ===\n"
    )

def print_empty_message(
    message: str
) -> None:

    print(
        Fore.LIGHTRED_EX
        + f"\n{message}"
    )

def print_total_count(
    label: str,
    count: int,
    colour: str
) -> None:

    print(
        colour
        + f"   {label}: {count}\n"
    )

def print_separator(
    count: int,
    colour: str=Fore.CYAN
) -> None:
    
    print(
    colour
    + "-" * count
    )

def logging_info(
    message: str,
    colour: str=Fore.YELLOW
) -> None:

    logging.info(
        colour
        + f"{message}"
    )
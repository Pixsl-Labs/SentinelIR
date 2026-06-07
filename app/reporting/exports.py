from app.utils.display import (
    print_info
)


import json
from datetime import datetime
from dataclasses import asdict, is_dataclass
from colorama import Fore


class Export:
    """
    Provides report export functionality.

    This mixin exports filtered analysis results to human-readable TXT files or
    structured JSON files for later review, sharing, or further processing.
    """
    def export_txt(
            self,
            filename: str,
            title: str,
            data: list
        ) -> None:
        """
        Exports filtered results to a TXT file.

        Writes a report title, generation timestamp, and each result entry to a
        human-readable text file. LogEntry-style objects are formatted with status,
        timestamp, username, IP address, and severity.

        Args:
            filename (str): Output TXT file path.
            title (str): Report title written at the top of the file.
            data (list): Results to export.

        Returns:
            None
        """

        now = datetime.now()

        with open(filename, "w") as f:

            f.write(f"=== {title} ===\n\n")

            f.write(
                now.strftime(
                    "Generated: %Y-%m-%d %H:%M:%S\n\n"
                )
            )

            if not data:
                f.write("No results found.\n")

            else:
                for item in data:
                    if hasattr(item, "ip"):

                        timestamp = (
                            item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                            if item.timestamp
                            else "Unknown"
                        )

                        f.write(
                            f"[{item.status:<7}] "
                            f"{timestamp} "
                            f"{item.user:<12} "
                            f"{item.ip:<15} "
                            f"[{item.severity}]\n"
                        )

                    else:
                        f.write(f"{item}\n")

        print_info(
            Fore.YELLOW
            + f"\nTXT report exported to {filename}"
        )

    def export_json(
            self,
            filename: str,
            title: str,
            data: list
        ) -> None:
        """
        Exports filtered results to a JSON file.

        Creates a structured JSON report containing a generation timestamp, title, and
        serialised result data. Dataclass object are converted into dictionaries before
        being written.

        Args:
            filename (str): Output JSON file path.
            title (str): Report title stored in the JSON output.
            data (list): Results to export.

        Returns:
            None
        """

        now = datetime.now()

        export_data = {
            "generated_at": now.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "title": title,
            
            "results": [
                {
                    key: (
                        value.strftime("%Y-%m-%d %H:%M:%S")
                        if isinstance(value, datetime)
                        else value
                    )

                    for key, value in asdict(item).items()
                }

                if is_dataclass(item)
                else item
                for item in data
            ]
        }

        with open(filename, "w") as f:
            json.dump(export_data, f, indent=4)

        print_info(
            Fore.YELLOW
            + f"\nJSON report exported to {filename}"
        )
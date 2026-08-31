import json
from datetime import datetime
from dataclasses import asdict, is_dataclass
from colorama import Fore

from app.utils.display import (
    print_info
)
from app.utils.export_formatting import (
    export_section_header,
    export_generated_timestamp,
    export_empty_message,
    export_log_entry_line,
    export_log_entry_header,
    export_filter_summary
)


def serialise_filters(
            filters: dict | None
    ) -> dict:
    """
    Converts export filters values into JSON-safe values.

    Args:
        filters (dict | None): Filters applied to the exported report.

    Returns:
        dict: JSON-safe filter dictionary.
    """

    if not filters:

        return {}

    serialised = {}

    for key, value in filters.items():

        if value is None:

            continue

        if hasattr(value, "strftime"):

            serialised[key] = value.strftime(
                "%H:%M:%S"
            )

        else:

            serialised[key] = value

    return serialised

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
            data: list,
            filters: dict | None = None
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
            filters (dict | None): Filters applied to the exported report.
                Defaults to None.

        Returns:
            None
        """

        with open(
                filename,
                "w"
            ) as f:

            f.write(
                export_section_header(title)
            )

            f.write(
                export_generated_timestamp()
                )

            f.write(
                export_filter_summary(filters)
            )

            if not data:
                f.write(
                    export_empty_message(
                        "No results found."
                    )
                )

            else:

                if all(
                    (hasattr(item, "ip")
                        and hasattr(item, "status")
                        for item in data)
                ):

                    f.write(
                        f"Total Results: {len(data)}\n\n"
                    )

                    f.write(
                        export_log_entry_header()
                    )

                for item in data:

                    if (hasattr(item, "ip")
                        and hasattr(item, "status")):

                        f.write(
                            export_log_entry_line(item)
                        )

                    else:

                        f.write(f"{item}\n")

    def export_json(
            self,
            filename: str,
            title: str,
            data: list,
            filters: dict | None = None
        ) -> None:
        """
        Exports filtered results to a structured JSON file.

        Creates a JSON report containing metadata, selected filters, result count, and
        serialised result data. Dataclass objects are converted into dictionaries before
        being written.

        Args:
            filename (str): Output JSON file path.
            title (str): Report title stored in the JSON output.
            data (list): Results to export.
            filters (dict | None): Filters applied to the exported report.
                Defaults to None.

        Returns:
            None
        """

        now = datetime.now()

        export_data = {
            "metadata": {
                "version": "1.0",
                "generated_at": now.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "title": title,
                "result_count": len(data),
                "filters": serialise_filters(filters)
            },

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

        with open(
            filename,
            "w"
            ) as f:

            json.dump(
                export_data,
                f,
                indent=4
            )

        print_info(
            Fore.YELLOW
            + f"\nJSON report exported to {filename}"
        )

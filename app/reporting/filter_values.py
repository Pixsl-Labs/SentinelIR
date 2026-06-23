from colorama import Fore

from app.utils.display import (
    print_section_header,
    print_empty_message
)
from app.utils.colours import (
    get_user_colour,
    get_service_colour,
    get_severity_colour,
    get_status_colour,
    get_status_code_colour
)


class FilterValues:
    """
    Provides helper methods for printing available filter values.

    These methods collect unique values from analysed failed and successful login
    entries and display them to the user before a filter value is entered. This
    supports the reusable CLI filter menu by showing valid choices for services,
    IP addresses, usernames, severities, statuses, HTTP methods, HTTP paths, and
    HTTP status codes.
    """

    def get_filter_entries(self) -> list:
        """
        Returns all entries available for filter values extraction.

        Combines failed and successful login entries so filter menus can show
        values from the full analysed activity set.

        Returns:
            list: Combined failed and successful login entries.
        """

        return (
            self.analyser.failed_logins
            + self.analyser.successful_logins
        )

    def _print_available_values(
            self,
            title: str,
            values: set,
            empty_message: str,
            colour: str = Fore.GREEN,
            value_colour_function=None
        ) -> None:
        """
        Prints a sorted list of available filter values.

        Args:
            title (str): Section title displayed above the available values.
            values (set): Unique values collected from analysed log entries.
            empty_message (str): Message displayed when no values are available.
            colour (str): Colorama colour for the section header.
                Default: Fore.GREEN
            value_colour_function: Optional function used to colour each individual
            value. Defaults: None.

        Returns:
            None
        """

        cleaned_values = {
            value
            for value in values
            if value is not None and value != ""
        }

        if not cleaned_values:
            print_empty_message(
                empty_message
            )

            return
        
        print_section_header(
            title,
            colour
        )

        for value in sorted(cleaned_values):

            value_colour = (
                value_colour_function(value)
                if value_colour_function
                else colour
            )

            print(f"    {value_colour}{value}{Fore.RESET}")

    def print_all_services(self) -> None:
        """
        Prints all services found in the analysed log entries.

        Collects unique service names such as SSH, FTP, and HTTP from failed and
        successful login entries. These values can be used by the service filter.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        services = {
            entry.service
            for entry in entries
        }

        self._print_available_values(
            "All available Services",
            services,
            "No services found.",
            Fore.GREEN,
            get_service_colour
        )

    def print_all_ips(self) -> None:
        """
        Prints all IP addresses found in the analysed log entries.

        Collects unique source IP addresses from failed and successful login
        entries. These values can be used by the IP address filter.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        ips = {
            entry.ip
            for entry in entries
        }

        self._print_available_values(
            "All Available IP Addresses",
            ips,
            "No IP addresses found."
        )

    def print_all_usernames(self) -> None:
        """
        Prints all usernames found in the analysed log entries.

        Collects unique usernames from failed and successful login entries. These
        values can be used by the username filter.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        usernames = {
            entry.user
            for entry in entries
        }

        self._print_available_values(
            "All Available Users",
            usernames,
            "No usernames found.",
            Fore.GREEN,
            get_user_colour
        )

    def print_all_severities(self) -> None:
        """
        Prints all severity levels found in the analysed log entries.

        Collects unique severity values such as LOW, MEDIUM, and HIGH from failed
        and successful login entries. These values can be used by the severity
        filter.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        severities = {
            entry.severity
            for entry in entries
        }

        self._print_available_values(
            "All Available Severities",
            severities,
            "No severities found.",
            Fore.GREEN,
            get_severity_colour
        )

    def print_all_statuses(self) -> None:
        """
        Prints all authentication statuses found in the analysed log entries.

        Collects unique authentication statuses such as FAILED and SUCCESS from
        failed and successful login entries. These values can be used by the status
        filter.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        statuses = {
            entry.status
            for entry in entries
        }

        self._print_available_values(
            "All Available Statuses",
            statuses,
            "No statuses found.",
            Fore.GREEN,
            get_status_colour
        )

    def print_all_methods(self) -> None:
        """
        Prints all HTTP methods found in the analysed log entries.

        Collects unique HTTP request methods such as GET and POST from parsed HTTP
        log entries. SSH and FTP entries do not contain methods and are ignored.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        methods = {
            entry.method
            for entry in entries
            if entry.method is not None
        }

        self._print_available_values(
            "All Available HTTP Methods",
            methods,
            "No HTTP methods found."
        )

    def print_all_paths(self) -> None:
        """
        Prints all HTTP paths found in the analysed log entries.

        Collects unique HTTP request paths from parsed HTTP log entries. SSH and
        FTP entries do not contain paths and are ignored.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        paths = {
            entry.path
            for entry in entries
            if entry.path is not None
        }

        self._print_available_values(
            "All Available HTTP Paths",
            paths,
            "No HTTP paths found."
        )

    def print_all_status_codes(self) -> None:
        """
        Prints all HTTP status codes found in the analysed log entries.

        Collects unique HTTP response status codes from parsed HTTP log entries.
        SSH and FTP entries do not contain HTTP status codes and are ignored.

        Returns:
            None
        """

        entries = self.get_filter_entries()

        status_codes = {
            entry.status_code
            for entry in entries
            if entry.status_code is not None
        }

        self._print_available_values(
            "All Available HTTP Status Codes",
            status_codes,
            "No HTTP status codes found.",
            Fore.GREEN,
            get_status_code_colour
        )
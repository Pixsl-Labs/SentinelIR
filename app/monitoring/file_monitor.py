from app.utils.display import (
    print_empty_message,
    print_info,
    logging_error,
    logging_info
)


import time
from colorama import Fore


class FileMonitor:
    """
    Monitors a log file for new lines during live analysis.

    The file monitor watches the configured file, reads new log lines as they are
    written, and passes them to the live event processor for parsing and detection.
    """
    def __init__(
        self,
        file_path: str,
        processor,
        poll_interval: float = 0.2
    ):
        """
        Initialises the file monitor.

        Stores the target file path, live event processor, polling interval, and running
        state used by the monitoring loop.

        Args:
            file_path (str): Path to the log file being monitored.
            processor (_type_): Live event processor used to process new log lines.
            poll_interval (float): Delay between checks for new file content.
                Defaults to 0.2.

        Returns:
            None
        """
        self.file_path = file_path
        self.processor = processor
        self.poll_interval = poll_interval
        self.running = True

    def watch(self) -> bool:
        """
        Watches the configured file for new log lines.

        Moves to the end of the file, waits for new lines, and sends each new line to
        the configured processor. Monitoring continues until stopped or interrupted.

        Returns:
            bool: True if monitoring stops cleanly, otherwise False.
        """

        try:

            logging_info(
                f"Monitoring file: {self.file_path}"
            )

            print_info(
                "\nMonitoring started...\n",
                Fore.GREEN
            )

            print_info(
                "Press CTRL+C to stop.\n",
                Fore.CYAN
            )

            with open(self.file_path, "r") as file:

                # Move to the end of the file.
                file.seek(0, 2)

                while self.running:

                    line = file.readline()

                    if not line:
                        time.sleep(self.poll_interval)

                        continue

                    self.processor.process_line(
                        line.strip()
                    )

            return True
        
        except FileNotFoundError:

            logging_error(
                f"Error: File '{self.file_path}' not found."
            )

            return False
        
        except KeyboardInterrupt:

            print_empty_message(
                "Monitoring stopped..."
            )

            return True
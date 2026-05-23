import time
import logging

from app.utils.display import (
    print_empty_message
)


class FileMonitor:

    def __init__(
        self,
        file_path: str,
        processor,
        poll_interval: float = 0.2
    ):
        self.file_path = file_path
        self.processor = processor
        self.poll_interval = poll_interval
        self.running = True

    def watch(self) -> bool:
        """
        Watches the configured file for new lines.
        """

        try:

            logging.info(
                f"Monitoring file: {self.file_path}"
            )

            print("\nMonitoring started...")
            print("Press CTRL+C to stop.\n")

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

            logging.error(
                f"Error: File '{self.file_path}' not found."
            )

            return False
        
        except KeyboardInterrupt:

            print_empty_message(
                "Monitoring stopped..."
            )

            return True
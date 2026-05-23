from colorama import Fore

from app.monitoring.file_monitor import FileMonitor
from app.monitoring.live_event_processor import LiveEventProcessor

from app.utils.display import (
    print_section_header,
    print_empty_message
)


class LiveRuntime:

    def __init__(
            self,
            analyser,
            reporter,
            log_file
        ):

        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(self):

        print_section_header(
            "Live Monitoring Mode",
            Fore.GREEN
        )

        processor = LiveEventProcessor(
            analyser=self.analyser
        )

        monitor = FileMonitor(
            file_path=self.log_file,
            processor=processor
        )

        success = monitor.watch()

        if not success:

            print_empty_message(
                "Monitoring failed."
            )
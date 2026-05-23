class LiveEventProcessor:

    def __init__(
            self,
            analyser,
            show_new_logs: bool = True
        ):
        self.analyser = analyser
        self.show_new_logs = show_new_logs

    def process_line(
            self,
            line: str
        ) -> None:
        """
        Processes a single live log line.
        """

        if not line:
            return
        
        if self.show_new_logs:
            print(f"[NEW LOG] {line}")

        lower_line = line.lower()

        if "failed password" in lower_line:

            self.analyser.extract_failed_ip(
                line
            )

            self.analyser.detection_engine.process_live_detection(
                self.analyser
            )

        elif (
            "accepted password" in lower_line
            or "session opened" in lower_line
        ):

            self.analyser.extract_successful_login(
                line
            )

            self.analyser.detection_engine.process_live_detection(
                self.analyser
            )
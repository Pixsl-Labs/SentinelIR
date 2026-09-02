from app.models.detection_summary import DetectionResults


class DetectionService:
    """
    Coordinates structured threat-detection operations.
    """

    def __init__(
        self,
        reporter
    ):
        """
        Initialises the analysis service.

        Args:
            reporter: Log reporter providing structured analysis results.

        Returns:
            None
        """

        self.reporter = reporter

    def get_results(
            self
    ) -> DetectionResults:
        """
        Returns all current structured detection findings.

        Returns:
            DetectionResults: Combined SentinelIR detection findings.
        """

        return self.reporter.get_detection_results()

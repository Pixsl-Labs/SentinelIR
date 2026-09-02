from pathlib import Path


from app.models.analysis_summary import AnalysisSummary


class AnalysisService:
    """
    Coordinates log analysis and structured analysis-summary operations.
    """

    def __init__(
        self,
        analyser,
        reporter
    ):
        """
        Initialises the analysis service.

        Args:
            analyser: Log analyser responsible for processing log files.
            reporter: Log reporter providing structured analysis results.

        Returns:
            None
        """

        self.analyser = analyser
        self.reporter = reporter

    def analyse_file(
            self,
            file_path: Path
    ) -> None:
        """
        Analyses a validated log file.

        Args:
            file_path (Path): Validated log file path to analyse.

        Returns:
            None
        """

        self.analyser.analyse(
            file_path
        )

    def get_summary(
            self
    ) -> AnalysisSummary:
        """
        Returns structured summary for current analysis.

        Returns:
            AnalysisSummary: Aggregate results for the analysed log data.
        """

        return self.reporter.get_analysis_summary()

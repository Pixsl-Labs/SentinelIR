from app.reporting.statistics import Statistics
from app.reporting.detection import Detection
from app.reporting.investigation import Investigation
from app.reporting.exports import Export
from app.reporting.summary import Summary
from app.reporting.filter_values import FilterValues


class LogReporter(
    Statistics,
    Detection,
    Investigation,
    Export,
    Summary,
    FilterValues
):
    """
    Combines reporting, detection, investigation, export, and summary features.

    LogReporter uses multiple mixins to provide a single interface for
    printing analysis results, exporting data, viewing statistics, and running
    detection-focused reports against the analyser state.
    """

    def __init__(self, analyser):
        """
        Initialises the log reporter.

        Stores the analyser instance used by the inherited reporting, detection,
        investigation, export, and summary methods.

        Args:
            analyser (_type_): Log analyser instance containing parsed authentication data.

        Returns:
            None
        """
        self.analyser = analyser

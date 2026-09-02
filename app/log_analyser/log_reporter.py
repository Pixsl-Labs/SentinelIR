from app.reporting.statistics import Statistics
from app.reporting.detection import Detection
from app.reporting.investigation import Investigation
from app.reporting.exports import Export
from app.reporting.summary import Summary
from app.reporting.filter_values import FilterValues

from app.detection.detection_engine import DetectionEngine

from app.models.analysis_summary import AnalysisSummary


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

    def __init__(
        self,
        analyser
    ) -> None:
        """
        Initialises the log reporter.

        Stores the analyser instance used by the inherited reporting,
        detection, investigation, export, and summary methods.

        Args:
            analyser: Log analyser instance containing parsed authentication
                data.

        Returns:
            None
        """

        self.analyser = analyser

    def get_analysis_summary(
        self
    ) -> AnalysisSummary:
        """
        Builds and returns a structured summary of the current analysis.

        Returns:
            AnalysisSummary: Aggregate totals for analysed events,
                authentication outcomes, unique IP addresses, services,
                severities, and detections.
        """

        entries = self.analyser.log_entries

        return AnalysisSummary(
            total_events=len(entries),
            failed_logins=len(
                self.analyser.failed_logins
            ),
            successful_logins=len(
                self.analyser.successful_logins
            ),
            unique_ips=len({
                entry.ip
                for entry in entries
            }),
            service_totals={
                service: sum(
                    1
                    for entry in entries
                    if entry.service == service
                )
                for service in {
                    entry.service
                    for entry in entries
                }
            },
            severity_totals={
                severity: sum(
                    1
                    for entry in entries
                    if entry.severity == severity
                )
                for severity in {
                    entry.severity
                    for entry in entries
                }
            },
            detection_counts={
                "brute_force": len(
                    DetectionEngine.get_brute_force(
                        self.analyser
                    )
                ),
                "suspicious_success": len(
                    DetectionEngine.get_suspicious_success(
                        self.analyser
                    )
                ),
                "user_targeting": len(
                    DetectionEngine.get_user_targeting(
                        self.analyser
                    )
                ),
                "anonymous_ftp": len(
                    DetectionEngine.get_anonymous_ftp_logins(
                        self.analyser
                    )
                )
            }
        )

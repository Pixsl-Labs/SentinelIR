from dataclasses import dataclass, field


@dataclass
class AnalysisSummary:
    """
    Represents the high-level results of a completed log analysis.

    Attributes:
        total_events (int): Total number of analysed log events.
        failed_logins (int): Number of failed authentication events.
        successful_logins (int): Number of successful authentication events.
        unique_ips (int): Number of unique source IP addresses.
        service_totals (dict[str, int]): Event totals grouped by service.
        severity_totals (dict[str, int]): Event totals grouped by severity.
        detection_counts (dict[str, int]): Totals for each detection category.
    """

    total_events: int
    failed_logins: int
    successful_logins: int
    unique_ips: int
    service_totals: dict[str, int] = field(default_factory=dict)
    severity_totals: dict[str, int] = field(default_factory=dict)
    detection_counts: dict[str, int] = field(default_factory=dict)

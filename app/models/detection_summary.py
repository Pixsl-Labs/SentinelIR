from dataclasses import dataclass, field


@dataclass
class DetectionResults:
    """
    Represents all structured detection findings for an analysis.

    Attributes:
        brute_force (list): Brute-force detection findings.
        suspicious_success (list): Successful logins following suspicious failures.
        suspicious_ips (list): Suspicious source IP findings.
        user_targeting (list): Distributed username-targeting findings.
        anonymous_ftp (list): Anonymous FTP login findings.
    """

    brute_force: list = field(default_factory=list)
    suspicious_success: list = field(default_factory=list)
    suspicious_ips: list = field(default_factory=list)
    user_targeting: list = field(default_factory=list)
    anonymous_ftp: list = field(default_factory=list)

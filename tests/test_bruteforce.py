from app.log_analyser.log_analyser import LogAnalyser
from app.detection.detection_engine import DetectionEngine


def test_brute_force_detected():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/brute_force.log")

    results = DetectionEngine.get_brute_force(analyser, 5, 10)

    assert len(results) > 0


def test_no_brute_force_detected():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/clean.log")

    results = DetectionEngine.get_brute_force(analyser, 5, 10)

    assert len(results) == 0

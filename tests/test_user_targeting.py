from app.log_analyser.log_reporter import LogReporter
from app.log_analyser.log_analyser import LogAnalyser
from app.detection.detection_engine import DetectionEngine

def test_user_targeting_detected():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/distributed_attack.log")

    results = DetectionEngine.get_user_targeting(analyser, 5)

    assert len(results) > 0

def test_no_user_targeting_detected():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/clean.log")

    results = DetectionEngine.get_user_targeting(analyser, 5)

    assert len(results) == 0

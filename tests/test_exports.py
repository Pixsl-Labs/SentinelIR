import json
import os

from app.log_analyser.log_reporter import LogReporter
from app.log_analyser.log_analyser import LogAnalyser


def test_export_txt_creates_file(brute_force_reporter):
    output_file = "tests/test_reports/test_txt_report_created.txt"

    data = brute_force_reporter.get_failed_logins()

    brute_force_reporter.export_txt(
        output_file,
        "Failed Logins",
        data
    )

    assert os.path.exists(output_file)

def test_export_txt_contains_headers(brute_force_reporter):

    output_file = "tests/test_reports/test_txt_report_created.txt"

    data = brute_force_reporter.get_failed_logins()

    brute_force_reporter.export_txt(
        output_file,
        "Failed Logins",
        data
    )

    with open(output_file, "r") as file:
        content = file.read()

    assert "Service" in content
    assert "Status" in content
    assert "Timestamp" in content
    assert "User" in content
    assert "IP Address" in content
    assert "Method" in content
    assert "Path" in content
    assert "Code" in content
    assert "Severity" in content

def test_export_txt_contains_first_result(brute_force_reporter):

    output_file = "tests/test_reports/test_txt_first_result.txt"

    data = brute_force_reporter.get_failed_logins()

    brute_force_reporter.export_txt(
        output_file,
        "Failed Logins",
        data
    )

    first_entry = data[0]

    with open(output_file, "r") as file:
        content = file.read()

    assert first_entry.service in content
    assert f"[{first_entry.status}]" in content
    assert first_entry.user in content
    assert first_entry.ip in content
    assert first_entry.severity in content

def test_export_txt_contains_filters(brute_force_reporter):

    output_file = "tests/test_reports/test_filtered_report.txt"

    filters = {
        "service": "FTP",
        "username": "root"
    }

    data = brute_force_reporter.get_failed_logins(
        **filters
    )

    brute_force_reporter.export_txt(
        output_file,
        "Failed Logins",
        data,
        filters=filters
    )

    with open(output_file, "r") as file:
        content = file.read()

    assert "Filters Applied:" in content
    assert "- service: FTP" in content
    assert "- username: root" in content

    assert "FTP" in content
    assert "root" in content


def test_export_json_creates_file(brute_force_reporter):
    output_file = "tests/test_reports/test_json_report_created.json"

    data = brute_force_reporter.get_failed_logins()

    brute_force_reporter.export_json(
        output_file,
        "Failed Logins",
        data
    )

    assert os.path.exists(output_file)

def test_export_json_contains_expected_keys(brute_force_reporter):
    output_file = "tests/test_reports/test_report.json"

    data = brute_force_reporter.get_failed_logins()

    brute_force_reporter.export_json(
        output_file,
        "Failed Logins",
        data
    )

    with open(output_file, "r") as file:
        exported_data = json.load(file)

    expected_keys = {
        "metadata",
        "results"
    }

    assert expected_keys.issubset(exported_data.keys())

def test_export_json_first_result_contains_expected_fields(brute_force_reporter):

    output_file = "tests/test_reports/test_report.json"

    data = brute_force_reporter.get_failed_logins()

    brute_force_reporter.export_json(
        output_file,
        "Failed Logins",
        data
    )

    with open(output_file, "r") as file:
        exported_data = json.load(file)

    results = exported_data["results"]

    assert len(results) > 0

    first_result = results[0]

    assert first_result["status"] == data[0].status
    assert first_result["service"] == data[0].service
    assert first_result["user"] == data[0].user
    assert first_result["ip"] == data[0].ip
    assert first_result["severity"] == data[0].severity

def test_export_json_contains_filters(brute_force_reporter):

    output_file = "tests/test_reports/test_filtered_report.json"

    filters = {
        "service": "FTP",
        "username": "admin"
    }

    data = brute_force_reporter.get_failed_logins(
        **filters
    )

    brute_force_reporter.export_json(
        output_file,
        "Failed Logins",
        data,
        filters=filters
    )

    with open(output_file, "r") as file:
        exported_data = json.load(file)

    assert exported_data["metadata"]["filters"]["service"] == "FTP"
    assert exported_data["metadata"]["filters"]["username"] == "admin"
    assert exported_data["metadata"]["result_count"] == len(data)


    assert all(
        result["service"].upper() == "FTP"
        and result["user"].lower() == "admin"
        for result in exported_data["results"]
    )

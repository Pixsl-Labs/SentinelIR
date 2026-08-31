import json

from app.config.config_loader import load_config
from app.models.app_config import AppConfig


def test_load_config_returns_app_config(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_data = {
        "watched_files": [
            "log_files/generated.log"
        ],

        "thresholds": {
            "brute_force_threshold": 5,
            "brute_force_time_window": 10,
            "user_targeting_threshold": 5
        },

        "live_monitoring": {
            "poll_interval": 0.2,
            "status_interval": 10,
            "show_new_logs": True
        },

        "outputs": {
            "reports_dir": "reports",
            "logs_dir": "logs"
        }
    }

    config_file.write_text(
        json.dumps(config_data)
    )

    config = load_config(
        str(config_file)
    )

    assert isinstance(config, AppConfig)

def test_load_config_reads_watched_files(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_data = {
        "watched_files": [
            "log_files/generated.log",
            "log_files/auth.log"
        ],

        "thresholds": {
            "brute_force_threshold": 5,
            "brute_force_time_window": 10,
            "user_targeting_threshold": 5
        },

        "live_monitoring": {
            "poll_interval": 0.2,
            "status_interval": 10,
            "show_new_logs": True
        },

        "outputs": {
            "reports_dir": "reports",
            "logs_dir": "logs"
        }
    }

    config_file.write_text(
        json.dumps(config_data)
    )

    config = load_config(
        str(config_file)
    )

    assert config.watched_files == [
        "log_files/generated.log",
        "log_files/auth.log"
    ]

def test_load_config_reads_thresholds(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_data = {
        "watched_files": [
            "log_files/generated.log"
        ],

        "thresholds": {
            "brute_force_threshold": 5,
            "brute_force_time_window": 10,
            "user_targeting_threshold": 5
        },

        "live_monitoring": {
            "poll_interval": 0.2,
            "status_interval": 10,
            "show_new_logs": True
        },

        "outputs": {
            "reports_dir": "reports",
            "logs_dir": "logs"
        }
    }

    config_file.write_text(
        json.dumps(config_data)
    )

    config = load_config(
        str(config_file)
    )

    assert config.thresholds.brute_force_threshold == 5
    assert config.thresholds.brute_force_time_window == 10
    assert config.thresholds.user_targeting_threshold == 5

def test_load_config_uses_defaults_when_optional_sections_missing(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_data = {
        "watched_files": [
            "log_files/generated.log"
        ]
    }

    config_file.write_text(
        json.dumps(config_data)
    )

    config = load_config(
        str(config_file)
    )

    assert config.watched_files == [
        "log_files/generated.log"
    ]

    assert config.thresholds.brute_force_threshold == 5
    assert config.thresholds.brute_force_time_window == 10
    assert config.thresholds.user_targeting_threshold == 5

    assert config.live_monitoring.poll_interval == 0.2
    assert config.live_monitoring.status_interval == 10
    assert config.live_monitoring.show_new_logs == True

    assert config.outputs.reports_dir == "reports"
    assert config.outputs.logs_dir == "logs"

def test_build_app_config_reads_live_monitoring_settings(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_data = {
        "watched_files": [
            "log_files/generated.log"
        ],

        "thresholds": {
            "brute_force_threshold": 5,
            "brute_force_time_window": 10,
            "user_targeting_threshold": 5
        },

        "live_monitoring": {
            "poll_interval": 0.2,
            "status_interval": 10,
            "show_new_logs": True
        },

        "outputs": {
            "reports_dir": "reports",
            "logs_dir": "logs"
        }
    }

    config_file.write_text(
        json.dumps(config_data)
    )

    config = load_config(
        str(config_file)
    )

    assert config.live_monitoring.poll_interval == 0.2
    assert config.live_monitoring.status_interval == 10
    assert config.live_monitoring.show_new_logs is True

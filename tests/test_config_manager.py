import json

from app.config.config_manager import (
    list_available_log_files,
    add_watched_file,
    remove_watched_file
)


def test_list_available_log_files_returns_only_log_files(tmp_path):
    log_dir = tmp_path / "log_files"

    log_dir.mkdir()

    auth_log = log_dir / "auth.log"
    brute_force_log = log_dir / "brute_force.log"
    notes_file = log_dir / "notes.txt"

    auth_log.write_text("test auth log")
    brute_force_log.write_text("test brute force log")
    notes_file.write_text("not a log file!")

    results = list_available_log_files(
        str(log_dir)
    )

    assert results == sorted([
        str(auth_log),
        str(brute_force_log)
    ])

    assert str(notes_file) not in results


def test_add_watched_file_updates_config(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_file.write_text(
        json.dumps({
            "watched_files": []
        })
    )

    added = add_watched_file(
        str(config_file),
        "log_files/auth.log"
    )

    config_data = json.loads(
        config_file.read_text()
    )

    assert added is True
    assert "log_files/auth.log" in config_data["watched_files"]


def test_add_watched_file_prevents_duplicates(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_file.write_text(
        json.dumps({
            "watched_files": [
                "log_files/auth.log"
            ]
        })
    )

    added = add_watched_file(
        str(config_file),
        "log_files/auth.log"
    )

    config_data = json.loads(
        config_file.read_text()
    )

    assert added is False
    assert config_data["watched_files"].count("log_files/auth.log") == 1


def test_remove_watched_file_updates_config(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    real_log_file = tmp_path / "auth.log"
    real_log_file.write_text("log content")

    config_file.write_text(
        json.dumps({
            "watched_files": [
                str(real_log_file)
            ]
        })
    )

    removed = remove_watched_file(
        str(config_file),
        str(real_log_file)
    )

    config_data = json.loads(
        config_file.read_text()
    )

    assert removed is True
    assert str(real_log_file) not in config_data["watched_files"]
    assert real_log_file.exists()


def test_remove_watched_file_returns_false_when_file_not_configured(tmp_path):
    config_file = tmp_path / "sentinel_config.json"

    config_file.write_text(
        json.dumps({
            "watched_files": [
                "log_files/auth.log"
            ]
        })
    )

    removed = remove_watched_file(
        str(config_file),
        "log_files/not_configured.log"
    )

    config_data = json.loads(
        config_file.read_text()
    )

    assert removed is False
    assert config_data["watched_files"] == [
        "log_files/auth.log"
    ]

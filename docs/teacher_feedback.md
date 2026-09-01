# Ian Feedback Action List

## Background Monitoring

- Explore a non-interactive mode where SentinelIR reads watched files from a config file.
- Add support for multiple watched files.
- Consider a future background/service mode.

## Configuration

- Review whether security_config.py should remain Python-based.
- Consider sentinel_config.json for thresholds and monitored files.
- Consider .env for future secrets/API keys.

## Documentation

- Add missing class/function docstrings.
- Improve developer readability.

## Future Interface

- Consider Qt/PySide6 for desktop GUI.
- Consider Flask/FastAPI + Docker as alternative local web app route.

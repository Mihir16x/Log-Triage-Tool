from datetime import datetime

from src.parser import parse_log_line


def test_parse_valid_log_line():
    line = (
        "2026-09-20 09:00:01 "
        "INFO auth-service User 1024 logged in successfully"
    )

    result = parse_log_line(line)

    assert result["timestamp"] == datetime(2026, 9, 20, 9, 0, 1)
    assert result["level"] == "INFO"
    assert result["service"] == "auth-service"
    assert result["message"] == "User 1024 logged in successfully"
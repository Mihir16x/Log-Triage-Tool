from src.analyzer import (
    count_levels,
    detect_error_spikes,
    error_rate_by_service,
    errors_by_service,
)


def sample_logs():
    return [
        {
            "timestamp": "2026-09-20 09:00:00",
            "level": "INFO",
            "service": "api-service",
            "message": "Request received",
        },
        {
            "timestamp": "2026-09-20 09:00:10",
            "level": "ERROR",
            "service": "api-service",
            "message": "Request failed",
        },
        {
            "timestamp": "2026-09-20 09:00:20",
            "level": "ERROR",
            "service": "api-service",
            "message": "Request failed",
        },
        {
            "timestamp": "2026-09-20 09:00:30",
            "level": "ERROR",
            "service": "api-service",
            "message": "Request failed",
        },
        {
            "timestamp": "2026-09-20 09:01:00",
            "level": "WARN",
            "service": "worker-service",
            "message": "Slow task",
        },
    ]


def test_count_levels():
    result = count_levels(sample_logs())

    assert result["INFO"] == 1
    assert result["WARN"] == 1
    assert result["ERROR"] == 3


def test_errors_by_service():
    result = errors_by_service(sample_logs())

    assert result["api-service"] == 3


def test_error_rate_by_service():
    result = error_rate_by_service(sample_logs())

    assert result["api-service"] == 0.75
    assert result["worker-service"] == 0.0


def test_detect_error_spikes():
    result = detect_error_spikes(sample_logs())

    assert len(result) == 1
    assert result[0]["service"] == "api-service"
    assert result[0]["error_count"] == 3